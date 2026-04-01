# Template Checklist Harian & Mingguan Mapping RME (Khanza + SATUSEHAT)

## Sheet 1 — `Daily_Control`
Gunakan satu baris per shift.

| Tanggal | Shift | PIC IT | PIC Unit | Service Up (Y/N) | Auth Token OK (Y/N) | Encounter OK (Y/N) | Gap Lokasi | Gap Obat/KFA | Gap Lab | Gap Radiologi | Gap Vaksin | Tindakan Koreksi | ETA | Status |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| 2026-__-__ | Pagi |  |  |  |  |  | 0 | 0 | 0 | 0 | 0 |  |  | Open/Closed |

### Definisi kolom
- **Service Up**: aplikasi service SATUSEHAT aktif.
- **Auth Token OK**: proses autentikasi berjalan normal.
- **Encounter OK**: encounter hari berjalan terkirim.
- **Gap***: jumlah item transaksi yang belum memiliki mapping.

## Sheet 2 — `Mapping_Backlog`
Gunakan untuk daftar item belum termapping.

| Domain | Kode Lokal | Nama Lokal | Kode Standar | System | Display | Unit Pemilik | PIC | Ditemukan Tgl | Prioritas | Status | Selesai Tgl | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Obat/KFA |  |  |  |  |  | Farmasi |  | 2026-__-__ | High/Med/Low | Belum Mapping/Done/Validasi |  | link/log |

### Aturan prioritas
1. **High**: item volume tinggi atau layanan kritis (IGD/ICU/OK).
2. **Medium**: item rutin dengan volume sedang.
3. **Low**: item long-tail/jarang dipakai.

## Sheet 3 — `Incident_Log`
Gunakan untuk insiden gagal kirim/gagal mapping.

| Tanggal-Jam | Domain | Gejala | Dampak | Root Cause | Fix | Preventive Action | PIC | SLA | Status |
|---|---|---|---|---|---|---|---|---|---|
| 2026-__-__ __:__ |  |  |  |  |  |  |  |  | Open/Closed |

## Template KPI Mingguan

| Minggu | Coverage Mapping (%) | Success Rate Kirim (%) | Median TAT Tutup Gap (jam) | Repeat Issue (jumlah) | Catatan |
|---|---:|---:|---:|---:|---|
| 2026-W__ | 0 | 0 | 0 | 0 |  |

### Rumus KPI
- **Coverage Mapping** = (item aktif termapping / item aktif total) x 100%
- **Success Rate Kirim** = (kirim sukses / total attempt kirim) x 100%
- **Median TAT Tutup Gap** = median selisih waktu item ditemukan hingga status Done

## Checklist 1 halaman (print)

### Header
- Tanggal:
- Shift:
- PIC IT:
- PIC Unit:

### A. Status Sistem
- [ ] Service SATUSEHAT aktif
- [ ] Koneksi DB normal
- [ ] Auth/token normal
- [ ] Tidak ada error kritis

### B. Prasyarat Mapping Inti
- [ ] Mapping Organisasi lengkap
- [ ] Mapping Lokasi Poli lengkap
- [ ] Mapping Lokasi Ranap lengkap
- [ ] Mapping Lokasi Farmasi/Lab/Rad lengkap

### C. Mapping Domain
- [ ] Obat/KFA termapping
- [ ] Lab termapping
- [ ] Radiologi termapping
- [ ] Vaksin termapping

### D. Hasil Kirim
- [ ] Encounter terkirim
- [ ] ServiceRequest/Observation/DiagnosticReport terkirim
- [ ] Medication flow terkirim
- [ ] Tidak ada gagal berulang

### E. Ringkasan Gap Hari Ini
- Gap Obat/KFA: ____
- Gap Lab: ____
- Gap Radiologi: ____
- Gap Vaksin: ____
- Gap Lokasi/Organisasi: ____

### F. Tindakan Koreksi
| No | Masalah | Akar Penyebab | Tindakan | PIC | ETA | Status |
|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  | Open/Closed |

Paraf PIC IT: ____________  
Paraf Verifikator Mutu/RM: ____________
