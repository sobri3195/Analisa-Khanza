#!/usr/bin/env python3
"""Sinkronisasi otomatis mapping online dari database Khanza ke endpoint API.

Fitur utama:
- Tarik data mapping aktif dari MySQL/MariaDB.
- Submit otomatis ke API eksternal (POST JSON).
- Mendukung dry-run untuk validasi sebelum eksekusi.
- Menyimpan state lokal agar data yang tidak berubah tidak dikirim ulang.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pymysql
import requests
import yaml


@dataclass
class SyncConfig:
    db: dict[str, Any]
    api: dict[str, Any]
    sync: dict[str, Any]


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def load_config(path: Path) -> SyncConfig:
    if not path.exists():
        raise FileNotFoundError(f"Config tidak ditemukan: {path}")

    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    for required in ("db", "api", "sync"):
        if required not in raw:
            raise ValueError(f"Bagian '{required}' wajib ada pada config")

    return SyncConfig(db=raw["db"], api=raw["api"], sync=raw["sync"])


def connect_db(db_cfg: dict[str, Any]) -> pymysql.connections.Connection:
    return pymysql.connect(
        host=db_cfg["host"],
        port=int(db_cfg.get("port", 3306)),
        user=db_cfg["user"],
        password=db_cfg["password"],
        database=db_cfg["database"],
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4",
        autocommit=True,
    )


def fetch_rows(conn: pymysql.connections.Connection, query: str, limit: int | None) -> list[dict[str, Any]]:
    sql = query
    params: tuple[Any, ...] = ()
    if limit and limit > 0:
        sql = f"{query.rstrip().rstrip(';')} LIMIT %s"
        params = (limit,)

    with conn.cursor() as cur:
        cur.execute(sql, params)
        return list(cur.fetchall())


def state_checksum(row: dict[str, Any]) -> str:
    material = json.dumps(row, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def load_state(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_state(path: Path, state: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, ensure_ascii=False)


def submit_payload(session: requests.Session, url: str, timeout: int, payload: dict[str, Any]) -> requests.Response:
    return session.post(url, json=payload, timeout=timeout)


def build_payload(row: dict[str, Any], mapping: dict[str, str]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for source_key, target_key in mapping.items():
        payload[target_key] = row.get(source_key)
    return payload


def run_sync(config: SyncConfig, dry_run: bool, force: bool, limit: int | None) -> int:
    query = config.sync.get(
        "query",
        """
        SELECT
            id,
            kode_provider,
            kode_layanan_online,
            kode_poli_khanza,
            kode_dokter_khanza,
            nama_layanan_online,
            aktif,
            updated_at
        FROM mapping_online_khanza
        WHERE aktif='YA'
        ORDER BY updated_at ASC
        """,
    )

    key_field = config.sync.get("key_field", "id")
    state_file = Path(config.sync.get("state_file", "sobri/.state/mapping_sync_state.json"))
    timeout = int(config.api.get("timeout_seconds", 30))
    field_mapping = config.sync.get(
        "field_mapping",
        {
            "kode_provider": "providerCode",
            "kode_layanan_online": "serviceCode",
            "kode_poli_khanza": "khanzaPolyCode",
            "kode_dokter_khanza": "khanzaDoctorCode",
            "nama_layanan_online": "serviceName",
            "aktif": "isActive",
        },
    )

    previous_state = load_state(state_file)
    new_state = previous_state.copy()

    conn = connect_db(config.db)
    rows = fetch_rows(conn, query, limit)
    conn.close()

    if not rows:
        logging.info("Tidak ada data mapping aktif untuk diproses")
        return 0

    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})

    token = config.api.get("bearer_token")
    if token:
        session.headers.update({"Authorization": f"Bearer {token}"})

    endpoint = config.api["endpoint"]
    success = 0
    skipped = 0
    failed = 0

    for row in rows:
        row_key = str(row.get(key_field))
        if row_key in ("None", ""):
            logging.warning("Baris tanpa key_field '%s' dilewati: %s", key_field, row)
            skipped += 1
            continue

        checksum = state_checksum(row)
        if not force and previous_state.get(row_key) == checksum:
            skipped += 1
            logging.debug("Skip id=%s (tidak ada perubahan)", row_key)
            continue

        payload = build_payload(row, field_mapping)
        logging.info("Proses id=%s payload=%s", row_key, payload)

        if dry_run:
            success += 1
            new_state[row_key] = checksum
            continue

        try:
            response = submit_payload(session, endpoint, timeout, payload)
            if 200 <= response.status_code < 300:
                success += 1
                new_state[row_key] = checksum
                logging.info("Sukses submit id=%s status=%s", row_key, response.status_code)
            else:
                failed += 1
                logging.error(
                    "Gagal submit id=%s status=%s response=%s",
                    row_key,
                    response.status_code,
                    response.text[:500],
                )
        except requests.RequestException as exc:
            failed += 1
            logging.exception("Error request id=%s: %s", row_key, exc)

    save_state(state_file, new_state)
    logging.info("Ringkasan sync -> sukses=%s, skip=%s, gagal=%s", success, skipped, failed)
    return 1 if failed > 0 else 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync mapping online Khanza ke API eksternal")
    parser.add_argument("--config", default="sobri/config.example.yaml", help="Path file YAML konfigurasi")
    parser.add_argument("--dry-run", action="store_true", help="Jalankan simulasi tanpa kirim ke API")
    parser.add_argument("--force", action="store_true", help="Kirim ulang semua data walau tidak berubah")
    parser.add_argument("--limit", type=int, default=None, help="Batasi jumlah data yang diproses")
    parser.add_argument("--log-level", default="INFO", help="DEBUG/INFO/WARNING/ERROR")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    setup_logging(args.log_level)

    try:
        cfg = load_config(Path(args.config))
        return run_sync(cfg, dry_run=args.dry_run, force=args.force, limit=args.limit)
    except Exception as exc:  # pragma: no cover
        logging.exception("Eksekusi gagal: %s", exc)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
