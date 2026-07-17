-- Kurumsal Bilgi Yönetimi tutarlı seed verileri
-- Çalıştırma sırası: 2

-- Departman seed verilerini ekler
INSERT INTO departmanlar (departman_id, departman_adi) VALUES
(1, 'Bilgi Islem'), (2, 'Muhasebe'), (4, 'Insan Kaynaklari'), (5, 'Satin Alma');

-- Kullanıcı seed verilerini ekler
INSERT INTO kullanicilar
(kullanici_id, ad_soyad, eposta, sifre_ozeti, rol, departman_id) VALUES
(1, 'Murat Aydin', 'admin@kurumsal.com', '$2b$12$admin_hash_ornegi', 'Yonetici', 1),
(2, 'Ahmet Yilmaz', 'ahmet.yilmaz@kurumsal.com', '$2b$12$ahmet_hash_ornegi', 'Personel', 4),
(3, 'Ayse Demir', 'ayse.demir@kurumsal.com', '$2b$12$ayse_hash_ornegi', 'Personel', 2),
(4, 'Mehmet Kaya', 'mehmet.kaya@kurumsal.com', '$2b$12$mehmet_hash_ornegi', 'Personel', 1),
(5, 'Zeynep Celik', 'zeynep.celik@kurumsal.com', '$2b$12$zeynep_hash_ornegi', 'Personel', 5);

-- Doküman seed verilerini ekler
INSERT INTO dokumanlar
(dokuman_id, baslik, dosya_adi, dosya_turu, yukleyen_kullanici_id, departman_id,
 surum_no, dosya_yolu, durum, dosya_boyutu) VALUES
(1, 'Personel El Kitabi', 'personel_el_kitabi.pdf', 'pdf', 2, 4, 1, '/dokumanlar/insan_kaynaklari/personel_el_kitabi.pdf', 'Aktif', 245760),
(2, 'Yillik Izin Yonetmeligi', 'yillik_izin_yonetmeligi.pdf', 'pdf', 2, 4, 1, '/dokumanlar/insan_kaynaklari/yillik_izin_yonetmeligi.pdf', 'Aktif', 184320),
(3, 'Muhasebe Surecleri', 'muhasebe_surecleri.pdf', 'pdf', 3, 2, 1, '/dokumanlar/muhasebe/muhasebe_surecleri.pdf', 'Aktif', 327680),
(4, 'Fatura Onay Proseduru', 'fatura_onay_proseduru.pdf', 'pdf', 3, 2, 1, '/dokumanlar/muhasebe/fatura_onay_proseduru.pdf', 'Aktif', 163840),
(5, 'Bilgi Guvenligi Politikasi', 'bilgi_guvenligi_politikasi.pdf', 'pdf', 4, 1, 1, '/dokumanlar/bilgi_islem/bilgi_guvenligi_politikasi.pdf', 'Aktif', 286720),
(6, 'BT Kullanim Politikasi', 'bt_kullanim_politikasi.pdf', 'pdf', 4, 1, 1, '/dokumanlar/bilgi_islem/bt_kullanim_politikasi.pdf', 'Aktif', 204800),
(7, 'Satin Alma Proseduru', 'satin_alma_proseduru.pdf', 'pdf', 5, 5, 1, '/dokumanlar/satin_alma/satin_alma_proseduru.pdf', 'Isleniyor', 225280),
(8, 'Tedarikci Degerlendirme Rehberi', 'tedarikci_degerlendirme_rehberi.pdf', 'pdf', 5, 5, 1, '/dokumanlar/satin_alma/tedarikci_degerlendirme_rehberi.pdf', 'Aktif', 194560),
(9, 'KVKK Politikasi', 'kvkk_politikasi.pdf', 'pdf', 1, 1, 1, '/dokumanlar/bilgi_islem/kvkk_politikasi.pdf', 'Arsiv', 266240),
(10, 'Acil Durum Plani', 'acil_durum_plani.pdf', 'pdf', 1, 1, 1, '/dokumanlar/bilgi_islem/acil_durum_plani.pdf', 'Arsiv', 174080);

