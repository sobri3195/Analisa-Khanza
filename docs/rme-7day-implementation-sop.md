# SOP Implementasi 7 Hari — Stabilkan Mapping RME (Khanza + SATUSEHAT)

Dokumen ini untuk eksekusi cepat lintas unit tanpa mengganggu layanan.

## Tujuan 7 hari
1. Coverage mapping domain prioritas mencapai >=95%.
2. Encounter & domain utama berjalan stabil.
3. Backlog mapping terkendali dengan PIC jelas.

## Tim minimum
- Koordinator: IT SIMRS
- PIC Farmasi
- PIC Lab
- PIC Radiologi
- PIC Poli/Ranap
- Verifikator RM/Mutu

## Hari 1 — Kickoff & Baseline
- Tetapkan PIC per domain.
- Tarik baseline gap: lokasi, obat, lab, radiologi, vaksin.
- Buat file kerja dari template:
  - `Daily_Control`
  - `Mapping_Backlog`
  - `Incident_Log`
- Freeze sementara pembuatan master baru tanpa mapping.

**Output hari 1:** daftar gap prioritas + owner.

## Hari 2 — Fondasi Organisasi & Lokasi
- Finalisasi mapping organisasi/departemen.
- Finalisasi mapping lokasi:
  - Poli ralan
  - Kamar ranap
  - Ruang lab, radiologi, OK, farmasi
- Uji kirim encounter setelah lokasi valid.

**Output hari 2:** encounter berhasil untuk sampel kasus uji.

## Hari 3 — Obat/KFA (prioritas tinggi)
- Mapping 50 item obat volume tertinggi.
- Fokus IGD/ICU/ruang intensif lebih dulu.
- Validasi alur medication (request/dispense/statement) pada sampel kunjungan.

**Output hari 3:** 80% item top-volume farmasi termapping.

## Hari 4 — Laboratorium
- Mapping item lab prioritas (top 30–50).
- Uji ServiceRequest, Specimen, Observation, DiagnosticReport lab.
- Catat error semantik kode/system/display pada `Incident_Log`.

**Output hari 4:** domain lab stabil untuk item prioritas.

## Hari 5 — Radiologi + Vaksin
- Mapping item radiologi prioritas (top 20–30).
- Mapping vaksin aktif.
- Uji end-to-end radiologi & imunisasi.

**Output hari 5:** domain radiologi/vaksin stabil.

## Hari 6 — Hardening & Rekonsiliasi
- Rekonsiliasi data layanan vs data terkirim 3 hari terakhir.
- Bersihkan repeat issue.
- Tutup gap medium priority.

**Output hari 6:** repeat issue turun signifikan, backlog terkendali.

## Hari 7 — Serah Operasional
- Review KPI minggu berjalan:
  - Coverage mapping
  - Success rate kirim
  - Median TAT tutup gap
  - Repeat issue
- Tetapkan SOP rutin:
  - Daily 20–30 menit
  - Weekly review 60–90 menit
- Approve daftar kontrol permanen oleh manajemen.

**Output hari 7:** proses masuk BAU (business as usual).

---

## SOP Eskalasi Cepat

### Level 1 (<=2 jam) — PIC Domain
- Lengkapi mapping item gagal.
- Re-run kirim domain terkait.
- Update status di `Daily_Control`.

### Level 2 (2–8 jam) — Koordinator IT
- Validasi dependency (lokasi/organisasi).
- Validasi konfigurasi auth/fhir.
- Putuskan workaround operasional.

### Level 3 (>8 jam) — Manajemen
- War-room lintas unit.
- Kunci perubahan master tanpa approval mapping.
- Tetapkan deadline & owner tunggal sampai closed.

---

## Definition of Done
- Tidak ada gap High priority terbuka >24 jam.
- Coverage mapping >=95% (target awal) dan tren naik.
- Success rate kirim >=98% pada domain prioritas.
