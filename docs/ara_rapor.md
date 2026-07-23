# RAG Tabanlı Kurumsal Bilgi Yönetimi Sistemi
## Staj Ara Raporu

### Öğrenci Bilgileri

- **Ad Soyad:** Sueda Tut
- **Bölüm:** Bilişim Sistemleri Mühendisliği
- **Üniversite:** Kocaeli Üniversitesi
- **Proje Adı:** RAG Tabanlı Kurumsal Bilgi Yönetimi Sistemi
- **Rapor Türü:** Staj Ara Raporu
- **Tarih:** Temmuz 2026

---

## 1. Projenin Tanımı

Bu proje, kurum içerisindeki dokümanların merkezi ve güvenli bir sistem üzerinden yönetilmesini sağlamak amacıyla geliştirilmektedir. Sistem sayesinde kullanıcılar yetkileri doğrultusunda kurumsal dokümanlara erişebilecek, doküman yükleyebilecek ve sohbet oturumları üzerinden kurumsal bilgiye ulaşabilecektir.

Projenin ilerleyen aşamasında Retrieval-Augmented Generation (RAG) yapısı kullanılacaktır. Bu yapı sayesinde kullanıcı soruları, yetkili oldukları doküman parçaları içerisinde aranacak ve bulunan içerikler yapay zekâ modeline kaynak olarak verilecektir. Böylece modelin kurum dışı veya ilgisiz bilgiler yerine kurumun kendi dokümanlarından yararlanarak yanıt üretmesi hedeflenmektedir.

---

## 2. Projenin Amacı

Projenin temel amaçları şunlardır:

- Kurumsal dokümanları merkezi bir veritabanında yönetmek.
- Kullanıcıların yalnızca yetkili oldukları dokümanlara erişmesini sağlamak.
- Dokümanları departmanlara ve kullanıcılara göre yetkilendirmek.
- Dokümanların parçalanarak vektör biçiminde saklanmasını sağlamak.
- Kurumsal dokümanlar üzerinde anlamsal arama gerçekleştirmek.
- Kullanıcıların doğal dilde soru sorabileceği bir sohbet altyapısı oluşturmak.
- Yapay zekâ yanıtlarında kullanılan doküman parçalarını kaynak olarak göstermek.

---

## 3. Kullanılan Teknolojiler

Projenin şu ana kadarki geliştirme sürecinde aşağıdaki teknolojiler kullanılmıştır:

- **Python:** Backend geliştirme dili.
- **FastAPI:** REST API geliştirme çatısı.
- **SQLAlchemy:** Veritabanı tablolarının ORM modelleriyle yönetilmesi.
- **Pydantic:** API istek ve yanıt verilerinin doğrulanması.
- **PostgreSQL:** İlişkisel veritabanı yönetim sistemi.
- **Supabase:** PostgreSQL veritabanının bulut ortamında çalıştırılması.
- **pgvector:** Doküman embedding vektörlerinin PostgreSQL içerisinde saklanması.
- **JWT:** Token tabanlı kullanıcı kimlik doğrulama.
- **Passlib ve bcrypt:** Kullanıcı parolalarının güvenli şekilde özetlenmesi.
- **python-jose:** JWT token üretme ve doğrulama.
- **Pytest:** Backend testlerinin hazırlanması ve çalıştırılması.
- **Swagger:** API endpointlerinin görüntülenmesi ve test edilmesi.
- **Git ve GitHub:** Sürüm kontrolü ve proje kaynak kodlarının saklanması.

---

## 4. Veritabanı Tasarımı

Proje kapsamında kurumsal bilgi yönetimi ihtiyaçlarına uygun bir PostgreSQL veritabanı tasarlanmıştır. Sistemde aşağıdaki temel tablolar bulunmaktadır:

1. `departmanlar`
2. `kullanicilar`
3. `dokumanlar`
4. `dokuman_parcalari`
5. `dokuman_etiketleri`
6. `dokuman_yetkileri`
7. `sohbet_oturumlari`
8. `sohbet_mesajlari`
9. `mesaj_kaynaklari`

