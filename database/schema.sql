-- =====================================================
-- Kurumsal Bilgi Yönetimi Sistemi
-- Veritabanı Şeması (Schema)
-- PostgreSQL
-- =====================================================
-- Kullanıcılar tablosu

CREATE TABLE kullanicilar
(
    kullanici_id SERIAL,

    ad_soyad VARCHAR(100) NOT NULL,

    eposta VARCHAR(150) NOT NULL,

    sifre_ozeti VARCHAR(255) NOT NULL,

    rol VARCHAR(30) NOT NULL,

    departman VARCHAR(50) NOT NULL,

    olusturulma_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_kullanicilar
        PRIMARY KEY (kullanici_id),

    CONSTRAINT uq_kullanicilar_eposta
        UNIQUE (eposta)

);

-- İndeksler

CREATE INDEX idx_kullanicilar_eposta
ON kullanicilar(eposta);

-- Dokümanlar tablosu

CREATE TABLE dokumanlar
(
    dokuman_id SERIAL,

    baslik VARCHAR(200) NOT NULL,

    dosya_adi VARCHAR(255) NOT NULL,

    dosya_turu VARCHAR(10) NOT NULL,

    yukleyen_kullanici_id INTEGER NOT NULL,

    yuklenme_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    departman VARCHAR(50) NOT NULL,

    surum_no INTEGER NOT NULL DEFAULT 1,

    dosya_yolu VARCHAR(300) NOT NULL,

    durum VARCHAR(20) NOT NULL,

    CONSTRAINT pk_dokumanlar
        PRIMARY KEY (dokuman_id),

    CONSTRAINT fk_dokumanlar_kullanicilar
        FOREIGN KEY (yukleyen_kullanici_id)
        REFERENCES kullanicilar(kullanici_id),

    CONSTRAINT uq_dokumanlar_dosya_yolu
        UNIQUE (dosya_yolu),

    CONSTRAINT chk_dokumanlar_dosya_turu
        CHECK (dosya_turu IN ('pdf', 'docx', 'xlsx')),

    CONSTRAINT chk_dokumanlar_surum_no
        CHECK (surum_no >= 1),

    CONSTRAINT chk_dokumanlar_durum
        CHECK (durum IN ('Isleniyor', 'Aktif', 'Arsivlendi'))
);

-- İndeksler

CREATE INDEX idx_dokumanlar_yukleyen_kullanici
ON dokumanlar(yukleyen_kullanici_id);

CREATE INDEX idx_dokumanlar_departman
ON dokumanlar(departman);

CREATE INDEX idx_dokumanlar_yuklenme_tarihi
ON dokumanlar(yuklenme_tarihi);

CREATE INDEX idx_dokumanlar_durum
ON dokumanlar(durum);

-- Doküman Parçaları tablosu

CREATE TABLE dokuman_parcalari
(
    parca_id SERIAL,

    dokuman_id INTEGER NOT NULL,

    parca_sirasi INTEGER NOT NULL,

    parca_metni TEXT NOT NULL,

    sayfa_no INTEGER,

    token_sayisi INTEGER NOT NULL,

    embedding_id VARCHAR(100),

    olusturulma_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_dokuman_parcalari
        PRIMARY KEY (parca_id),

    CONSTRAINT fk_dokuman_parcalari_dokumanlar
        FOREIGN KEY (dokuman_id)
        REFERENCES dokumanlar(dokuman_id),

    CONSTRAINT uq_dokuman_parcalari_embedding_id
        UNIQUE (embedding_id),

    CONSTRAINT uq_dokuman_parcalari_dokuman_parca
        UNIQUE (dokuman_id, parca_sirasi),

    CONSTRAINT chk_dokuman_parcalari_parca_sirasi
        CHECK (parca_sirasi >= 1),

    CONSTRAINT chk_dokuman_parcalari_sayfa_no
        CHECK (sayfa_no IS NULL OR sayfa_no >= 1),

    CONSTRAINT chk_dokuman_parcalari_token_sayisi
        CHECK (token_sayisi > 0)
);

