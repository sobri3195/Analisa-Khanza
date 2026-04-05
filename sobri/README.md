# Sobri - Mapping Online Khanza

Folder ini berisi pondasi **otomasi mapping online Khanza** untuk mengambil data dari SQL (MySQL/MariaDB) lalu mengirimkannya otomatis ke endpoint API.

## 1) Analisa singkat codebase (relevan ke kebutuhan Anda)
- Repository ini dominan Java desktop (SIMRS Khanza) dan belum menyediakan pipeline Python bawaan untuk integrasi mapping online.
- Integrasi paling aman untuk tahap awal adalah model **sidecar script** (di luar aplikasi utama), supaya:
  1. Tidak mengganggu proses build Java utama.
  2. Mudah diuji bertahap dengan `--dry-run`.
  3. Mudah dijadwalkan via cron/Task Scheduler.
- Karena struktur database Khanza bisa berbeda antar instansi, query SQL dibuat configurable dari file YAML.

## 2) Isi folder
- `mapping_online_khanza.sql` → skema tabel mapping + contoh seed data.
- `khanza_online_sync.py` → script Python untuk tarik data SQL dan submit ke API.
- `config.example.yaml` → contoh konfigurasi DB, endpoint API, query, dan mapping field.
- `requirements.txt` → dependency Python.
- `mapping-online-obat-radiologi.md` → template mapping online berhasil untuk domain obat & radiologi.

## 3) Alur otomasi
1. Script baca config YAML.
2. Script tarik data aktif dari tabel `mapping_online_khanza`.
3. Script hitung checksum per baris.
4. Jika data belum berubah, script skip (hemat request).
5. Jika berubah, script kirim payload JSON ke API.
6. Script simpan state lokal ke `sobri/.state/mapping_sync_state.json`.

## 4) Instalasi & penggunaan
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r sobri/requirements.txt
```

Jalankan simulasi dulu:
```bash
python sobri/khanza_online_sync.py --config sobri/config.example.yaml --dry-run --log-level DEBUG
```

Jalankan eksekusi real:
```bash
python sobri/khanza_online_sync.py --config sobri/config.example.yaml
```

Opsional:
- `--force` : kirim ulang semua data walau belum berubah.
- `--limit 50` : batasi jumlah data saat testing.

## 5) Saran sebelum eksekusi produksi
1. **Pastikan kontrak API jelas**: metode auth, format field wajib, dan response error.
2. **Gunakan token/credential via secret manager atau environment variable** (hindari hardcode).
3. **Mulai dari dry-run + limit kecil** untuk validasi payload.
4. **Aktifkan logging terpusat** agar retry/insiden mudah ditelusuri.
5. **Siapkan retry/backoff** jika endpoint sering timeout (bisa jadi enhancement berikutnya).
6. **Tambahkan audit table** di DB bila butuh histori kirim per-record.

## 6) Jadwal otomatis
Contoh cron tiap 5 menit:
```bash
*/5 * * * * /path/to/.venv/bin/python /path/to/repo/sobri/khanza_online_sync.py --config /path/to/repo/sobri/config.example.yaml >> /var/log/khanza_sync.log 2>&1
```