Kullanıcılar bir departmana bağlıdır. Dokümanlar bir kullanıcı tarafından yüklenmekte ve bir departmanla ilişkilendirilmektedir. Doküman yetkileri tablosu aracılığıyla farklı departmanlara doküman görüntüleme yetkisi verilebilmektedir.

Doküman parçaları tablosunda `vector(1536)` türünde embedding sütunu bulunmaktadır. Bu yapı, ilerleyen aşamada doküman parçalarının OpenAI embedding modeliyle vektörleştirilerek pgvector içerisinde saklanmasını sağlayacaktır.

Veritabanında foreign key, unique ve check kısıtları kullanılmıştır. Ayrıca güncelleme tarihlerinin otomatik değiştirilmesi için trigger yapıları hazırlanmıştır.

---

## 5. Seed Verileri ve Veritabanı Testleri

Sistemin geliştirme ve test sürecinde kullanılmak üzere tutarlı seed verileri hazırlanmıştır. Seed kapsamında:

- 4 departman,
- 5 kullanıcı,
- 10 temel doküman,
- Her doküman için 4 parça,
- 5 sohbet oturumu,
- 20 sohbet mesajı,
- Doküman etiketleri, yetkileri ve mesaj kaynakları

oluşturulmuştur.

Hatalı rol, durum, dosya türü, dosya boyutu ve foreign key değerleri eklenerek veritabanı kısıtları test edilmiştir. Hazırlanan doğrulama sorguları ile tablo kayıt sayıları, doküman istatistikleri ve kullanıcı erişimleri kontrol edilmiştir.

Veritabanı dosyaları aşağıdaki şekilde ayrılmıştır:

- `database/schema.sql`
- `database/seed.sql`
- `database/test.sql`

---

## 6. Backend Mimarisi

Backend uygulaması katmanlı bir yapıya göre geliştirilmiştir:

- `models/`: SQLAlchemy ORM modelleri
- `schemas/`: Pydantic istek ve yanıt şemaları
- `crud/`: Veritabanı işlemleri
- `routers/`: API endpointleri
- `services/`: İş kuralları ve ortak servis fonksiyonları
- `core/`: Güvenlik, bağımlılık, hata yönetimi ve logging
- `db/`: Veritabanı bağlantı yapılandırması
- `tests/`: Otomatik backend testleri

Bu ayrım sayesinde veritabanı işlemleri, API endpointleri ve iş kuralları birbirinden ayrılmıştır. Tekrarlanan yetki ve sahiplik kontrolleri ortak fonksiyonlara taşınmıştır.

---

## 7. ORM Modelleri ve Pydantic Şemaları

Veritabanındaki bütün tablolar için SQLAlchemy ORM modelleri oluşturulmuştur. Modeller arasındaki one-to-many ve many-to-many ilişkiler `relationship` tanımlarıyla kurulmuştur.

Doküman parçalarındaki embedding alanı için pgvector kütüphanesinin `Vector(1536)` SQLAlchemy türü kullanılmıştır.

Her varlık için Pydantic tarafında `Base`, `Create` ve `Response` şemaları hazırlanmıştır. Yanıt şemalarında `from_attributes=True` yapılandırması kullanılmıştır.

Güvenlik nedeniyle kullanıcı yanıtlarında `sifre` ve `sifre_ozeti` alanlarının dönmesine izin verilmemiştir.

---

## 8. Kimlik Doğrulama ve Yetkilendirme

Sisteme e-posta ve parola ile giriş yapılabilmesi için `POST /giris` endpointi geliştirilmiştir. Kullanıcı parolaları bcrypt algoritmasıyla özetlenmektedir.

Başarılı giriş sonucunda 8 saat geçerli JWT erişim tokenı üretilmektedir. Korunan endpointlere erişim sırasında token doğrulanmakta ve kullanıcı bilgileri `get_current_user` dependency fonksiyonu üzerinden alınmaktadır.

Aşağıdaki senaryolar test edilmiştir:

- Doğru e-posta ve parola ile giriş
- Yanlış parola
- Sistemde bulunmayan kullanıcı
- Tokensız erişim
- Geçerli token ile erişim
- Süresi dolmuş token ile erişim