-- İndeksler

CREATE INDEX idx_dokuman_parcalari_dokuman
ON dokuman_parcalari(dokuman_id);

CREATE INDEX idx_dokuman_parcalari_embedding
ON dokuman_parcalari(embedding_id);

-- Sohbet Oturumları tablosu

CREATE TABLE sohbet_oturumlari
(
    oturum_id SERIAL,

    kullanici_id INTEGER NOT NULL,

    oturum_basligi VARCHAR(200) NOT NULL,

    baslangic_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_sohbet_oturumlari
        PRIMARY KEY (oturum_id),

    CONSTRAINT fk_sohbet_oturumlari_kullanicilar
        FOREIGN KEY (kullanici_id)
        REFERENCES kullanicilar(kullanici_id)
);

-- İndeksler

CREATE INDEX idx_sohbet_oturumlari_kullanici
ON sohbet_oturumlari(kullanici_id);

CREATE INDEX idx_sohbet_oturumlari_baslangic_tarihi
ON sohbet_oturumlari(baslangic_tarihi);

-- Sohbet Mesajları tablosu

CREATE TABLE sohbet_mesajlari
(
    mesaj_id SERIAL,

    oturum_id INTEGER NOT NULL,

    gonderen_tipi VARCHAR(20) NOT NULL,

    mesaj_metni TEXT NOT NULL,

    olusturulma_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_sohbet_mesajlari
        PRIMARY KEY (mesaj_id),

    CONSTRAINT fk_sohbet_mesajlari_sohbet_oturumlari
        FOREIGN KEY (oturum_id)
        REFERENCES sohbet_oturumlari(oturum_id),

    CONSTRAINT chk_sohbet_mesajlari_gonderen_tipi
        CHECK (gonderen_tipi IN ('Kullanici', 'Yapay Zeka'))
);

-- İndeksler

CREATE INDEX idx_sohbet_mesajlari_oturum
ON sohbet_mesajlari(oturum_id);

CREATE INDEX idx_sohbet_mesajlari_olusturulma_tarihi
ON sohbet_mesajlari(olusturulma_tarihi);

-- Doküman Etiketleri tablosu

CREATE TABLE dokuman_etiketleri
(
    dokuman_etiket_id SERIAL,

    dokuman_id INTEGER NOT NULL,

    etiket_adi VARCHAR(50) NOT NULL,

    CONSTRAINT pk_dokuman_etiketleri
        PRIMARY KEY (dokuman_etiket_id),

    CONSTRAINT fk_dokuman_etiketleri_dokumanlar
        FOREIGN KEY (dokuman_id)
        REFERENCES dokumanlar(dokuman_id),

    CONSTRAINT uq_dokuman_etiketleri_dokuman_etiket
        UNIQUE (dokuman_id, etiket_adi)
);

-- İndeksler

CREATE INDEX idx_dokuman_etiketleri_dokuman
ON dokuman_etiketleri(dokuman_id);

CREATE INDEX idx_dokuman_etiketleri_etiket
ON dokuman_etiketleri(etiket_adi);

-- Doküman Yetkileri tablosu

CREATE TABLE dokuman_yetkileri
(
    yetki_id SERIAL,

    dokuman_id INTEGER NOT NULL,

    rol_adi VARCHAR(30) NOT NULL,

    goruntuleyebilir_mi BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT pk_dokuman_yetkileri
        PRIMARY KEY (yetki_id),

    CONSTRAINT fk_dokuman_yetkileri_dokumanlar
        FOREIGN KEY (dokuman_id)
        REFERENCES dokumanlar(dokuman_id),

    CONSTRAINT uq_dokuman_yetkileri_dokuman_rol
        UNIQUE (dokuman_id, rol_adi)
);

-- İndeksler

CREATE INDEX idx_dokuman_yetkileri_dokuman
ON dokuman_yetkileri(dokuman_id);

CREATE INDEX idx_dokuman_yetkileri_rol
ON dokuman_yetkileri(rol_adi); 