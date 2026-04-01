-- Baseline tabel mapping layanan online ke master Khanza
CREATE TABLE IF NOT EXISTS mapping_online_khanza (
    id BIGINT NOT NULL AUTO_INCREMENT,
    kode_provider VARCHAR(50) NOT NULL,
    kode_layanan_online VARCHAR(100) NOT NULL,
    kode_poli_khanza VARCHAR(5) NOT NULL,
    kode_dokter_khanza VARCHAR(20) DEFAULT NULL,
    nama_layanan_online VARCHAR(150) DEFAULT NULL,
    aktif ENUM('YA','TIDAK') NOT NULL DEFAULT 'YA',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_provider_layanan (kode_provider, kode_layanan_online),
    KEY idx_poli (kode_poli_khanza),
    KEY idx_dokter (kode_dokter_khanza)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Contoh data awal
INSERT INTO mapping_online_khanza
(kode_provider, kode_layanan_online, kode_poli_khanza, kode_dokter_khanza, nama_layanan_online, aktif)
VALUES
('BOOKING_APP', 'POLI-INT-001', 'INT', NULL, 'Poli Penyakit Dalam', 'YA')
ON DUPLICATE KEY UPDATE
nama_layanan_online = VALUES(nama_layanan_online),
aktif = VALUES(aktif),
updated_at = CURRENT_TIMESTAMP;
