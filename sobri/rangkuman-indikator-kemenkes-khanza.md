# Rangkuman Implementasi RME Khanza untuk Kemenkes (6 Indikator)

Dokumen ini menjawab 4 poin:
1) 6 indikator Kemenkes dan status umum di Khanza.
2) Data ditarik per kapan.
3) Prioritas mapping: paling sulit, paling banyak, dan strategi 1 bulan.
4) Solusi masalah implementasi.

---

## 1) Enam indikator Kemenkes: dari Khanza sudah aman?

> Jawaban singkat: **belum bisa dinyatakan “semua aman” tanpa audit dashboard SATUSEHAT + uji data aktual**.  
> Namun dari struktur modul dan artefak yang ada, Khanza sudah punya pondasi kuat untuk menuju aman.

### Indikator 1 — Kepatuhan regulasi & kelembagaan
**Cek:** RS/fasyankes terdaftar, sistem RME terdaftar, dan tata kelola PIC/SOP berjalan.  
**Status Khanza:** *bergantung institusi* (bukan software saja). Aplikasi bisa siap, tapi status regulasi tetap harus divalidasi di level RS.

### Indikator 2 — Kesiapan integrasi SATUSEHAT
**Cek:** kredensial production aktif, koneksi stabil, endpoint terkonfigurasi, monitoring aktif.  
**Status Khanza:** ada komponen integrasi SATUSEHAT di codebase, sehingga secara teknis **siap diintegrasikan** bila kredensial dan konfigurasi benar.

### Indikator 3 — Cakupan resource prioritas
**Cek:** resource prioritas (minimal identitas fasilitas, pasien, tenaga medis, encounter, kondisi/diagnostik, imunisasi/lab sesuai layanan) terkirim.  
**Status Khanza:** dari artefak laporan terlihat sudah ada jejak resource SATUSEHAT (mis. Encounter, Condition, DiagnosticReport Lab, Imunisasi), indikasi cakupan sudah berjalan sebagian.

### Indikator 4 — Kualitas data
**Cek:** kelengkapan field wajib, validitas coding (ICD/SNOMED/LOINC/KFA sesuai kebutuhan), konsistensi relasi antar-resource.  
**Status Khanza:** **umumnya ini area paling sering jadi gap**. Aman atau tidak harus dilihat dari rasio error validasi dan audit mapping istilah.

### Indikator 5 — Kinerja transaksi
**Cek:** persentase sukses HTTP 200/201, retry berhasil, antrean tidak menumpuk, latency terkontrol.  
**Status Khanza:** dapat dimonitor dan ditingkatkan dengan logging, retry, dan dashboard harian.

### Indikator 6 — Operasional berkelanjutan
**Cek:** SOP insiden, SLA perbaikan, rekonsiliasi data, review mingguan lintas unit, dan perbaikan berulang.  
**Status Khanza:** perlu penguatan proses organisasi agar stabil jangka panjang.

### Kesimpulan status “aman”
Gunakan klasifikasi praktis berikut:
- **Hijau (aman):** sukses transaksi konsisten tinggi, error validasi rendah, dan tidak ada backlog signifikan.
- **Kuning:** transaksi berjalan tapi error kualitas data masih berulang.
- **Merah:** banyak gagal kirim/validasi dan belum ada SLA penanganan.

Tanpa angka dari dashboard, jawaban jujur adalah: **belum bisa klaim 100% aman**.

---

## 2) Data ditarik per kapan?

Rekomendasi praktik aman:

1. **Near real-time** untuk layanan kritikal (mis. IGD/rawat inap): interval **5–15 menit**.  
2. **Batch terjadwal** untuk layanan non-kritikal/rekap: **setiap jam** atau **harian**.  
3. Gunakan **watermark waktu** (`last_updated`) + **ID terakhir** agar tidak ada data lompat/duplikat.  
4. Tetapkan **cutoff rekonsiliasi harian** (mis. jam 23:59 waktu server) untuk catch-up data gagal.

