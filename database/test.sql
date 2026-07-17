-- Kurumsal Bilgi Yönetimi doğrulama ve kısıt testleri
-- Çalıştırma sırası: 3

-- Tablo başına kayıt sayılarını doğrular
SELECT 'departmanlar' AS tablo_adi, COUNT(*) AS kayit_sayisi FROM departmanlar
UNION ALL SELECT 'kullanicilar', COUNT(*) FROM kullanicilar
UNION ALL SELECT 'dokumanlar', COUNT(*) FROM dokumanlar
UNION ALL SELECT 'dokuman_parcalari', COUNT(*) FROM dokuman_parcalari
UNION ALL SELECT 'dokuman_etiketleri', COUNT(*) FROM dokuman_etiketleri
UNION ALL SELECT 'dokuman_yetkileri', COUNT(*) FROM dokuman_yetkileri
UNION ALL SELECT 'sohbet_oturumlari', COUNT(*) FROM sohbet_oturumlari
UNION ALL SELECT 'sohbet_mesajlari', COUNT(*) FROM sohbet_mesajlari
UNION ALL SELECT 'mesaj_kaynaklari', COUNT(*) FROM mesaj_kaynaklari
ORDER BY tablo_adi;

-- Her dokümanda dört parça bulunduğunu doğrular
SELECT dokuman_id, COUNT(*) AS parca_sayisi
FROM dokuman_parcalari
GROUP BY dokuman_id
ORDER BY dokuman_id;

-- Embedding üretim durumunu gösterir
SELECT d.dokuman_id, d.baslik,
       COUNT(dp.parca_id) AS toplam_parca,
       COUNT(dp.embedding) AS embedding_olusturulan_parca,
       COUNT(dp.parca_id) - COUNT(dp.embedding) AS eksik_embedding
FROM dokumanlar d
LEFT JOIN dokuman_parcalari dp ON d.dokuman_id = dp.dokuman_id
GROUP BY d.dokuman_id, d.baslik
ORDER BY d.dokuman_id;

-- Ayşe Demir'in görebildiği dokümanları listeler
SELECT d.dokuman_id, d.baslik, dep.departman_adi, d.durum,
       CASE
           WHEN d.yukleyen_kullanici_id = k.kullanici_id THEN 'Yukledigi dokuman'
           WHEN d.departman_id = k.departman_id THEN 'Kendi departmani'
           ELSE 'Yonetici yetkisi'
       END AS erisim_nedeni
FROM kullanicilar k
INNER JOIN fn_kullanicinin_gorebildigi_dokumanlar(k.kullanici_id) d ON TRUE
INNER JOIN departmanlar dep ON d.departman_id = dep.departman_id
WHERE k.eposta = 'ayse.demir@kurumsal.com'
ORDER BY d.dokuman_id;

-- Dördüncü oturumun mesajlarını ve kaynaklarını birlikte gösterir
SELECT so.oturum_id, so.oturum_basligi, sm.mesaj_id, sm.gonderen_tipi,
       sm.mesaj_metni, d.baslik AS kaynak_dokuman, dp.parca_sirasi,
       dp.parca_metni AS kaynak_metni, mk.benzerlik_puani
FROM sohbet_oturumlari so
INNER JOIN sohbet_mesajlari sm ON so.oturum_id = sm.oturum_id
LEFT JOIN mesaj_kaynaklari mk ON sm.mesaj_id = mk.mesaj_id
LEFT JOIN dokuman_parcalari dp ON mk.parca_id = dp.parca_id
LEFT JOIN dokumanlar d ON dp.dokuman_id = d.dokuman_id
WHERE so.oturum_id = 4
ORDER BY sm.mesaj_id, mk.benzerlik_puani DESC;

