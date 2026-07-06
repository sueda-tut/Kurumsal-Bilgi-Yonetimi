
-- Kullanıcı Seed Verileri

INSERT INTO kullanicilar
(
    ad_soyad,
    eposta,
    sifre_ozeti,
    rol,
    departman
)
VALUES
(
    'Sistem Yoneticisi',
    'admin@kurumsal.com',
    '$2b$12$admin_hash_ornegi',
    'Yonetici',
    'Bilgi Islem'
),
(
    'Ahmet Yilmaz',
    'ahmet.yilmaz@kurumsal.com',
    '$2b$12$ahmet_hash_ornegi',
    'Personel',
    'Insan Kaynaklari'
),
(
    'Ayse Demir',
    'ayse.demir@kurumsal.com',
    '$2b$12$ayse_hash_ornegi',
    'Personel',
    'Muhasebe'
),
(
    'Mehmet Kaya',
    'mehmet.kaya@kurumsal.com',
    '$2b$12$mehmet_hash_ornegi',
    'Personel',
    'Bilgi Islem'
),
(
    'Zeynep Celik',
    'zeynep.celik@kurumsal.com',
    '$2b$12$zeynep_hash_ornegi',
    'Personel',
    'Satin Alma'
);

ALTER TABLE kullanicilar
DROP CONSTRAINT chk_kullanicilar_rol;

ALTER TABLE kullanicilar
ADD CONSTRAINT chk_kullanicilar_rol
CHECK (rol IN ('Yonetici', 'Personel'));

-- Doküman Seed Verileri

INSERT INTO dokumanlar
(
    baslik,
    dosya_adi,
    dosya_turu,
    yukleyen_kullanici_id,
    yuklenme_tarihi,
    departman,
    surum_no,
    dosya_yolu,
    durum
)
VALUES
(
    'Personel El Kitabi',
    'personel_el_kitabi.pdf',
    'pdf',
    2,
    CURRENT_TIMESTAMP,
    'IK',
    1,
    '/dokumanlar/ik/personel_el_kitabi.pdf',
    'Aktif'
),
(
    'Yillik Izin Yonetmeligi',
    'yillik_izin_yonetmeligi.pdf',
    'pdf',
    2,
    CURRENT_TIMESTAMP,
    'IK',
    1,
    '/dokumanlar/ik/yillik_izin_yonetmeligi.pdf',
    'Aktif'
),
(
    'Muhasebe Surecleri',
    'muhasebe_surecleri.pdf',
    'pdf',
    3,
    CURRENT_TIMESTAMP,
    'Muhasebe',
    1,
    '/dokumanlar/muhasebe/muhasebe_surecleri.pdf',
    'Aktif'
),
(
    'Fatura Onay Proseduru',
    'fatura_onay_proseduru.pdf',
    'pdf',
    3,
    CURRENT_TIMESTAMP,
    'Muhasebe',
    1,
    '/dokumanlar/muhasebe/fatura_onay_proseduru.pdf',
    'Aktif'
),
(
    'Bilgi Guvenligi Politikasi',
    'bilgi_guvenligi_politikasi.pdf',
    'pdf',
    4,
    CURRENT_TIMESTAMP,
    'Bilgi Islem',
    1,
    '/dokumanlar/bilgi_islem/bilgi_guvenligi_politikasi.pdf',
    'Aktif'
),
(
    'BT Kullanim Politikasi',
    'bt_kullanim_politikasi.pdf',
    'pdf',
    4,
    CURRENT_TIMESTAMP,
    'Bilgi Islem',
    1,
    '/dokumanlar/bilgi_islem/bt_kullanim_politikasi.pdf',
    'Aktif'
),
(
    'Satin Alma Proseduru',
    'satin_alma_proseduru.pdf',
    'pdf',
    5,
    CURRENT_TIMESTAMP,
    'Satin Alma',
    1,
    '/dokumanlar/satin_alma/satin_alma_proseduru.pdf',
    'Isleniyor'
),
(
    'Tedarikci Degerlendirme Rehberi',
    'tedarikci_degerlendirme_rehberi.pdf',
    'pdf',
    5,
    CURRENT_TIMESTAMP,
    'Satin Alma',
    1,
    '/dokumanlar/satin_alma/tedarikci_degerlendirme_rehberi.pdf',
    'Aktif'
),
(
    'KVKK Politikasi',
    'kvkk_politikasi.pdf',
    'pdf',
    1,
    CURRENT_TIMESTAMP,
    'Bilgi Islem',
    1,
    '/dokumanlar/bilgi_islem/kvkk_politikasi.pdf',
    'Arsivlendi'
),
(
    'Acil Durum Plani',
    'acil_durum_plani.pdf',
    'pdf',
    1,
    CURRENT_TIMESTAMP,
    'Bilgi Islem',
    1,
    '/dokumanlar/bilgi_islem/acil_durum_plani.pdf',
    'Arsivlendi'
);

