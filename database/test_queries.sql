-- Test Aşaması

SELECT *
FROM vw_dokuman_ozetleri;

SELECT table_name
FROM information_schema.views
WHERE table_schema = 'public';

SELECT *
FROM vw_dokuman_ozeti;

SELECT *
FROM vw_sohbet_ozeti;

SELECT *
FROM vw_dokuman_istatistikleri;

SELECT *
FROM vw_aktif_dokumanlar;

SELECT
    routine_name
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_type = 'FUNCTION'
ORDER BY routine_name;

SELECT
    routine_name,
    data_type
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_type = 'FUNCTION'
AND routine_name LIKE 'fn_%';

SELECT
    p.proname AS function_name,
    pg_get_function_identity_arguments(p.oid) AS parameters
FROM pg_proc p
JOIN pg_namespace n
ON p.pronamespace = n.oid
WHERE n.nspname = 'public'
AND p.proname LIKE 'fn_%'
ORDER BY p.proname;

SELECT fn_chunk_sayisi(1);

SELECT fn_token_sayisi(1);

SELECT fn_dokuman_etiket_sayisi(1);

SELECT fn_kullanici_dokuman_sayisi(1);

SELECT fn_sohbet_mesaj_sayisi(1);

SELECT
    yukleyen_kullanici_id,
    COUNT(*) AS dokuman_sayisi
FROM dokumanlar
GROUP BY yukleyen_kullanici_id
ORDER BY yukleyen_kullanici_id;

SELECT
    routine_name
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_type = 'PROCEDURE'
ORDER BY routine_name;

SELECT
    dokuman_id,
    baslik,
    durum
FROM dokumanlar
WHERE dokuman_id = 1;

CALL sp_dokuman_arsivle(1);

SELECT
    dokuman_id,
    baslik,
    durum
FROM dokumanlar
WHERE dokuman_id = 1;

SELECT *
FROM vw_aktif_dokumanlar;

CALL sp_dokuman_geri_aktiflestir(1);

SELECT
    dokuman_id,
    baslik,
    durum
FROM dokumanlar
WHERE dokuman_id = 1;

SELECT *
FROM vw_aktif_dokumanlar;

SELECT
    k.ad_soyad,
    d.baslik,
    d.departman
FROM kullanicilar k
INNER JOIN dokumanlar d
ON k.kullanici_id = d.yukleyen_kullanici_id;

SELECT
    d.baslik,
    dp.parca_sirasi,
    dp.token_sayisi
FROM dokumanlar d
INNER JOIN dokuman_parcalari dp
ON d.dokuman_id = dp.dokuman_id;

SELECT
    d.baslik,
    de.etiket_adi
FROM dokumanlar d
INNER JOIN dokuman_etiketleri de
ON d.dokuman_id = de.dokuman_id;

SELECT
    so.oturum_basligi,
    sm.gonderen_tipi,
    sm.mesaj_metni
FROM sohbet_oturumlari so
INNER JOIN sohbet_mesajlari sm
ON so.oturum_id = sm.oturum_id;

SELECT
    d.baslik,
    de.etiket_adi
FROM dokumanlar d
LEFT JOIN dokuman_etiketleri de
ON d.dokuman_id = de.dokuman_id;

SELECT
    so.oturum_basligi,
    sm.mesaj_metni
FROM sohbet_oturumlari so
LEFT JOIN sohbet_mesajlari sm
ON so.oturum_id = sm.oturum_id;

SELECT
    departman,
    COUNT(*) AS dokuman_sayisi
FROM dokumanlar
GROUP BY departman;

SELECT
    dosya_turu,
    COUNT(*) AS dokuman_sayisi
FROM dokumanlar
GROUP BY dosya_turu;

SELECT
    k.ad_soyad,
    COUNT(d.dokuman_id) AS yuklenen_dokuman_sayisi
FROM kullanicilar k
LEFT JOIN dokumanlar d
ON k.kullanici_id = d.yukleyen_kullanici_id
GROUP BY
    k.kullanici_id,
    k.ad_soyad;


SELECT
    k.ad_soyad,
    COUNT(d.dokuman_id) AS yuklenen_dokuman_sayisi
FROM kullanicilar k
INNER JOIN dokumanlar d
ON k.kullanici_id = d.yukleyen_kullanici_id
GROUP BY
    k.kullanici_id,
    k.ad_soyad
HAVING COUNT(d.dokuman_id) >= 2;

SELECT
    d.baslik,
    COUNT(dp.parca_id) AS parca_sayisi
FROM dokumanlar d
INNER JOIN dokuman_parcalari dp
ON d.dokuman_id = dp.dokuman_id
GROUP BY
    d.dokuman_id,
    d.baslik
HAVING COUNT(dp.parca_id) >= 3;

SELECT
    d.baslik,
    COUNT(de.dokuman_etiket_id) AS etiket_sayisi
FROM dokumanlar d
INNER JOIN dokuman_etiketleri de
ON d.dokuman_id = de.dokuman_id
GROUP BY
    d.dokuman_id,
    d.baslik
HAVING COUNT(de.dokuman_etiket_id) >= 3;

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
WHERE dokuman_sayisi >= 2
ORDER BY dokuman_sayisi DESC;

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
ORDER BY toplam_token DESC;