-- View ve fonksiyon sonuçlarını doğrular
SELECT * FROM vw_aktif_dokumanlar ORDER BY dokuman_id;
SELECT * FROM vw_dokuman_ozeti ORDER BY dokuman_id;
SELECT * FROM vw_sohbet_ozeti ORDER BY oturum_id;
SELECT * FROM vw_dokuman_istatistikleri ORDER BY dokuman_id;
SELECT fn_chunk_sayisi(1) AS dokuman_1_parca_sayisi;
SELECT fn_token_sayisi(1) AS dokuman_1_token_sayisi;

-- Aşağıdaki bloklar hatalı verilerin kısıtlar tarafından reddedildiğini test eder
DO $$
BEGIN
    INSERT INTO kullanicilar(ad_soyad,eposta,sifre_ozeti,rol,departman_id)
    VALUES ('Test Kullanici','test.rol@kurumsal.com','test_hash','Editor',1);
    RAISE EXCEPTION 'Rol CHECK testi başarısız: kayıt kabul edildi';
EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'Rol CHECK testi başarılı';
END $$;

DO $$
BEGIN
    INSERT INTO dokumanlar
    (baslik,dosya_adi,dosya_turu,yukleyen_kullanici_id,departman_id,surum_no,dosya_yolu,durum,dosya_boyutu)
    VALUES ('Durum Testi','durum.pdf','pdf',1,1,1,'/test/durum.pdf','Silindi',1024);
    RAISE EXCEPTION 'Durum CHECK testi başarısız: kayıt kabul edildi';
EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'Durum CHECK testi başarılı';
END $$;

DO $$
BEGIN
    INSERT INTO dokumanlar
    (baslik,dosya_adi,dosya_turu,yukleyen_kullanici_id,departman_id,surum_no,dosya_yolu,durum,dosya_boyutu)
    VALUES ('Boyut Testi','boyut.pdf','pdf',1,1,1,'/test/boyut.pdf','Isleniyor',-100);
    RAISE EXCEPTION 'Dosya boyutu CHECK testi başarısız: kayıt kabul edildi';
EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'Dosya boyutu CHECK testi başarılı';
END $$;

DO $$
BEGIN
    INSERT INTO sohbet_mesajlari(oturum_id,gonderen_tipi,mesaj_metni)
    VALUES (1,'Sistem','Gönderen tipi testi');
    RAISE EXCEPTION 'Gönderen tipi CHECK testi başarısız: kayıt kabul edildi';
EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'Gönderen tipi CHECK testi başarılı';
END $$;

DO $$
BEGIN
    INSERT INTO mesaj_kaynaklari(mesaj_id,parca_id,benzerlik_puani)
    VALUES (2,2,1.50);
    RAISE EXCEPTION 'Benzerlik CHECK testi başarısız: kayıt kabul edildi';
EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'Benzerlik CHECK testi başarılı';
END $$;

DO $$
BEGIN
    INSERT INTO kullanicilar(ad_soyad,eposta,sifre_ozeti,rol,departman_id)
    VALUES ('FK Test','test.fk@kurumsal.com','test_hash','Personel',9999);
    RAISE EXCEPTION 'Foreign key testi başarısız: kayıt kabul edildi';
EXCEPTION WHEN foreign_key_violation THEN
    RAISE NOTICE 'Foreign key testi başarılı';
END $$;

DO $$
BEGIN
    INSERT INTO kullanicilar(ad_soyad,eposta,sifre_ozeti,rol,departman_id)
    VALUES ('Tekrar Kullanici','admin@kurumsal.com','test_hash','Personel',1);
    RAISE EXCEPTION 'UNIQUE testi başarısız: kayıt kabul edildi';
EXCEPTION WHEN unique_violation THEN
    RAISE NOTICE 'E-posta UNIQUE testi başarılı';
END $$;

DO $$
BEGIN
    UPDATE dokuman_parcalari SET embedding = '[0.1,0.2,0.3]'::vector WHERE parca_id = 1;
    RAISE EXCEPTION 'Vektör boyutu testi başarısız: kayıt kabul edildi';
EXCEPTION WHEN data_exception THEN
    RAISE NOTICE 'vector(1536) boyut testi başarılı: %', SQLERRM;
END $$;