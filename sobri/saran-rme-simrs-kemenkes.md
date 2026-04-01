# Saran Pengiriman Data SIMRS ke Kemenkes & Indikator Implementasi RME

Pertanyaan: **"Bagaimana agar pengiriman data dari SIMRS ke Kemenkes lancar, dan apa indikator Kemenkes untuk implementasi RME?"**

## 1) Saran praktis agar pengiriman data SIMRS → Kemenkes lancar

1. **Pastikan jalur registrasi resmi selesai terlebih dahulu**
   - Update data sistem RME di **DFO/REGFASYANKES/RS Online**.
   - Pastikan sistem RME sudah terverifikasi (bila menggunakan vendor: vendor terverifikasi; bila mandiri: sistem didaftarkan).
   - Setelah data valid, kode akses API production umumnya tersedia dalam beberapa hari kerja.

2. **Bangun fondasi resource prasyarat terlebih dahulu**
   - Stabilkan resource inti: `Organization`, `Location`, `Practitioner`, `Patient`.
   - Lanjutkan ke resource layanan (mis. Encounter, Condition, Observation) sesuai use case.

3. **Gunakan standar terminologi sejak awal**
   - Lakukan pemetaan terminologi yang dibutuhkan (contoh: ICD, SNOMED CT, LOINC, KFA).
   - Banyak kegagalan integrasi terjadi karena *mapping* data yang belum konsisten.

4. **Pisahkan alur Sandbox vs Production**
   - Sandbox untuk uji skenario dan validasi.
   - Production untuk data riil dengan SOP penanganan error/rollback.

5. **Pasang monitoring harian berbasis dashboard SATUSEHAT**
   - Pantau **Ringkasan Transaksi FHIR** (indikasi sukses pada HTTP 200/201).
   - Pantau **Log Transaksi FHIR** untuk identifikasi error per resource ID.
   - Tetapkan PIC yang menindaklanjuti error harian.

6. **Perkuat tata kelola internal**
   - Tetapkan PIC teknis, PIC mutu data, PIC layanan, dan penanggung jawab manajemen.
   - Susun SLA penyelesaian error (contoh: error kritis <24 jam).

7. **Selaraskan proses klinis dan proses IT**
   - Pastikan form/input layanan klinis mendukung pengisian field wajib.
   - Lakukan review berkala bersama unit layanan agar data tidak kosong/invalid.

---

## 2) Indikator Kemenkes untuk implementasi RME (praktis untuk monitoring)

> Catatan: indikator di bawah merupakan turunan operasional dari regulasi dan panduan resmi Kemenkes/SATUSEHAT yang lazim dipakai di lapangan.

### A. Indikator kepatuhan regulasi
- Fasyankes menyelenggarakan RME.
- RME terintegrasi dengan platform SATUSEHAT.
- Memenuhi ketentuan pembinaan/pengawasan yang berlaku.

### B. Indikator kesiapan integrasi
- Registrasi/verifikasi fasyankes dan sistem RME selesai.
- Kredensial/API production aktif.
- Akses dashboard monitoring aktif.

### C. Indikator transaksi interoperabilitas
- Jumlah transaksi sukses per resource (HTTP 200/201).
- Konsistensi pengiriman data (harian/mingguan).
- Cakupan resource sesuai jenis layanan yang berjalan.

### D. Indikator kualitas data
- Kelengkapan elemen data wajib.
- Konsistensi relasi antar-resource.
- Tren penurunan error validasi dari waktu ke waktu.

### E. Indikator tata kelola & keamanan
- SOP integrasi, audit trail, dan manajemen insiden tersedia.
- Kontrol akses dan kerahasiaan data diterapkan.
- Evaluasi berkala oleh manajemen berjalan.

---

## 3) Tanggal penting implementasi

- **Permenkes No. 24 Tahun 2022** ditetapkan pada **31 Agustus 2022**.
- Masa transisi penerapan RME sempat didorong hingga **31 Desember 2023** pada fase awal implementasi.
- Dalam perkembangan implementasi nasional, terdapat komunikasi Kemenkes/BKPK yang mendorong percepatan integrasi hingga **akhir 2025**.

---

## Referensi resmi

1. Permenkes No. 24 Tahun 2022 (JDIH Kemenkes):
   https://jdih.kemkes.go.id/documents/peraturan-menteri-kesehatan-nomor-24-tahun-2022
2. Panduan registrasi fasyankes SATUSEHAT:
   https://satusehat.kemkes.go.id/platform/docs/id/registration-guide/regis-institution/
3. Panduan monitoring SATUSEHAT:
   https://satusehat.kemkes.go.id/platform/docs/id/monitoring-guide/
4. Ringkasan transaksi FHIR SATUSEHAT:
   https://satusehat.kemkes.go.id/platform/docs/id/monitoring-guide/transaksi-fhir/
5. Rilis BKPK Kemenkes (percepatan integrasi):
   https://www.badankebijakan.kemkes.go.id/wajib-integrasi-satu-sehat-kemenkes-desak-percepatan-rme-di-fasyankes/
6. Rilis Ditjen Keslan terkait pembinaan/SE:
   https://keslan.kemkes.go.id/read/1704/desk-sistem-informasi-rumah-sakit-rme-dan-satusehat
