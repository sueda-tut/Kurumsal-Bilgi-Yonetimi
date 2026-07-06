-- INNER JOIN Sorguları


-- Kullanıcı -> Doküman

SELECT
    k.kullanici_id,
    k.ad_soyad,
    d.dokuman_id,
    d.baslik,
    d.yuklenme_tarihi
FROM kullanicilar k
INNER JOIN dokumanlar d
ON k.kullanici_id = d.yukleyen_kullanici_id;

-- Doküman -> Chunk

SELECT
    d.dokuman_id,
    d.baslik,
    dp.parca_id,
    dp.parca_sirasi,
    dp.token_sayisi
FROM dokumanlar d
INNER JOIN dokuman_parcalari dp
ON d.dokuman_id = dp.dokuman_id;


-- Doküman -> Etiket

SELECT
    d.dokuman_id,
    d.baslik,
    de.etiket_adi
FROM dokumanlar d
INNER JOIN dokuman_etiketleri de
ON d.dokuman_id = de.dokuman_id;

-- Sohbet -> Mesaj

SELECT
    s.oturum_id,
    s.oturum_basligi,
    sm.mesaj_id,
    sm.gonderen_tipi,
    sm.mesaj_metni
FROM sohbet_oturumlari s
INNER JOIN sohbet_mesajlari sm
ON s.oturum_id = sm.oturum_id;

-- LEFT JOIN Sorguları

-- Etiketi Olmayan Dokümanlar

SELECT
    d.dokuman_id,
    d.baslik
FROM dokumanlar d
LEFT JOIN dokuman_etiketleri de
ON d.dokuman_id = de.dokuman_id
WHERE de.dokuman_etiket_id IS NULL;

-- Mesajı Olmayan Sohbetler

SELECT
    s.oturum_id,
    s.oturum_basligi,
    s.baslangic_tarihi
FROM sohbet_oturumlari s
LEFT JOIN sohbet_mesajlari sm
ON s.oturum_id = sm.oturum_id
WHERE sm.mesaj_id IS NULL;

-- GROUP BY Sorguları

-- Dashboard
-- Departmanlara Göre Doküman Sayısı

SELECT
    departman,
    COUNT(*) AS dokuman_sayisi
FROM dokumanlar
GROUP BY departman;

-- İstatistik Ekranı
-- Dosya Türüne Göre Doküman Sayısı

SELECT
    dosya_turu,
    COUNT(*) AS dokuman_sayisi
FROM dokumanlar
GROUP BY dosya_turu;


-- Yönetici Paneli
-- Kullanıcıların Yüklediği Doküman Sayısı

SELECT
    k.ad_soyad,
    COUNT(d.dokuman_id) AS yuklenen_dokuman_sayisi
FROM kullanicilar k
LEFT JOIN dokumanlar d
ON k.kullanici_id = d.yukleyen_kullanici_id
GROUP BY
    k.kullanici_id,
    k.ad_soyad;


-- HAVING Sorguları

-- Minimum Doküman Sayısına Sahip Kullanıcılar

SELECT
    k.ad_soyad,
    COUNT(d.dokuman_id) AS yuklenen_dokuman_sayisi
FROM kullanicilar k
INNER JOIN dokumanlar d
ON k.kullanici_id = d.yukleyen_kullanici_id
GROUP BY
    k.kullanici_id,
    k.ad_soyad
HAVING COUNT(d.dokuman_id) >= 3;


-- Minimum Chunk Sayısına Sahip Dokümanlar

SELECT
    d.baslik,
    COUNT(dp.parca_id) AS parca_sayisi
FROM dokumanlar d
INNER JOIN dokuman_parcalari dp
ON d.dokuman_id = dp.dokuman_id
GROUP BY
    d.dokuman_id,
    d.baslik
HAVING COUNT(dp.parca_id) >= 10;


-- Minimum Etiket Sayısına Sahip Dokümanlar

SELECT
    d.baslik,
    COUNT(de.dokuman_etiket_id) AS etiket_sayisi
FROM dokumanlar d
INNER JOIN dokuman_etiketleri de
ON d.dokuman_id = de.dokuman_id
GROUP BY
    d.dokuman_id,
    d.baslik
HAVING COUNT(de.dokuman_etiket_id) >= 2;

-- CTE Sorguları

--Dashboard
-- Departmanlara Göre Doküman Sayısı

WITH departman_dokumanlari AS
(
    SELECT
        departman,
        COUNT(*) AS dokuman_sayisi
    FROM dokumanlar
    GROUP BY departman
)

SELECT
    departman,
    dokuman_sayisi
FROM departman_dokumanlari
ORDER BY dokuman_sayisi DESC;

-- Yönetici Paneli
-- En Çok Doküman Yükleyen Kullanıcılar

WITH kullanici_dokumanlari AS
(
    SELECT
        k.kullanici_id,
        k.ad_soyad,
        COUNT(d.dokuman_id) AS dokuman_sayisi
    FROM kullanicilar k
    LEFT JOIN dokumanlar d
        ON k.kullanici_id = d.yukleyen_kullanici_id
    GROUP BY
        k.kullanici_id,
        k.ad_soyad
)

SELECT
    ad_soyad,
    dokuman_sayisi
FROM kullanici_dokumanlari
WHERE dokuman_sayisi >= 3
ORDER BY dokuman_sayisi DESC;

-- Doküman İstatistikleri

WITH dokuman_istatistikleri AS
(
    SELECT
        d.dokuman_id,
        d.baslik,
        COUNT(dp.parca_id) AS parca_sayisi,
        SUM(dp.token_sayisi) AS toplam_token
    FROM dokumanlar d
    LEFT JOIN dokuman_parcalari dp
        ON d.dokuman_id = dp.dokuman_id
    GROUP BY
        d.dokuman_id,
        d.baslik
)