TRUNCATE TABLE kullanicilar RESTART IDENTITY CASCADE;

-- Doküman Parçaları Seed Verileri

INSERT INTO dokuman_parcalari
(
    dokuman_id,
    parca_sirasi,
    parca_metni,
    sayfa_no,
    token_sayisi,
    embedding_id
)
VALUES
(
    1,
    1,
    'Şirketimize hoş geldiniz. Bu el kitabı çalışanların işe uyum sürecini kolaylaştırmak amacıyla hazırlanmıştır. Çalışma saatleri hafta içi 08:30 ile 17:30 arasındadır. Çalışanların mesai başlangıç ve bitiş saatlerine uyması beklenmektedir.',
    1,
    42,
    'emb_doc1_chunk1'
),
(
    1,
    2,
    'Çalışanlar yıllık izin, mazeret izni ve sağlık izni haklarından şirket politikaları doğrultusunda yararlanabilir. İzin talepleri şirketin izin yönetim sistemi üzerinden yöneticinin onayına sunulmalıdır.',
    2,
    35,
    'emb_doc1_chunk2'
),
(
    1,
    3,
    'Şirket kurallarına aykırı davranışlar disiplin süreci kapsamında değerlendirilir. Tüm çalışanların bilgi güvenliği kurallarına uyması, şirket ekipmanlarını yalnızca iş amaçlı kullanması ve kurum etik ilkelerine bağlı kalması beklenmektedir.',
    3,
    39,
    'emb_doc1_chunk3'
);

TRUNCATE TABLE dokuman_parcalari RESTART IDENTITY;

-- Doküman Parçaları Seed Verileri

INSERT INTO dokuman_parcalari
(
    dokuman_id,
    parca_sirasi,
    parca_metni,
    sayfa_no,
    token_sayisi,
    embedding_id
)
VALUES
(
    1,
    1,
    'Şirketimize hoş geldiniz. Bu personel el kitabı çalışanların kuruma uyum sağlamasını kolaylaştırmak amacıyla hazırlanmıştır. Normal çalışma saatleri hafta içi 08:30 ile 17:30 arasındadır. Çalışanların mesai başlangıç ve bitiş saatlerine uyması beklenmektedir.',
    1,
    52,
    'emb_doc1_chunk1'
),
(
    1,
    2,
    'Çalışanlar yıllık izin, mazeret izni ve sağlık izni haklarından şirket politikalarına uygun olarak yararlanabilir. İzin talepleri kurumun izin yönetim sistemi üzerinden oluşturulmalı ve ilgili yönetici tarafından onaylandıktan sonra kullanılmalıdır.',
    2,
    47,
    'emb_doc1_chunk2'
),
(
    1,
    3,
    'Şirket kurallarına aykırı davranışlar disiplin süreci kapsamında değerlendirilir. Tüm çalışanların bilgi güvenliği kurallarına uyması, şirket ekipmanlarını yalnızca iş amaçlı kullanması ve kurumun etik ilkelerine uygun hareket etmesi beklenmektedir.',
    3,
    50,
    'emb_doc1_chunk3'
);

INSERT INTO dokuman_parcalari
(
    dokuman_id,
    parca_sirasi,
    parca_metni,
    sayfa_no,
    token_sayisi,
    embedding_id
)
VALUES

-- Doküman 2 - Yillik Izin Yonetmeligi

(
    2,
    1,
    'Çalışanlar hizmet sürelerine bağlı olarak yıllık ücretli izin hakkına sahiptir. Yıllık izin süresi yürürlükteki iş kanunu ve şirket politikaları doğrultusunda belirlenmektedir.',
    1,
    41,
    'emb_doc2_chunk1'
),
(
    2,
    2,
    'Yıllık izin talepleri en az bir hafta önceden sistem üzerinden oluşturulmalı ve ilgili yönetici tarafından onaylanmalıdır. Onaylanmayan izinler kullanılamaz.',
    2,
    39,
    'emb_doc2_chunk2'
),
(
    2,
    3,
    'Resmî tatiller yıllık izin süresinden düşülmez. Kullanılmayan izin hakları şirket politikalarına uygun olarak sonraki döneme devredilebilir.',
    3,
    37,
    'emb_doc2_chunk3'
),

