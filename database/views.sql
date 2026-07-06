-- Aktif Dokümanlar View

CREATE VIEW vw_aktif_dokumanlar AS

SELECT
    dokuman_id,
    baslik,
    dosya_adi,
    dosya_turu,
    yukleyen_kullanici_id,
    yuklenme_tarihi,
    departman,
    surum_no,
    dosya_yolu,
    durum
FROM dokumanlar
WHERE durum = 'Aktif';

-- Doküman Özeti View

CREATE VIEW vw_dokuman_ozeti AS

SELECT
    d.dokuman_id,
    d.baslik,
    d.dosya_adi,
    d.dosya_turu,
    k.ad_soyad AS yukleyen_kullanici,
    d.departman,
    d.surum_no,
    d.durum,
    d.yuklenme_tarihi
FROM dokumanlar d
INNER JOIN kullanicilar k
ON d.yukleyen_kullanici_id = k.kullanici_id;

-- Sohbet Özeti View

CREATE VIEW vw_sohbet_ozeti AS

SELECT
    s.oturum_id,
    k.ad_soyad,
    s.oturum_basligi,
    s.baslangic_tarihi,
    COUNT(m.mesaj_id) AS toplam_mesaj
FROM sohbet_oturumlari s
INNER JOIN kullanicilar k
ON s.kullanici_id = k.kullanici_id
LEFT JOIN sohbet_mesajlari m
ON s.oturum_id = m.oturum_id
GROUP BY
    s.oturum_id,
    k.ad_soyad,
    s.oturum_basligi,
    s.baslangic_tarihi;

-- Doküman İstatistikleri View

CREATE VIEW vw_dokuman_istatistikleri AS

SELECT
    d.dokuman_id,
    d.baslik,
    COUNT(DISTINCT dp.parca_id) AS parca_sayisi,
    COUNT(DISTINCT de.dokuman_etiket_id) AS etiket_sayisi,
    COUNT(DISTINCT dy.yetki_id) AS yetki_sayisi
FROM dokumanlar d
LEFT JOIN dokuman_parcalari dp
ON d.dokuman_id = dp.dokuman_id
LEFT JOIN dokuman_etiketleri de
ON d.dokuman_id = de.dokuman_id
LEFT JOIN dokuman_yetkileri dy
ON d.dokuman_id = dy.dokuman_id
GROUP BY
    d.dokuman_id,
    d.baslik;