SELECT
    baslik,
    parca_sayisi,
    toplam_token
FROM dokuman_istatistikleri
WHERE parca_sayisi >= 10
ORDER BY toplam_token DESC;

-- Subquery Sorguları

-- Ortalamanın Üzerinde Chunk Sayısına Sahip Dokümanlar

SELECT
    d.dokuman_id,
    d.baslik,
    COUNT(dp.parca_id) AS parca_sayisi
FROM dokumanlar d
INNER JOIN dokuman_parcalari dp
ON d.dokuman_id = dp.dokuman_id
GROUP BY
    d.dokuman_id,
    d.baslik
HAVING COUNT(dp.parca_id) >
(
    SELECT AVG(parca_sayisi)
    FROM
    (
        SELECT
            COUNT(*) AS parca_sayisi
        FROM dokuman_parcalari
        GROUP BY dokuman_id
    ) AS ortalama
);

-- En Fazla Doküman Yükleyen Kullanıcı(lar)

SELECT
    ad_soyad
FROM kullanicilar
WHERE kullanici_id IN
(
    SELECT
        yukleyen_kullanici_id
    FROM dokumanlar
    GROUP BY yukleyen_kullanici_id
    HAVING COUNT(*) =
    (
        SELECT MAX(dokuman_sayisi)
        FROM
        (
            SELECT
                COUNT(*) AS dokuman_sayisi
            FROM dokumanlar
            GROUP BY yukleyen_kullanici_id
        ) AS maksimum
    )
);

-- Etiketi Olmayan Dokümanlar

SELECT
    dokuman_id,
    baslik
FROM dokumanlar
WHERE dokuman_id NOT IN
(
    SELECT
        dokuman_id
    FROM dokuman_etiketleri
);

-- CASE Sorguları

-- Doküman Boyutunu Chunk Sayısına Göre Sınıflandırma

SELECT
    d.baslik,
    COUNT(dp.parca_id) AS parca_sayisi,
    CASE
        WHEN COUNT(dp.parca_id) < 10 THEN 'Küçük'
        WHEN COUNT(dp.parca_id) BETWEEN 10 AND 30 THEN 'Orta'
        ELSE 'Büyük'
    END AS dokuman_boyutu
FROM dokumanlar d
LEFT JOIN dokuman_parcalari dp
ON d.dokuman_id = dp.dokuman_id
GROUP BY
    d.dokuman_id,
    d.baslik;


-- Dokümanı Toplam Token Sayısına Göre Sınıflandırma
SELECT
    d.baslik,
    SUM(dp.token_sayisi) AS toplam_token,
    CASE
        WHEN SUM(dp.token_sayisi) < 500 THEN 'Dusuk'
        WHEN SUM(dp.token_sayisi) BETWEEN 500 AND 2000 THEN 'Orta'
        ELSE 'Yuksek'
    END AS token_yogunlugu
FROM dokumanlar d
LEFT JOIN dokuman_parcalari dp
ON d.dokuman_id = dp.dokuman_id
GROUP BY
    d.dokuman_id,
    d.baslik;

-- Kullanıcıları Yüklediği Doküman Sayısına Göre Sınıflandırma

SELECT
    k.ad_soyad,
    COUNT(d.dokuman_id) AS yuklenen_dokuman_sayisi,
    CASE
        WHEN COUNT(d.dokuman_id) < 5 THEN 'Baslangic'
        WHEN COUNT(d.dokuman_id) BETWEEN 5 AND 20 THEN 'Aktif'
        ELSE 'Uzman'
    END AS kullanici_seviyesi
FROM kullanicilar k
LEFT JOIN dokumanlar d
ON k.kullanici_id = d.yukleyen_kullanici_id
GROUP BY
    k.kullanici_id,
    k.ad_soyad;

-- WINDOW FUNCTION Sorguları

-- Kullanıcıları Yüklediği Doküman Sayısına Göre Sıralama

SELECT
    k.ad_soyad,
    COUNT(d.dokuman_id) AS yuklenen_dokuman_sayisi,
    RANK() OVER (
        ORDER BY COUNT(d.dokuman_id) DESC
    ) AS kullanici_sirasi
FROM kullanicilar k
LEFT JOIN dokumanlar d
ON k.kullanici_id = d.yukleyen_kullanici_id
GROUP BY
    k.kullanici_id,
    k.ad_soyad;

-- Dokümanları Toplam Token Sayısına Göre Sıralama

SELECT
    d.baslik,
    SUM(dp.token_sayisi) AS toplam_token,
    DENSE_RANK() OVER (
        ORDER BY SUM(dp.token_sayisi) DESC
    ) AS token_sirasi
FROM dokumanlar d
LEFT JOIN dokuman_parcalari dp
ON d.dokuman_id = dp.dokuman_id
GROUP BY
    d.dokuman_id,
    d.baslik;

-- Departman Bazında Kullanıcı Sıralaması

SELECT
    k.departman,
    k.ad_soyad,
    COUNT(d.dokuman_id) AS yuklenen_dokuman_sayisi,
    ROW_NUMBER() OVER (
        PARTITION BY k.departman
        ORDER BY COUNT(d.dokuman_id) DESC
    ) AS departman_sirasi
FROM kullanicilar k
LEFT JOIN dokumanlar d
ON k.kullanici_id = d.yukleyen_kullanici_id
GROUP BY
    k.departman,
    k.kullanici_id,
    k.ad_soyad;