-- Doküman 3 - Muhasebe Surecleri

(
    3,
    1,
    'Muhasebe birimi tüm mali kayıtları eksiksiz ve zamanında sisteme işlemekle sorumludur. Belgeler elektronik ortamda arşivlenmelidir.',
    1,
    36,
    'emb_doc3_chunk1'
),
(
    3,
    2,
    'Fatura kayıtları ilgili mevzuata uygun olarak muhasebe sistemine girilir ve gerekli kontroller tamamlandıktan sonra onaylanır.',
    2,
    35,
    'emb_doc3_chunk2'
),
(
    3,
    3,
    'Ay sonu kapanış işlemleri tamamlandıktan sonra finansal raporlar hazırlanarak yönetime sunulur.',
    3,
    32,
    'emb_doc3_chunk3'
),

-- Doküman 4 - Fatura Onay Proseduru

(
    4,
    1,
    'Tedarikçilerden gelen faturalar öncelikle ilgili departman tarafından kontrol edilir ve sisteme yüklenir.',
    1,
    34,
    'emb_doc4_chunk1'
),
(
    4,
    2,
    'Fatura tutarları satın alma siparişi ile karşılaştırılır. Uyuşmazlık olması durumunda işlem durdurulur.',
    2,
    33,
    'emb_doc4_chunk2'
),
(
    4,
    3,
    'Onaylanan faturalar muhasebe sistemine aktarılır ve ödeme planına dahil edilir.',
    3,
    31,
    'emb_doc4_chunk3'
),

-- Doküman 5 - Bilgi Guvenligi Politikasi

(
    5,
    1,
    'Tüm çalışanlar güçlü parola kullanmalı ve parolalarını üçüncü kişilerle paylaşmamalıdır. Parolalar düzenli aralıklarla değiştirilmelidir.',
    1,
    38,
    'emb_doc5_chunk1'
),
(
    5,
    2,
    'Kurumsal veriler yalnızca yetkili kullanıcılar tarafından erişilebilir. Yetkisiz erişim girişimleri kayıt altına alınmaktadır.',
    2,
    37,
    'emb_doc5_chunk2'
),
(
    5,
    3,
    'Taşınabilir bellek kullanımı şirket politikalarına uygun olmalı ve gerekli durumlarda veriler şifrelenmelidir.',
    3,
    35,
    'emb_doc5_chunk3'
),

-- Doküman 6 - BT Kullanim Politikasi

(
    6,
    1,
    'Şirket bilgisayarları yalnızca iş amaçlı kullanılmalıdır. Lisanssız yazılım kurulmasına izin verilmez.',
    1,
    34,
    'emb_doc6_chunk1'
),
(
    6,
    2,
    'Kurumsal e-posta hesapları güvenli iletişim amacıyla kullanılmalı ve şüpheli bağlantılara tıklanmamalıdır.',
    2,
    36,
    'emb_doc6_chunk2'
),
(
    6,
    3,
    'İnternet kullanımı şirket politikalarına uygun olmalı ve bilgi güvenliğini riske atacak işlemlerden kaçınılmalıdır.',
    3,
    35,
    'emb_doc6_chunk3'
),

-- Doküman 7 - Satin Alma Proseduru

(
    7,
    1,
    'Satın alma talepleri ilgili birim tarafından sistem üzerinden oluşturulur ve gerekli onay sürecine gönderilir.',
    1,
    37,
    'emb_doc7_chunk1'
),
(
    7,
    2,
    'En az üç farklı tedarikçiden teklif alınarak fiyat ve kalite değerlendirmesi yapılır.',
    2,
    33,
    'emb_doc7_chunk2'
),
(
    7,
    3,
    'Onaylanan teklifler doğrultusunda sipariş oluşturulur ve teslim süreci takip edilir.',
    3,
    32,
    'emb_doc7_chunk3'
),

-- Doküman 8 - Tedarikci Degerlendirme Rehberi