Template kebijakan waktu tarik:
- Mode operasional: tiap 10 menit.
- Mode rekonsiliasi: 1x per hari tarik ulang data H-1 dan H-2.
- Mode insiden: force reprocess per resource/kunjungan.

---

## 3) Mapping: paling sulit, paling banyak, dan cara khusus dalam 1 bulan

### A. Mapping paling sulit (umumnya)
1. **Terminologi klinis** (SNOMED/LOINC/KFA) karena perlu padanan lokal → standar nasional/internasional.
2. **Relasi antar-resource** (Encounter–Condition–Observation–DiagnosticReport–Medication) agar referensi konsisten.
3. **Data historis yang tidak seragam** (legacy input bebas, singkatan lokal, field kosong).

### B. Mapping paling banyak volume
1. **Observation** (tanda vital/lab/non-lab) → volume tertinggi.
2. **Encounter** → hampir semua layanan membuat encounter.
3. **Condition & DiagnosticReport** → tinggi pada layanan penyakit kronis/lab.

### C. Cara khusus (rencana 1 bulan)

#### Minggu 1 — Baseline & prioritas
- Inventaris semua field lokal yang dikirim ke SATUSEHAT.
- Kelompokkan: wajib, penting, tambahan.
- Hitung baseline: sukses kirim, error validasi, dan backlog.

#### Minggu 2 — Fokus 20 mapping penyumbang error terbesar
- Ambil **Top 20 error code** paling sering.
- Buat tabel padanan kode + aturan transformasi.
- Terapkan normalisasi input (format tanggal, satuan, enum).

#### Minggu 3 — Hardening pipeline
- Tambah retry bertahap (exponential backoff), dead-letter queue sederhana, dan rekonsiliasi otomatis H-1/H-2.
- Tambah dashboard harian per resource + error reason.

#### Minggu 4 — Stabilkan operasional
- Simulasi insiden (token gagal, timeout, payload invalid).
- Tetapkan SLA: kritikal <24 jam, mayor <3 hari.
- Finalisasi SOP dan jadwal review mingguan lintas tim.

Output akhir 1 bulan yang harus terlihat:
- Tren error menurun konsisten tiap minggu.
- Top error lama hilang/menurun drastis.
- Tidak ada backlog tua yang tidak tertangani.

---

## 4) Solusi untuk masalah implementasi

### Masalah umum → solusi langsung

1. **Registrasi/kredensial belum sinkron**  
   **Solusi:** checklist administrasi satu pintu, PIC tunggal, dan verifikasi berkala status akses.

2. **Banyak gagal validasi payload**  
   **Solusi:** validator lokal sebelum kirim + kamus mapping terpusat + uji regresi payload.

3. **Kode lokal tidak cocok terminologi standar**  
   **Solusi:** governance terminologi (owner per kamus kode), mapping bertahap dari layanan prioritas tinggi.

4. **Data klinis kosong/tidak konsisten dari unit layanan**  
   **Solusi:** perbaiki form input, field wajib kontekstual, dan umpan balik mutu data ke unit tiap minggu.

5. **Transaksi tersendat saat trafik tinggi**  
   **Solusi:** queue + retry + circuit breaker ringan, dan monitoring antrean real-time.

6. **Tim operasional reaktif, bukan proaktif**  
   **Solusi:** dashboard KPI harian, rapat review mingguan 30 menit, dan SLA berbasis prioritas.

---

## Checklist eksekusi cepat (praktis)

- [ ] Validasi 6 indikator dengan status Hijau/Kuning/Merah.
- [ ] Tetapkan interval tarik data + mekanisme rekonsiliasi.
- [ ] Pilih 20 mapping prioritas tertinggi berdasarkan error nyata.
- [ ] Jalankan rencana 4 minggu dengan metrik mingguan.
- [ ] Review hasil bulan pertama dan lanjutkan siklus perbaikan.

Jika diperlukan, dokumen ini bisa langsung diturunkan menjadi:
1) template KPI mingguan,  
2) template SLA insiden integrasi,  
3) tabel prioritas mapping per resource SATUSEHAT.
