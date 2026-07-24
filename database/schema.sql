-- Kurumsal Bilgi Yönetimi veritabanı şeması
-- Çalıştırma sırası: 1

-- pgvector eklentisini etkinleştirir
CREATE EXTENSION IF NOT EXISTS vector;

-- Departmanları tutar
CREATE TABLE departmanlar
(
    departman_id SERIAL,
    departman_adi VARCHAR(50) NOT NULL,
    CONSTRAINT pk_departmanlar PRIMARY KEY (departman_id),
    CONSTRAINT uq_departmanlar_departman_adi UNIQUE (departman_adi)
);

-- Sistem kullanıcılarını tutar
CREATE TABLE kullanicilar
(
    kullanici_id SERIAL,
    ad_soyad VARCHAR(100) NOT NULL,
    eposta VARCHAR(150) NOT NULL,
    sifre_ozeti VARCHAR(255) NOT NULL,
    rol VARCHAR(30) NOT NULL,
    departman_id INTEGER NOT NULL,
    aktif_mi BOOLEAN NOT NULL DEFAULT TRUE,
    olusturulma_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    guncelleme_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_kullanicilar PRIMARY KEY (kullanici_id),
    CONSTRAINT uq_kullanicilar_eposta UNIQUE (eposta),
    CONSTRAINT chk_kullanicilar_rol CHECK (rol IN ('Yonetici', 'Personel')),
    CONSTRAINT fk_kullanicilar_departmanlar FOREIGN KEY (departman_id)
        REFERENCES departmanlar(departman_id)
);

-- Kurumsal dokümanların üst bilgilerini tutar
CREATE TABLE dokumanlar
(
    dokuman_id SERIAL,
    baslik VARCHAR(200) NOT NULL,
    dosya_adi VARCHAR(255) NOT NULL,
    dosya_turu VARCHAR(10) NOT NULL,
    yukleyen_kullanici_id INTEGER NOT NULL,
    yuklenme_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    departman_id INTEGER NOT NULL,
    surum_no INTEGER NOT NULL DEFAULT 1,
    dosya_yolu VARCHAR(300) NOT NULL,
    durum VARCHAR(20) NOT NULL DEFAULT 'Isleniyor',
    dosya_boyutu BIGINT NOT NULL,
    guncelleme_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_dokumanlar PRIMARY KEY (dokuman_id),
    CONSTRAINT fk_dokumanlar_kullanicilar FOREIGN KEY (yukleyen_kullanici_id)
        REFERENCES kullanicilar(kullanici_id),
    CONSTRAINT fk_dokumanlar_departmanlar FOREIGN KEY (departman_id)
        REFERENCES departmanlar(departman_id),
    CONSTRAINT uq_dokumanlar_dosya_yolu UNIQUE (dosya_yolu),
    CONSTRAINT chk_dokumanlar_dosya_turu CHECK (dosya_turu IN ('pdf', 'docx', 'xlsx')),
    CONSTRAINT chk_dokumanlar_surum_no CHECK (surum_no >= 1),
    CONSTRAINT chk_dokumanlar_durum CHECK (durum IN ('Isleniyor', 'Aktif', 'Hata', 'Arsiv')),
    CONSTRAINT chk_dokumanlar_dosya_boyutu CHECK (dosya_boyutu > 0)
);

-- Dokümanların RAG için bölünmüş metin parçalarını ve embeddinglerini tutar
CREATE TABLE dokuman_parcalari
(
    parca_id SERIAL,
    dokuman_id INTEGER NOT NULL,
    parca_sirasi INTEGER NOT NULL,
    parca_metni TEXT NOT NULL,
    sayfa_no INTEGER,
    token_sayisi INTEGER NOT NULL,
    embedding VECTOR(1536),
    olusturulma_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_dokuman_parcalari PRIMARY KEY (parca_id),
    CONSTRAINT fk_dokuman_parcalari_dokumanlar FOREIGN KEY (dokuman_id)
        REFERENCES dokumanlar(dokuman_id) ON DELETE CASCADE,
    CONSTRAINT uq_dokuman_parcalari_dokuman_parca UNIQUE (dokuman_id, parca_sirasi),
    CONSTRAINT chk_dokuman_parcalari_parca_sirasi CHECK (parca_sirasi >= 1),
    CONSTRAINT chk_dokuman_parcalari_sayfa_no CHECK (sayfa_no IS NULL OR sayfa_no >= 1),
    CONSTRAINT chk_dokuman_parcalari_token_sayisi CHECK (token_sayisi > 0)
);