(
    8,
    1,
    'Tedarikçiler kalite, teslim süresi ve maliyet kriterlerine göre düzenli olarak değerlendirilmektedir.',
    1,
    34,
    'emb_doc8_chunk1'
),
(
    8,
    2,
    'Performans puanı düşük olan tedarikçiler için iyileştirme planı hazırlanır veya alternatif firma araştırılır.',
    2,
    37,
    'emb_doc8_chunk2'
),
(
    8,
    3,
    'Değerlendirme sonuçları yıllık raporlarda saklanır ve satın alma yönetimi tarafından incelenir.',
    3,
    34,
    'emb_doc8_chunk3'
),

-- Doküman 9 - KVKK Politikasi

(
    9,
    1,
    'Kişisel veriler yalnızca belirlenen amaçlar doğrultusunda işlenebilir ve ilgili mevzuata uygun şekilde korunmalıdır.',
    1,
    40,
    'emb_doc9_chunk1'
),
(
    9,
    2,
    'Kişisel verilere yalnızca yetkili personel erişebilir. Erişim kayıtları düzenli olarak denetlenmektedir.',
    2,
    38,
    'emb_doc9_chunk2'
),
(
    9,
    3,
    'Saklama süresi dolan kişisel veriler güvenli yöntemlerle silinir, yok edilir veya anonim hale getirilir.',
    3,
    39,
    'emb_doc9_chunk3'
),

-- Doküman 10 - Acil Durum Plani

(
    10,
    1,
    'Yangın durumunda çalışanlar en yakın acil çıkış kapısını kullanarak belirlenen toplanma alanına gitmelidir.',
    1,
    36,
    'emb_doc10_chunk1'
),
(
    10,
    2,
    'Deprem sırasında güvenli bir noktada yaşam üçgeni oluşturulmalı ve sarsıntı sona erene kadar beklenmelidir.',
    2,
    37,
    'emb_doc10_chunk2'
),
(
    10,
    3,
    'Acil durum ekipleri olay yerine ulaşıncaya kadar çalışanlar panik yapmadan güvenlik talimatlarına uymalıdır.',
    3,
    35,
    'emb_doc10_chunk3'
);

-- Doküman Etiketleri Seed Verileri

INSERT INTO dokuman_etiketleri
(
    dokuman_id,
    etiket_adi
)
VALUES
(1, 'Personel'),
(1, 'IK'),
(1, 'Calisma'),

(2, 'Izin'),
(2, 'IK'),
(2, 'Yonetmelik'),

(3, 'Muhasebe'),
(3, 'Finans'),
(3, 'Raporlama'),

(4, 'Fatura'),
(4, 'Onay'),
(4, 'Muhasebe'),

(5, 'Guvenlik'),
(5, 'Siber Guvenlik'),
(5, 'Parola'),

(6, 'BT'),
(6, 'Eposta'),
(6, 'Internet'),

(7, 'Satin Alma'),
(7, 'Tedarik'),
(7, 'Siparis'),

(8, 'Tedarikci'),
(8, 'Degerlendirme'),
(8, 'Performans'),

(9, 'KVKK'),
(9, 'Kisisel Veri'),
(9, 'Gizlilik'),

(10, 'Acil Durum'),
(10, 'Yangin'),
(10, 'Deprem');

-- Doküman Yetkileri Seed Verileri

INSERT INTO dokuman_yetkileri
(
    dokuman_id,
    rol_adi,
    goruntuleyebilir_mi
)
VALUES
(1, 'Personel', TRUE),
(1, 'Yonetici', TRUE),

(2, 'Personel', TRUE),
(2, 'Yonetici', TRUE),

(3, 'Yonetici', TRUE),
(3, 'Personel', FALSE),

(4, 'Yonetici', TRUE),
(4, 'Personel', FALSE),

(5, 'Personel', TRUE),
(5, 'Yonetici', TRUE),

(6, 'Personel', TRUE),
(6, 'Yonetici', TRUE),

(7, 'Personel', TRUE),
(7, 'Yonetici', TRUE),

(8, 'Personel', TRUE),
(8, 'Yonetici', TRUE),

(9, 'Personel', TRUE),
(9, 'Yonetici', TRUE),

(10, 'Personel', TRUE),
(10, 'Yonetici', TRUE);

-- Sohbet Oturumları Seed Verileri

