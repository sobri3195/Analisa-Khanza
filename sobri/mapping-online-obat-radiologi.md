# Mapping Online Berhasil (MD) — Obat & Radiologi

Dokumen ini dipakai sebagai **template siap pakai** agar mapping online untuk domain **obat** dan **radiologi** bisa dieksekusi dengan pola yang sama seperti pipeline `khanza_online_sync.py`.

## 1) Tujuan
- Menstandarkan field yang dikirim ke API online.
- Memudahkan validasi apakah mapping sudah “berhasil” (siap kirim).
- Menyediakan contoh query SQL + field mapping YAML.

## 2) Definisi “Mapping Berhasil” (Checklist)
Sebuah baris mapping dinyatakan **berhasil** jika:

- `aktif = 'YA'`.
- Kode master lokal terisi (kode obat / kode pemeriksaan radiologi).
- Kode referensi online terisi.
- Nama item tidak kosong.
- `updated_at` terisi (untuk incremental sync).

## 3) Struktur Tabel Rekomendasi

### 3.1 Mapping Obat
```sql
CREATE TABLE IF NOT EXISTS mapping_online_obat (
    id BIGINT NOT NULL AUTO_INCREMENT,
    kode_provider VARCHAR(50) NOT NULL,
    kode_obat_khanza VARCHAR(30) NOT NULL,
    kode_obat_online VARCHAR(100) NOT NULL,
    nama_obat_khanza VARCHAR(150) NOT NULL,
    satuan_khanza VARCHAR(30) DEFAULT NULL,
    aktif ENUM('YA','TIDAK') NOT NULL DEFAULT 'YA',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_provider_obat (kode_provider, kode_obat_online),
    KEY idx_obat_khanza (kode_obat_khanza)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 3.2 Mapping Radiologi
```sql
CREATE TABLE IF NOT EXISTS mapping_online_radiologi (
    id BIGINT NOT NULL AUTO_INCREMENT,
    kode_provider VARCHAR(50) NOT NULL,
    kode_tindakan_radiologi_khanza VARCHAR(30) NOT NULL,
    kode_tindakan_radiologi_online VARCHAR(100) NOT NULL,
    nama_tindakan_radiologi_khanza VARCHAR(150) NOT NULL,
    modality VARCHAR(30) DEFAULT NULL,
    aktif ENUM('YA','TIDAK') NOT NULL DEFAULT 'YA',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_provider_radiologi (kode_provider, kode_tindakan_radiologi_online),
    KEY idx_tindakan_radiologi_khanza (kode_tindakan_radiologi_khanza)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## 4) Query Sinkronisasi (untuk config YAML)

### 4.1 Query Obat
```sql
SELECT
  id,
  kode_provider,
  kode_obat_khanza,
  kode_obat_online,
  nama_obat_khanza,
  satuan_khanza,
  aktif,
  updated_at
FROM mapping_online_obat
WHERE aktif='YA'
ORDER BY updated_at ASC;
```

### 4.2 Query Radiologi
```sql
SELECT
  id,
  kode_provider,
  kode_tindakan_radiologi_khanza,
  kode_tindakan_radiologi_online,
  nama_tindakan_radiologi_khanza,
  modality,
  aktif,
  updated_at
FROM mapping_online_radiologi
WHERE aktif='YA'
ORDER BY updated_at ASC;
```

## 5) Contoh `field_mapping` YAML

### 5.1 Field Mapping Obat
```yaml
sync:
  key_field: id
  state_file: "sobri/.state/mapping_sync_state_obat.json"
  query: |
    SELECT
      id,
      kode_provider,
      kode_obat_khanza,
      kode_obat_online,
      nama_obat_khanza,
      satuan_khanza,
      aktif,
      updated_at
    FROM mapping_online_obat
    WHERE aktif='YA'
    ORDER BY updated_at ASC
  field_mapping:
    kode_provider: providerCode
    kode_obat_khanza: khanzaDrugCode
    kode_obat_online: onlineDrugCode
    nama_obat_khanza: drugName
    satuan_khanza: unit
    aktif: isActive
```

### 5.2 Field Mapping Radiologi
```yaml
sync:
  key_field: id
  state_file: "sobri/.state/mapping_sync_state_radiologi.json"
  query: |
    SELECT
      id,
      kode_provider,
      kode_tindakan_radiologi_khanza,
      kode_tindakan_radiologi_online,
      nama_tindakan_radiologi_khanza,
      modality,
      aktif,
      updated_at
    FROM mapping_online_radiologi
    WHERE aktif='YA'
    ORDER BY updated_at ASC
  field_mapping:
    kode_provider: providerCode
    kode_tindakan_radiologi_khanza: khanzaRadiologyCode
    kode_tindakan_radiologi_online: onlineRadiologyCode
    nama_tindakan_radiologi_khanza: radiologyName
    modality: modality
    aktif: isActive
```

## 6) Validasi Cepat Sebelum Go-Live

### 6.1 Cari data invalid di mapping obat
```sql
SELECT *
FROM mapping_online_obat
WHERE aktif='YA'
  AND (
    kode_obat_khanza IS NULL OR kode_obat_khanza='' OR
    kode_obat_online IS NULL OR kode_obat_online='' OR
    nama_obat_khanza IS NULL OR nama_obat_khanza=''
  );
```

### 6.2 Cari data invalid di mapping radiologi
```sql
SELECT *
FROM mapping_online_radiologi
WHERE aktif='YA'
  AND (
    kode_tindakan_radiologi_khanza IS NULL OR kode_tindakan_radiologi_khanza='' OR
    kode_tindakan_radiologi_online IS NULL OR kode_tindakan_radiologi_online='' OR
    nama_tindakan_radiologi_khanza IS NULL OR nama_tindakan_radiologi_khanza=''
  );
```

## 7) Cara Eksekusi
1. Siapkan 2 file config YAML terpisah (mis. `config.obat.yaml` dan `config.radiologi.yaml`).
2. Jalankan dry-run dulu untuk masing-masing domain.
3. Jika payload sudah benar, jalankan mode real.

Contoh:
```bash
python sobri/khanza_online_sync.py --config sobri/config.obat.yaml --dry-run --log-level DEBUG
python sobri/khanza_online_sync.py --config sobri/config.radiologi.yaml --dry-run --log-level DEBUG

python sobri/khanza_online_sync.py --config sobri/config.obat.yaml
python sobri/khanza_online_sync.py --config sobri/config.radiologi.yaml
```

## 8) Output yang Diharapkan
- Tidak ada baris invalid dari query validasi.
- Log sync menampilkan sukses > 0 dan gagal = 0.
- State file domain obat/radiologi terbentuk otomatis di folder `sobri/.state/`.