-- Kullanıcıların sohbet oturumlarını tutar
CREATE TABLE sohbet_oturumlari
(
    oturum_id SERIAL,
    kullanici_id INTEGER NOT NULL,
    oturum_basligi VARCHAR(200) NOT NULL,
    baslangic_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sohbet_oturumlari PRIMARY KEY (oturum_id),
    CONSTRAINT fk_sohbet_oturumlari_kullanicilar FOREIGN KEY (kullanici_id)
        REFERENCES kullanicilar(kullanici_id)
);

-- Sohbetlerdeki kullanıcı ve yapay zekâ mesajlarını tutar
CREATE TABLE sohbet_mesajlari
(
    mesaj_id SERIAL,
    oturum_id INTEGER NOT NULL,
    gonderen_tipi VARCHAR(20) NOT NULL,
    mesaj_metni TEXT NOT NULL,
    olusturulma_tarihi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_sohbet_mesajlari PRIMARY KEY (mesaj_id),
    CONSTRAINT fk_sohbet_mesajlari_sohbet_oturumlari FOREIGN KEY (oturum_id)
        REFERENCES sohbet_oturumlari(oturum_id) ON DELETE CASCADE,
    CONSTRAINT chk_sohbet_mesajlari_gonderen_tipi CHECK (gonderen_tipi IN ('Kullanici', 'AI'))
);

-- Doküman etiketlerini tutar
CREATE TABLE dokuman_etiketleri
(
    dokuman_etiket_id SERIAL,
    dokuman_id INTEGER NOT NULL,
    etiket_adi VARCHAR(50) NOT NULL,
    CONSTRAINT pk_dokuman_etiketleri PRIMARY KEY (dokuman_etiket_id),
    CONSTRAINT fk_dokuman_etiketleri_dokumanlar FOREIGN KEY (dokuman_id)
        REFERENCES dokumanlar(dokuman_id) ON DELETE CASCADE,
    CONSTRAINT uq_dokuman_etiketleri_dokuman_etiket UNIQUE (dokuman_id, etiket_adi)
);

-- Departmanların doküman görüntüleme yetkilerini tutar
CREATE TABLE dokuman_yetkileri
(
    yetki_id SERIAL,
    dokuman_id INTEGER NOT NULL,
    goruntuleyebilir_mi BOOLEAN NOT NULL DEFAULT TRUE,
    departman_id INTEGER NOT NULL,
    CONSTRAINT pk_dokuman_yetkileri PRIMARY KEY (yetki_id),
    CONSTRAINT fk_dokuman_yetkileri_dokumanlar FOREIGN KEY (dokuman_id)
        REFERENCES dokumanlar(dokuman_id) ON DELETE CASCADE,
    CONSTRAINT fk_dokuman_yetkileri_departmanlar FOREIGN KEY (departman_id)
        REFERENCES departmanlar(departman_id),
    CONSTRAINT uq_dokuman_yetkileri_dokuman_departman UNIQUE (dokuman_id, departman_id)
);

-- AI cevaplarının dayandığı doküman parçalarını tutar
CREATE TABLE mesaj_kaynaklari
(
    kaynak_id SERIAL,
    mesaj_id INTEGER NOT NULL,
    parca_id INTEGER NOT NULL,
    benzerlik_puani DECIMAL(5,4) NOT NULL,
    CONSTRAINT pk_mesaj_kaynaklari PRIMARY KEY (kaynak_id),
    CONSTRAINT fk_mesaj_kaynaklari_mesaj FOREIGN KEY (mesaj_id)
        REFERENCES sohbet_mesajlari(mesaj_id) ON DELETE CASCADE,
    CONSTRAINT fk_mesaj_kaynaklari_parca FOREIGN KEY (parca_id)
        REFERENCES dokuman_parcalari(parca_id) ON DELETE CASCADE,
    CONSTRAINT uq_mesaj_kaynaklari_mesaj_parca UNIQUE (mesaj_id, parca_id),
    CONSTRAINT chk_mesaj_kaynaklari_benzerlik_puani
        CHECK (benzerlik_puani >= 0 AND benzerlik_puani <= 1)
);