INSERT INTO sohbet_oturumlari
(
    kullanici_id,
    oturum_basligi,
    baslangic_tarihi
)
VALUES
(
    1,
    'Bilgi Guvenligi Hakkinda',
    CURRENT_TIMESTAMP
),
(
    1,
    'KVKK Sorulari',
    CURRENT_TIMESTAMP
),
(
    2,
    'Personel El Kitabi',
    CURRENT_TIMESTAMP
),
(
    3,
    'Muhasebe Surecleri',
    CURRENT_TIMESTAMP
),
(
    4,
    'Satin Alma Proseduru',
    CURRENT_TIMESTAMP
),
(
    5,
    'Acil Durum Plani',
    CURRENT_TIMESTAMP
);

-- Sohbet Mesajları Seed Verileri

INSERT INTO sohbet_mesajlari
(
    oturum_id,
    gonderen_tipi,
    mesaj_metni,
    olusturulma_tarihi
)
VALUES

-- Oturum 1
(1,'Kullanici','Guclu parola nasil olusturulmalidir?',CURRENT_TIMESTAMP),
(1,'Yapay Zeka','Bilgi Guvenligi Politikasina gore parolalar buyuk ve kucuk harf, rakam ve ozel karakter icermelidir.',CURRENT_TIMESTAMP),
(1,'Kullanici','Parolami ne siklikla degistirmeliyim?',CURRENT_TIMESTAMP),
(1,'Yapay Zeka','Sirket politikasi geregi parolalar duzenli araliklarla degistirilmelidir.',CURRENT_TIMESTAMP),

-- Oturum 2
(2,'Kullanici','Kisisel veriler ne kadar sure saklanir?',CURRENT_TIMESTAMP),
(2,'Yapay Zeka','KVKK Politikasina gore saklama suresi dolan veriler guvenli sekilde silinir veya anonim hale getirilir.',CURRENT_TIMESTAMP),
(2,'Kullanici','Verilere kimler erisebilir?',CURRENT_TIMESTAMP),
(2,'Yapay Zeka','Yalnizca yetkilendirilmis personel kisisel verilere erisebilir.',CURRENT_TIMESTAMP),

-- Oturum 3
(3,'Kullanici','Calisma saatleri nedir?',CURRENT_TIMESTAMP),
(3,'Yapay Zeka','Calisma saatleri hafta ici 08:30 ile 17:30 arasindadir.',CURRENT_TIMESTAMP),
(3,'Kullanici','Izin basvurusu nasil yapilir?',CURRENT_TIMESTAMP),
(3,'Yapay Zeka','Izin talepleri izin yonetim sistemi uzerinden olusturularak yonetici onayina gonderilir.',CURRENT_TIMESTAMP),

-- Oturum 4
(4,'Kullanici','Faturalar nasil onaylanir?',CURRENT_TIMESTAMP),
(4,'Yapay Zeka','Faturalar ilgili departman tarafindan kontrol edilir ve daha sonra muhasebe sistemine aktarilir.',CURRENT_TIMESTAMP),
(4,'Kullanici','Ay sonu raporlari ne zaman hazirlanir?',CURRENT_TIMESTAMP),
(4,'Yapay Zeka','Ay sonu kapanis islemleri tamamlandiktan sonra finansal raporlar hazirlanir.',CURRENT_TIMESTAMP),

-- Oturum 5
(5,'Kullanici','Satin alma sureci nasil baslar?',CURRENT_TIMESTAMP),
(5,'Yapay Zeka','Satin alma talepleri sistem uzerinden olusturulur ve onay surecine gonderilir.',CURRENT_TIMESTAMP),
(5,'Kullanici','Kac teklif alinmalidir?',CURRENT_TIMESTAMP),
(5,'Yapay Zeka','En az uc farkli tedarikciden teklif alinmasi tavsiye edilmektedir.',CURRENT_TIMESTAMP),

-- Oturum 6
(6,'Kullanici','Yangin sirasinda ne yapmaliyim?',CURRENT_TIMESTAMP),
(6,'Yapay Zeka','En yakin acil cikis kullanilarak belirlenen toplanma alanina gidilmelidir.',CURRENT_TIMESTAMP),
(6,'Kullanici','Deprem sirasinda nasil hareket etmeliyim?',CURRENT_TIMESTAMP),
(6,'Yapay Zeka','Guvenli bir noktada yasam ucgeni olusturulmali ve sarsinti sona erene kadar beklenmelidir.',CURRENT_TIMESTAMP);