-- Her doküman için dört metin parçası ekler; embeddingler backend tarafından üretilecektir
INSERT INTO dokuman_parcalari
(dokuman_id, parca_sirasi, parca_metni, sayfa_no, token_sayisi) VALUES
(1,1,'Şirketimize hoş geldiniz. Normal çalışma saatleri hafta içi 08:30 ile 17:30 arasındadır.',1,52),
(1,2,'Çalışanlar yıllık izin, mazeret izni ve sağlık izni haklarından yararlanabilir.',2,47),
(1,3,'Çalışanların bilgi güvenliği ve kurum etik ilkelerine uygun hareket etmesi beklenir.',3,50),
(1,4,'Kurum içi iletişimde saygılı ve profesyonel bir yaklaşım benimsenmelidir.',4,42),
(2,1,'Çalışanlar hizmet sürelerine bağlı olarak yıllık ücretli izin hakkına sahiptir.',1,41),
(2,2,'İzin talepleri en az bir hafta önceden oluşturulmalı ve yönetici tarafından onaylanmalıdır.',2,39),
(2,3,'Resmî tatiller yıllık izin süresinden düşülmez.',3,37),
(2,4,'İzin tarihleri departmanın iş yoğunluğu dikkate alınarak planlanır.',4,43),
(3,1,'Muhasebe birimi tüm mali kayıtları eksiksiz ve zamanında sisteme işler.',1,36),
(3,2,'Fatura kayıtları mevzuata uygun olarak muhasebe sistemine girilir.',2,35),
(3,3,'Ay sonu kapanışından sonra finansal raporlar yönetime sunulur.',3,32),
(3,4,'Muhasebe kayıtları düzenli olarak kontrol edilir ve hatalar düzeltilir.',4,43),
(4,1,'Tedarikçilerden gelen faturalar ilgili departman tarafından kontrol edilir.',1,34),
(4,2,'Fatura tutarları satın alma siparişiyle karşılaştırılır.',2,33),
(4,3,'Onaylanan faturalar ödeme planına dahil edilir.',3,31),
(4,4,'Eksik belgesi veya onayı bulunan faturalar ödeme sürecine alınmaz.',4,39),
(5,1,'Tüm çalışanlar güçlü parola kullanmalı ve parolalarını paylaşmamalıdır.',1,38),
(5,2,'Kurumsal verilere yalnızca yetkili kullanıcılar erişebilir.',2,37),
(5,3,'Taşınabilir belleklerdeki kurumsal veriler şifrelenmelidir.',3,35),
(5,4,'Bilgi güvenliği ihlalleri bilgi işlem birimine bildirilmelidir.',4,44),
(6,1,'Şirket bilgisayarları yalnızca iş amaçlı kullanılmalıdır.',1,34),
(6,2,'Kurumsal e-postalarda şüpheli bağlantılara tıklanmamalıdır.',2,36),
(6,3,'İnternet kullanımı bilgi güvenliği politikalarına uygun olmalıdır.',3,35),
(6,4,'Şirket cihazları gözetimsiz bırakıldığında ekran kilitlenmelidir.',4,37),
(7,1,'Satın alma talepleri sistem üzerinden oluşturularak onaya gönderilir.',1,37),
(7,2,'En az üç farklı tedarikçiden teklif alınır.',2,33),
(7,3,'Onaylanan teklif için sipariş oluşturulur ve teslim süreci izlenir.',3,32),
(7,4,'Teslim alınan ürünler sipariş bilgileriyle karşılaştırılır.',4,41),
(8,1,'Tedarikçiler kalite, teslim süresi ve maliyete göre değerlendirilir.',1,34),
(8,2,'Düşük performanslı tedarikçiler için iyileştirme planı hazırlanır.',2,37),
(8,3,'Değerlendirme sonuçları yıllık raporlarda saklanır.',3,34),
(8,4,'Başarılı tedarikçiler öncelikli tedarikçi olarak değerlendirilebilir.',4,41),
(9,1,'Kişisel veriler yalnızca belirlenen amaçlar doğrultusunda işlenebilir.',1,40),
(9,2,'Kişisel verilere yalnızca yetkili personel erişebilir.',2,38),
(9,3,'Saklama süresi dolan kişisel veriler güvenli şekilde silinir.',3,39),
(9,4,'Kişisel veri ihlalleri ilgili birimlere bildirilmelidir.',4,41),
(10,1,'Yangında en yakın acil çıkış kullanılarak toplanma alanına gidilmelidir.',1,36),
(10,2,'Deprem sırasında güvenli bir noktada sarsıntının bitmesi beklenmelidir.',2,37),
(10,3,'Çalışanlar acil durum ekiplerinin talimatlarına uymalıdır.',3,35),
(10,4,'Yetkililer izin vermeden çalışma alanına geri dönülmemelidir.',4,42);

-- Doküman etiketlerini ekler
INSERT INTO dokuman_etiketleri (dokuman_id, etiket_adi) VALUES
(1,'Personel'),(1,'IK'),(1,'Calisma'),(2,'Izin'),(2,'IK'),(2,'Yonetmelik'),
(3,'Muhasebe'),(3,'Finans'),(3,'Raporlama'),(4,'Fatura'),(4,'Onay'),(4,'Muhasebe'),
(5,'Guvenlik'),(5,'Siber Guvenlik'),(5,'Parola'),(6,'BT'),(6,'Eposta'),(6,'Internet'),
(7,'Satin Alma'),(7,'Tedarik'),(7,'Siparis'),(8,'Tedarikci'),(8,'Degerlendirme'),(8,'Performans'),
(9,'KVKK'),(9,'Kisisel Veri'),(9,'Gizlilik'),(10,'Acil Durum'),(10,'Yangin'),(10,'Deprem');