-- Sorgu performansı için indeksleri oluşturur
CREATE INDEX idx_kullanicilar_departman_id ON kullanicilar(departman_id);
CREATE INDEX idx_kullanicilar_aktif_mi ON kullanicilar(aktif_mi);
CREATE INDEX idx_dokumanlar_yukleyen_kullanici ON dokumanlar(yukleyen_kullanici_id);
CREATE INDEX idx_dokumanlar_departman_id ON dokumanlar(departman_id);
CREATE INDEX idx_dokumanlar_yuklenme_tarihi ON dokumanlar(yuklenme_tarihi);
CREATE INDEX idx_dokumanlar_durum ON dokumanlar(durum);
CREATE INDEX idx_dokuman_parcalari_dokuman ON dokuman_parcalari(dokuman_id);
CREATE INDEX idx_dokuman_parcalari_embedding_hnsw
    ON dokuman_parcalari USING hnsw (embedding vector_cosine_ops);
CREATE INDEX idx_sohbet_oturumlari_kullanici ON sohbet_oturumlari(kullanici_id);
CREATE INDEX idx_sohbet_oturumlari_baslangic_tarihi ON sohbet_oturumlari(baslangic_tarihi);
CREATE INDEX idx_sohbet_mesajlari_oturum ON sohbet_mesajlari(oturum_id);
CREATE INDEX idx_sohbet_mesajlari_olusturulma_tarihi ON sohbet_mesajlari(olusturulma_tarihi);
CREATE INDEX idx_dokuman_etiketleri_dokuman ON dokuman_etiketleri(dokuman_id);
CREATE INDEX idx_dokuman_etiketleri_etiket ON dokuman_etiketleri(etiket_adi);
CREATE INDEX idx_dokuman_yetkileri_dokuman ON dokuman_yetkileri(dokuman_id);
CREATE INDEX idx_dokuman_yetkileri_departman_id ON dokuman_yetkileri(departman_id);
CREATE INDEX idx_mesaj_kaynaklari_mesaj ON mesaj_kaynaklari(mesaj_id);
CREATE INDEX idx_mesaj_kaynaklari_parca ON mesaj_kaynaklari(parca_id);

-- Doküman embedding aramalarını hızlandırır
CREATE INDEX IF NOT EXISTS idx_dokuman_parcalari_embedding_hnsw
ON dokuman_parcalari
USING hnsw (embedding vector_cosine_ops);

-- Kullanıcı güncellenme tarihini otomatik yeniler
CREATE OR REPLACE FUNCTION fn_kullanicilar_guncelleme_tarihi()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.guncelleme_tarihi = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_kullanicilar_guncelleme_tarihi
BEFORE UPDATE ON kullanicilar
FOR EACH ROW EXECUTE FUNCTION fn_kullanicilar_guncelleme_tarihi();

-- Doküman güncellenme tarihini otomatik yeniler
CREATE OR REPLACE FUNCTION fn_dokumanlar_guncelleme_tarihi()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.guncelleme_tarihi = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_dokumanlar_guncelleme_tarihi
BEFORE UPDATE ON dokumanlar
FOR EACH ROW EXECUTE FUNCTION fn_dokumanlar_guncelleme_tarihi();

-- Temel sayısal raporlama fonksiyonlarını oluşturur
CREATE OR REPLACE FUNCTION fn_chunk_sayisi(p_dokuman_id INTEGER)
RETURNS INTEGER LANGUAGE sql STABLE AS $$
    SELECT COUNT(*)::INTEGER FROM dokuman_parcalari WHERE dokuman_id = p_dokuman_id;
$$;

CREATE OR REPLACE FUNCTION fn_token_sayisi(p_dokuman_id INTEGER)
RETURNS INTEGER LANGUAGE sql STABLE AS $$
    SELECT COALESCE(SUM(token_sayisi), 0)::INTEGER
    FROM dokuman_parcalari WHERE dokuman_id = p_dokuman_id;
$$;

CREATE OR REPLACE FUNCTION fn_kullanici_dokuman_sayisi(p_kullanici_id INTEGER)
RETURNS INTEGER LANGUAGE sql STABLE AS $$
    SELECT COUNT(*)::INTEGER FROM dokumanlar WHERE yukleyen_kullanici_id = p_kullanici_id;
$$;

CREATE OR REPLACE FUNCTION fn_sohbet_mesaj_sayisi(p_oturum_id INTEGER)
RETURNS INTEGER LANGUAGE sql STABLE AS $$
    SELECT COUNT(*)::INTEGER FROM sohbet_mesajlari WHERE oturum_id = p_oturum_id;
$$;