---

## 9. Doküman Yetkilendirme Sistemi

Kullanıcının görebileceği dokümanları merkezi olarak belirleyen `gorebildigi_dokuman_idleri()` fonksiyonu hazırlanmıştır.

Yetki kuralları şu şekildedir:

- Yönetici bütün dokümanları görebilir.
- Personel kendi yüklediği dokümanları görebilir.
- Personel kendi departmanına yetki verilen dokümanları görebilir.
- Yetkisiz doküman detay isteği `403 Forbidden` sonucunu döndürür.
- Arşivlenmiş dokümanlar genel doküman listesinde gösterilmez.

Yapılan testte İnsan Kaynakları personelinin Muhasebe departmanına ait dokümanı göremediği doğrulanmıştır.

Bu merkezi yetki fonksiyonu ilerleyen aşamada pgvector tabanlı anlamsal aramada da kullanılacaktır.

---

## 10. Doküman Yönetimi

Sistemde PDF, DOCX ve XLSX dosyalarının yüklenebilmesi için `POST /dokumanlar/yukle` endpointi geliştirilmiştir.

Dosya yükleme sırasında:

- Dosya uzantısı kontrol edilmektedir.
- MIME türü doğrulanmaktadır.
- En fazla 20 MB dosya yüklenmesine izin verilmektedir.
- Dosya UUID tabanlı benzersiz bir adla kaydedilmektedir.
- Veritabanında `Isleniyor` durumuyla doküman kaydı oluşturulmaktadır.
- Başarısız işlemlerde yarım kalan dosya silinmektedir.

Doküman yönetimi kapsamında ayrıca:

- Dokümana etiket ekleme,
- Etiketleri küçük harfe dönüştürme,
- Departmana görüntüleme yetkisi verme,
- Yönetici veya yükleyen kullanıcı kontrolü,
- Dokümanı arşivleme

işlemleri tamamlanmıştır.

---

## 11. Sohbet Altyapısı

Yapay zekâ entegrasyonundan önce temel sohbet kayıt altyapısı hazırlanmıştır.

Kullanıcılar:

- Yeni sohbet oturumu oluşturabilir.
- Kendi sohbet oturumlarını listeleyebilir.
- Sohbet oturumuna mesaj ekleyebilir.
- Oturumdaki mesajları görüntüleyebilir.

Kullanıcıların başka kullanıcılara ait sohbet oturumlarına erişmesi `403 Forbidden` ile engellenmektedir. Şu aşamada mesajlar düz kayıt olarak saklanmakta, henüz yapay zekâ yanıtı üretilmemektedir.

---

## 12. Hata Yönetimi ve Logging

API genelinde standart hata yanıt formatı oluşturulmuştur. `401`, `403`, `404`, `409`, `413`, `415`, `422` ve `500` durumları ortak bir JSON yapısında döndürülmektedir.

Standart hata yanıtı aşağıdaki alanları içermektedir:

- Hata kodu
- Kullanıcıya gösterilecek mesaj
- Gerekli durumlarda doğrulama ayrıntıları
- İstek yolu

Logging altyapısıyla birlikte HTTP metodu, istek yolu, durum kodu ve işlem süresi terminale kaydedilmektedir. Beklenmeyen hatalar ayrıntılı olarak loglanırken kullanıcıya güvenli bir hata mesajı döndürülmektedir.

---

## 13. Otomatik Testler

Backend tarafındaki kritik işlemler için Pytest kullanılarak otomatik testler hazırlanmıştır.

Test edilen senaryolar:

1. Doğru bilgilerle kullanıcı girişi
2. Yanlış parola ile giriş
3. Personelin yetkisiz dokümana erişiminin engellenmesi
4. Geçersiz dosya uzantısının reddedilmesi
5. Dosya uzantısı ile MIME türü uyumsuzluğunun reddedilmesi
6. 20 MB üzerindeki dosyanın reddedilmesi

Testler gerçek Supabase verilerini değiştirmeyecek şekilde dependency override ve mock yapıları kullanılarak hazırlanmıştır.

Test sonucu:

```text
6 passed