-- Dokümanları kendi departmanlarına yetkilendirir
INSERT INTO dokuman_yetkileri (dokuman_id, departman_id, goruntuleyebilir_mi) VALUES
(1,4,TRUE),(2,4,TRUE),(3,2,TRUE),(4,2,TRUE),(5,1,TRUE),
(6,1,TRUE),(7,5,TRUE),(8,5,TRUE),(9,1,TRUE),(10,1,TRUE);

-- Beş sohbet oturumu ekler
INSERT INTO sohbet_oturumlari (oturum_id, kullanici_id, oturum_basligi) VALUES
(1,1,'Bilgi Guvenligi Hakkinda'),(2,1,'KVKK Sorulari'),
(3,2,'Personel El Kitabi'),(4,3,'Muhasebe Surecleri'),(5,5,'Satin Alma Proseduru');

-- Her oturuma dört mesaj ekler
INSERT INTO sohbet_mesajlari (mesaj_id, oturum_id, gonderen_tipi, mesaj_metni) VALUES
(1,1,'Kullanici','Guclu parola nasil olusturulmalidir?'),
(2,1,'AI','Parolalar buyuk ve kucuk harf, rakam ve ozel karakter icermelidir.'),
(3,1,'Kullanici','Parolami ne siklikla degistirmeliyim?'),
(4,1,'AI','Parolalar duzenli araliklarla degistirilmelidir.'),
(5,2,'Kullanici','Kisisel veriler ne kadar sure saklanir?'),
(6,2,'AI','Saklama suresi dolan veriler guvenli sekilde silinir veya anonimlestirilir.'),
(7,2,'Kullanici','Verilere kimler erisebilir?'),
(8,2,'AI','Yalnizca yetkilendirilmis personel kisisel verilere erisebilir.'),
(9,3,'Kullanici','Calisma saatleri nedir?'),
(10,3,'AI','Calisma saatleri hafta ici 08:30 ile 17:30 arasindadir.'),
(11,3,'Kullanici','Izin basvurusu nasil yapilir?'),
(12,3,'AI','Izin talebi sistemden olusturularak yonetici onayina gonderilir.'),
(13,4,'Kullanici','Faturalar nasil onaylanir?'),
(14,4,'AI','Faturalar ilgili departman tarafindan kontrol edilerek sisteme aktarilir.'),
(15,4,'Kullanici','Ay sonu raporlari ne zaman hazirlanir?'),
(16,4,'AI','Finansal raporlar ay sonu kapanis islemlerinden sonra hazirlanir.'),
(17,5,'Kullanici','Satin alma sureci nasil baslar?'),
(18,5,'AI','Satin alma talepleri sistemde olusturularak onaya gonderilir.'),
(19,5,'Kullanici','Kac teklif alinmalidir?'),
(20,5,'AI','En az uc farkli tedarikciden teklif alinmalidir.');

-- AI mesajlarının kaynak doküman parçalarını ekler
INSERT INTO mesaj_kaynaklari (mesaj_id, parca_id, benzerlik_puani)
SELECT v.mesaj_id, dp.parca_id, v.benzerlik_puani
FROM (VALUES
 (2,5,1,0.94),(4,5,1,0.89),(6,9,3,0.96),(8,9,2,0.95),(10,1,1,0.98),
 (12,1,2,0.97),(14,4,1,0.93),(16,3,3,0.96),(18,7,1,0.97),(20,7,2,0.95)
) AS v(mesaj_id,dokuman_id,parca_sirasi,benzerlik_puani)
INNER JOIN dokuman_parcalari dp
    ON dp.dokuman_id = v.dokuman_id AND dp.parca_sirasi = v.parca_sirasi;

-- Açık kimliklerle eklenen seedlerden sonra sequence değerlerini eşitler
SELECT setval(pg_get_serial_sequence('departmanlar','departman_id'), MAX(departman_id)) FROM departmanlar;
SELECT setval(pg_get_serial_sequence('kullanicilar','kullanici_id'), MAX(kullanici_id)) FROM kullanicilar;
SELECT setval(pg_get_serial_sequence('dokumanlar','dokuman_id'), MAX(dokuman_id)) FROM dokumanlar;
SELECT setval(pg_get_serial_sequence('sohbet_oturumlari','oturum_id'), MAX(oturum_id)) FROM sohbet_oturumlari;
SELECT setval(pg_get_serial_sequence('sohbet_mesajlari','mesaj_id'), MAX(mesaj_id)) FROM sohbet_mesajlari;