CREATE OR REPLACE FUNCTION fn_dokuman_etiket_sayisi(p_dokuman_id INTEGER)
RETURNS INTEGER LANGUAGE sql STABLE AS $$
    SELECT COUNT(*)::INTEGER FROM dokuman_etiketleri WHERE dokuman_id = p_dokuman_id;
$$;

-- Kullanıcının rol ve departmanına göre görebileceği dokümanları döndürür
CREATE OR REPLACE FUNCTION fn_kullanicinin_gorebildigi_dokumanlar(p_kullanici_id INTEGER)
RETURNS SETOF dokumanlar LANGUAGE sql STABLE AS $$
    SELECT DISTINCT d.*
    FROM dokumanlar d
    INNER JOIN kullanicilar k ON k.kullanici_id = p_kullanici_id
    LEFT JOIN dokuman_yetkileri dy
        ON dy.dokuman_id = d.dokuman_id
       AND dy.departman_id = k.departman_id
       AND dy.goruntuleyebilir_mi = TRUE
    WHERE k.aktif_mi = TRUE
      AND (k.rol = 'Yonetici'
           OR d.yukleyen_kullanici_id = k.kullanici_id
           OR dy.yetki_id IS NOT NULL);
$$;

-- Doküman durumunu değiştiren prosedürleri oluşturur
CREATE OR REPLACE PROCEDURE sp_dokuman_arsivle(IN p_dokuman_id INTEGER)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE dokumanlar SET durum = 'Arsiv' WHERE dokuman_id = p_dokuman_id;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_dokuman_geri_aktiflestir(IN p_dokuman_id INTEGER)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE dokumanlar SET durum = 'Aktif' WHERE dokuman_id = p_dokuman_id;
END;
$$;

-- Aktif dokümanları gösterir
CREATE VIEW vw_aktif_dokumanlar AS
SELECT d.dokuman_id, d.baslik, d.dosya_adi, d.dosya_turu, d.dosya_boyutu,
       d.yukleyen_kullanici_id, d.yuklenme_tarihi, d.guncelleme_tarihi,
       d.departman_id, dep.departman_adi, d.surum_no, d.dosya_yolu, d.durum
FROM dokumanlar d
INNER JOIN departmanlar dep ON dep.departman_id = d.departman_id
WHERE d.durum = 'Aktif';

-- Doküman ve yükleyen kullanıcı özetini gösterir
CREATE VIEW vw_dokuman_ozeti AS
SELECT d.dokuman_id, d.baslik, d.dosya_adi, d.dosya_turu, d.dosya_boyutu,
       k.ad_soyad AS yukleyen_kullanici, dep.departman_adi, d.surum_no,
       d.durum, d.yuklenme_tarihi, d.guncelleme_tarihi
FROM dokumanlar d
INNER JOIN kullanicilar k ON d.yukleyen_kullanici_id = k.kullanici_id
INNER JOIN departmanlar dep ON d.departman_id = dep.departman_id;

-- Sohbetlerin mesaj sayılarını gösterir
CREATE VIEW vw_sohbet_ozeti AS
SELECT s.oturum_id, k.ad_soyad, s.oturum_basligi, s.baslangic_tarihi,
       COUNT(m.mesaj_id) AS toplam_mesaj
FROM sohbet_oturumlari s
INNER JOIN kullanicilar k ON s.kullanici_id = k.kullanici_id
LEFT JOIN sohbet_mesajlari m ON s.oturum_id = m.oturum_id
GROUP BY s.oturum_id, k.ad_soyad, s.oturum_basligi, s.baslangic_tarihi;

-- Dokümanların parça, etiket, yetki ve token sayılarını gösterir
CREATE VIEW vw_dokuman_istatistikleri AS
SELECT d.dokuman_id, d.baslik, dep.departman_adi,
       (SELECT COUNT(*) FROM dokuman_parcalari dp WHERE dp.dokuman_id = d.dokuman_id) AS parca_sayisi,
       (SELECT COUNT(*) FROM dokuman_etiketleri de WHERE de.dokuman_id = d.dokuman_id) AS etiket_sayisi,
       (SELECT COUNT(*) FROM dokuman_yetkileri dy WHERE dy.dokuman_id = d.dokuman_id) AS yetki_sayisi,
       (SELECT COALESCE(SUM(dp.token_sayisi), 0) FROM dokuman_parcalari dp WHERE dp.dokuman_id = d.dokuman_id) AS toplam_token
FROM dokumanlar d
INNER JOIN departmanlar dep ON d.departman_id = dep.departman_id;