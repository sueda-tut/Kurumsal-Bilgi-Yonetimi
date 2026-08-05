RAG Tabanlı Kurumsal Bilgi Yönetimi Sistemi

Staj Ara Raporu

Öğrenci Bilgileri

Ad Soyad: Sueda Tut

Bölüm: Bilişim Sistemleri Mühendisliği

Üniversite: Kocaeli Üniversitesi

Proje Adı: RAG Tabanlı Kurumsal Bilgi Yönetimi Sistemi

Rapor Türü: Staj Ara Raporu

Tarih: Ağustos 2026

1. Projenin Tanımı

Bu proje, kurum içerisindeki dokümanların merkezi ve güvenli bir sistem üzerinden yönetilmesini sağlamak amacıyla geliştirilmektedir. Sistem sayesinde kullanıcılar yetkileri doğrultusunda kurumsal dokümanlara erişebilecek, doküman yükleyebilecek ve sohbet oturumları üzerinden kurumsal bilgiye ulaşabilecektir.

Projede Retrieval-Augmented Generation (RAG) yapısı uygulanmıştır. Kullanıcı soruları embedding vektörlerine dönüştürülmekte, yalnızca kullanıcının yetkili olduğu aktif doküman parçaları içinde pgvector ile anlamsal arama yapılmakta ve bulunan içerikler yapay zekâ modeline bağlam olarak verilmektedir. Üretilen cevapların altında kullanılan doküman ve sayfa bilgileri kaynak kartları şeklinde gösterilmektedir.

2. Projenin Amacı

Projenin temel amaçları şunlardır:

Kurumsal dokümanları merkezi bir veritabanında yönetmek.

Kullanıcıların yalnızca yetkili oldukları dokümanlara erişmesini sağlamak.

Dokümanları departmanlara ve kullanıcılara göre yetkilendirmek.

Dokümanların parçalanarak vektör biçiminde saklanmasını sağlamak.

Kurumsal dokümanlar üzerinde anlamsal arama gerçekleştirmek.

Kullanıcıların doğal dilde soru sorabileceği bir sohbet altyapısı oluşturmak.

Yapay zekâ yanıtlarında kullanılan doküman parçalarını kaynak olarak göstermek.

3. Kullanılan Teknolojiler

Projenin şu ana kadarki geliştirme sürecinde aşağıdaki teknolojiler kullanılmıştır:

Python: Backend geliştirme dili.

FastAPI: REST API geliştirme çatısı.

SQLAlchemy: Veritabanı tablolarının ORM modelleriyle yönetilmesi.

Pydantic: API istek ve yanıt verilerinin doğrulanması.

PostgreSQL: İlişkisel veritabanı yönetim sistemi.

Supabase: PostgreSQL veritabanının bulut ortamında çalıştırılması.

pgvector: Doküman embedding vektörlerinin PostgreSQL içerisinde saklanması.

JWT: Token tabanlı kullanıcı kimlik doğrulama.

Passlib ve bcrypt: Kullanıcı parolalarının güvenli şekilde özetlenmesi.

python-jose: JWT token üretme ve doğrulama.

Pytest: Backend testlerinin hazırlanması ve çalıştırılması.

Swagger: API endpointlerinin görüntülenmesi ve test edilmesi.

OpenAI API: Embedding üretimi ve bağlama dayalı cevap oluşturma.

PyMuPDF, python-docx ve openpyxl: PDF, DOCX ve XLSX dosyalarından metin çıkarma.

LangChain ve tiktoken: Dokümanları parçalara ayırma ve token sayılarını hesaplama.

React ve Vite: Kullanıcı arayüzünün geliştirilmesi.

React Router: Korumalı sayfa yönlendirmeleri.

Axios: Frontend ile FastAPI arasındaki HTTP iletişimi.

React Markdown: Yapay zekâ cevaplarındaki Markdown biçimlendirmesinin gösterilmesi.

Git ve GitHub: Sürüm kontrolü ve proje kaynak kodlarının saklanması.

4. Veritabanı Tasarımı

Proje kapsamında kurumsal bilgi yönetimi ihtiyaçlarına uygun bir PostgreSQL veritabanı tasarlanmıştır. Sistemde aşağıdaki temel tablolar bulunmaktadır:

departmanlar

kullanicilar

dokumanlar

dokuman_parcalari

dokuman_etiketleri

dokuman_yetkileri

sohbet_oturumlari

sohbet_mesajlari

mesaj_kaynaklari

Kullanıcılar bir departmana bağlıdır. Dokümanlar bir kullanıcı tarafından yüklenmekte ve bir departmanla ilişkilendirilmektedir. Doküman yetkileri tablosu aracılığıyla farklı departmanlara doküman görüntüleme yetkisi verilebilmektedir.

Doküman parçaları tablosunda vector(1536) türünde embedding sütunu bulunmaktadır. Doküman parçalarının OpenAI text-embedding-3-small modeliyle üretilen vektörleri doğrudan PostgreSQL içerisinde saklanmaktadır. Ayrı bir vektör veritabanı kullanılmadığı için ilişkisel kayıtlarla embeddingler arasında ek bir senkronizasyon ihtiyacı oluşmamaktadır.

Veritabanında foreign key, unique ve check kısıtları kullanılmıştır. Ayrıca güncelleme tarihlerinin otomatik değiştirilmesi için trigger yapıları hazırlanmıştır.

5. Seed Verileri ve Veritabanı Testleri

Sistemin geliştirme ve test sürecinde kullanılmak üzere tutarlı seed verileri hazırlanmıştır. Seed kapsamında:

4 departman,

5 kullanıcı,

10 temel doküman,

Her doküman için 4 parça,

5 sohbet oturumu,

20 sohbet mesajı,

Doküman etiketleri, yetkileri ve mesaj kaynakları

oluşturulmuştur.

Hatalı rol, durum, dosya türü, dosya boyutu ve foreign key değerleri eklenerek veritabanı kısıtları test edilmiştir. Hazırlanan doğrulama sorguları ile tablo kayıt sayıları, doküman istatistikleri ve kullanıcı erişimleri kontrol edilmiştir.

Veritabanı dosyaları aşağıdaki şekilde ayrılmıştır:

database/schema.sql

database/seed.sql

database/test.sql

Seed verileri sistemin ilk kurulum durumunu temsil etmektedir. Uygulama üzerinden daha sonra oluşturulan kullanıcılar, yüklenen dokümanlar ve sohbet kayıtları seed verisi değil, canlı geliştirme ve test verileridir.

5.1. Güncel Canlı Veritabanı Durumu

Ağustos 2026 itibarıyla canlı geliştirme veritabanındaki kayıt sayıları aşağıdaki gibidir:

Tablo

Kayıt sayısı

departmanlar

6

kullanicilar

9

dokumanlar

38

dokuman_parcalari

120

dokuman_etiketleri

65

dokuman_yetkileri

31

sohbet_oturumlari

18

sohbet_mesajlari

79

mesaj_kaynaklari

47

Sistemde Bilgi İşlem, Muhasebe, İnsan Kaynakları, Satın Alma, Ar-Ge ve Hukuk olmak üzere 6 departman bulunmaktadır. Toplam 38 dokümanın 19'u aktif, 19'u arşiv durumundadır. Aktif dokümanların dosya türlerine göre dağılımı 7 PDF, 6 DOCX ve 6 XLSX şeklindedir.

Departman

Aktif kullanıcı

Aktif doküman

Bilgi İşlem

3

3

Muhasebe

1

3

İnsan Kaynakları

2

3

Satın Alma

1

3

Ar-Ge

1

3

Hukuk

1

4

Toplam 120 doküman parçasının 77'sinde embedding bulunmaktadır. Embeddingi olmayan 43 parça yalnızca eski ve arşivlenmiş dokümanlara aittir. Aktif dokümanlara ait 56 parçanın tamamında 1536 boyutlu embedding bulunduğu SQL doğrulama sorgularıyla kontrol edilmiştir.

Sohbet verileri 18 oturum, 40 kullanıcı mesajı, 39 yapay zekâ mesajı ve toplam 47 kaynak kaydından oluşmaktadır.

6. Backend Mimarisi

Backend uygulaması katmanlı bir yapıya göre geliştirilmiştir:

models/: SQLAlchemy ORM modelleri

schemas/: Pydantic istek ve yanıt şemaları

crud/: Veritabanı işlemleri

routers/: API endpointleri

services/: İş kuralları ve ortak servis fonksiyonları

core/: Güvenlik, bağımlılık, hata yönetimi ve logging

db/: Veritabanı bağlantı yapılandırması

tests/: Otomatik backend testleri

Bu ayrım sayesinde veritabanı işlemleri, API endpointleri ve iş kuralları birbirinden ayrılmıştır. Tekrarlanan yetki ve sahiplik kontrolleri ortak fonksiyonlara taşınmıştır.

7. ORM Modelleri ve Pydantic Şemaları

Veritabanındaki bütün tablolar için SQLAlchemy ORM modelleri oluşturulmuştur. Modeller arasındaki one-to-many ve many-to-many ilişkiler relationship tanımlarıyla kurulmuştur.

Doküman parçalarındaki embedding alanı için pgvector kütüphanesinin Vector(1536) SQLAlchemy türü kullanılmıştır.

Her varlık için Pydantic tarafında Base, Create ve Response şemaları hazırlanmıştır. Yanıt şemalarında from_attributes=True yapılandırması kullanılmıştır.

Güvenlik nedeniyle kullanıcı yanıtlarında sifre ve sifre_ozeti alanlarının dönmesine izin verilmemiştir.

8. Kimlik Doğrulama ve Yetkilendirme

Sisteme e-posta ve parola ile giriş yapılabilmesi için POST /giris endpointi geliştirilmiştir. Kullanıcı parolaları bcrypt algoritmasıyla özetlenmektedir.

Başarılı giriş sonucunda 8 saat geçerli JWT erişim tokenı üretilmektedir. Korunan endpointlere erişim sırasında token doğrulanmakta ve kullanıcı bilgileri get_current_user dependency fonksiyonu üzerinden alınmaktadır.

Aşağıdaki senaryolar test edilmiştir:

Doğru e-posta ve parola ile giriş

Yanlış parola

Sistemde bulunmayan kullanıcı

Tokensız erişim

Geçerli token ile erişim

Süresi dolmuş token ile erişim

9. Doküman Yetkilendirme Sistemi

Kullanıcının görebileceği dokümanları merkezi olarak belirleyen gorebildigi_dokuman_idleri() fonksiyonu hazırlanmıştır.

Yetki kuralları şu şekildedir:

Yönetici bütün dokümanları görebilir.

Personel kendi yüklediği dokümanları görebilir.

Personel kendi departmanına yetki verilen dokümanları görebilir.

Yetkisiz doküman detay isteği 403 Forbidden sonucunu döndürür.

Arşivlenmiş dokümanlar genel doküman listesinde gösterilmez.

Yapılan testte İnsan Kaynakları personelinin Muhasebe departmanına ait dokümanı göremediği doğrulanmıştır.

Bu merkezi yetki fonksiyonu pgvector tabanlı anlamsal aramada da kullanılmaktadır. Benzerlik araması ile doküman yetki filtresi aynı SQL sorgusunda uygulanarak yetkisiz doküman parçalarının yapay zekâ bağlamına girmesi engellenmektedir.

10. Doküman Yönetimi

Sistemde PDF, DOCX ve XLSX dosyalarının yüklenebilmesi için POST /dokumanlar/yukle endpointi geliştirilmiştir.

Dosya yükleme sırasında:

Dosya uzantısı kontrol edilmektedir.

MIME türü doğrulanmaktadır.

En fazla 20 MB dosya yüklenmesine izin verilmektedir.

Dosya UUID tabanlı benzersiz bir adla kaydedilmektedir.

Veritabanında Isleniyor durumuyla doküman kaydı oluşturulmaktadır.

Dosyadan temiz metin çıkarılmakta ve yaklaşık 600 tokenlık, örtüşmeli parçalara ayrılmaktadır.

Her parça için embedding üretilerek dokuman_parcalari.embedding sütununa yazılmaktadır.

İşlem tamamlandığında doküman durumu Aktif, hata oluştuğunda Hata olarak güncellenmektedir.

Başarısız işlemlerde yarım kalan dosya silinmektedir.

Doküman yönetimi kapsamında ayrıca:

Dokümana etiket ekleme,

Etiketleri küçük harfe dönüştürme,

Departmana görüntüleme yetkisi verme,

Yönetici veya yükleyen kullanıcı kontrolü,

Dokümanı arşivleme

Yetkili kullanıcının PDF dosyasını tarayıcıda görüntülemesi, DOCX ve XLSX dosyalarını indirmesi

işlemleri tamamlanmıştır.

11. Sohbet ve RAG Altyapısı

Temel sohbet kayıt altyapısı, pgvector tabanlı retrieval ve yapay zekâ cevap üretim akışıyla birleştirilmiştir.

Kullanıcılar:

Yeni sohbet oturumu oluşturabilir.

Kendi sohbet oturumlarını listeleyebilir.

Sohbet oturumuna mesaj ekleyebilir.

Oturumdaki mesajları görüntüleyebilir.

Yetkili oldukları kurumsal dokümanlar hakkında doğal dilde soru sorabilir.

Yapay zekâ cevabında kullanılan doküman ve sayfa kaynaklarını görüntüleyebilir.

Kullanıcıların başka kullanıcılara ait sohbet oturumlarına erişmesi 403 Forbidden ile engellenmektedir. POST /sor akışında kullanıcı sorusu kaydedilmekte, soru embeddingi üretilmekte, yetki filtreli pgvector aramasıyla ilgili parçalar seçilmekte, LLM cevabı oluşturulmakta ve cevap ile kaynak ilişkileri sohbet_mesajlari ve mesaj_kaynaklari tablolarına kaydedilmektedir.

Prompt şablonunda modelin yalnızca sağlanan bağlamı kullanması, bağlamda cevap yoksa “Yetkili olduğunuz dokümanlarda bulunamadı.” demesi ve doküman içeriklerini talimat değil veri olarak değerlendirmesi istenmektedir.

12. Hata Yönetimi ve Logging

API genelinde standart hata yanıt formatı oluşturulmuştur. 401, 403, 404, 409, 413, 415, 422 ve 500 durumları ortak bir JSON yapısında döndürülmektedir.

Standart hata yanıtı aşağıdaki alanları içermektedir:

Hata kodu

Kullanıcıya gösterilecek mesaj

Gerekli durumlarda doğrulama ayrıntıları

İstek yolu

Logging altyapısıyla birlikte HTTP metodu, istek yolu, durum kodu ve işlem süresi terminale kaydedilmektedir. Beklenmeyen hatalar ayrıntılı olarak loglanırken kullanıcıya güvenli bir hata mesajı döndürülmektedir.

13. Frontend Uygulaması

Vite ve React kullanılarak FastAPI ile gerçek zamanlı iletişim kuran bir kullanıcı arayüzü geliştirilmiştir. Axios interceptor yapısı her korumalı isteğe JWT tokenını eklemekte, geçersiz veya süresi dolmuş token durumunda kullanıcı giriş sayfasına yönlendirilmektedir.

Frontend uygulamasında aşağıdaki ekranlar tamamlanmıştır:

Kullanıcı giriş ve kayıt ekranı

Korumalı rota ve güvenli çıkış işlemi

Görülebilen doküman ve son sohbet sayılarını gösteren dashboard

Yetkiye göre doküman listesi ve doküman detay ekranı

PDF görüntüleme ile DOCX/XLSX indirme işlemleri

Dosya, başlık, departman, etiket ve yetki bilgileriyle doküman yükleme formu

Dokümanın Isleniyor, Aktif ve Hata durumlarını izleyen yükleme göstergesi

Geçmiş oturumları, mesaj balonlarını ve kaynak kartlarını gösteren AI sohbet ekranı

Kullanıcı profil ekranı

Yöneticinin departman ekleyebildiği departman yönetim ekranı

Yönetici veya yükleyenin dokümanı arşivleyebilmesi

Kayıt olan kullanıcılar Personel rolüyle kullanıcı tablosuna eklenmektedir. Yöneticiye ait işlemler hem frontend görünürlüğü hem de backend yetki kontrolüyle sınırlandırılmıştır.

14. Plan Dışı Ek Geliştirmeler

Projenin başlangıç planında bulunmamasına rağmen, kullanılabilirliği ve yönetilebilirliği artırmak amacıyla aşağıdaki ek özellikler geliştirilmiştir:

- Kullanıcıların ad, e-posta, parola ve departman bilgileriyle sisteme kayıt olabilmesi sağlanmıştır. Yeni kullanıcılar güvenli parola özetiyle `kullanicilar` tablosuna kaydedilmektedir.
- Yönetici rolündeki kullanıcıların sistem üzerinden yeni departman oluşturabilmesi sağlanmıştır. Bu özellik yalnızca yöneticilerin erişebildiği departman yönetimi ekranına eklenmiştir.
- Yetkili kullanıcıların doküman detay ekranından fiziksel dosyaya ulaşabilmesi sağlanmıştır. PDF dosyaları tarayıcıda görüntülenirken DOCX ve XLSX dosyaları güvenli şekilde indirilebilmektedir.
- Test amaçlı boş veya eski dokümanlar arşivlenmiş; PDF, DOCX ve XLSX formatlarında gerçek içerikli kurumsal dokümanlar sisteme yüklenmiştir.
- Yeni dokümanların metin çıkarma, parçalama ve embedding işlemleri tamamlanarak yetki filtreli RAG soru-cevap sisteminde kullanılabilmesi sağlanmıştır.
- Yönetici kullanıcıların dokümanları arayüz üzerinden arşivleyebilmesi sağlanmış ve arşivlenen dokümanların aktif listelerde görünmesi engellenmiştir.

15. Otomatik Testler

Backend tarafındaki kritik işlemler için Pytest kullanılarak otomatik testler hazırlanmıştır.

Test edilen senaryolar:

Doğru bilgilerle kullanıcı girişi

Yanlış parola ile giriş

Personelin yetkisiz dokümana erişiminin engellenmesi

Geçersiz dosya uzantısının reddedilmesi

Dosya uzantısı ile MIME türü uyumsuzluğunun reddedilmesi

20 MB üzerindeki dosyanın reddedilmesi

Yetki filtreli pgvector aramasında İK personelinin Muhasebe doküman parçalarını alamamasının doğrulanması

Testler gerçek Supabase verilerini değiştirmeyecek şekilde dependency override ve mock yapıları kullanılarak hazırlanmıştır.

Test sonucu:

7 passed

Doküman metni çıkarma modülü için ayrıca PDF, DOCX ve XLSX formatlarında üç bağımsız test uygulanmıştır.

AI metin çıkarma test sonucu:

3 passed

Toplam otomatik test sonucu:

10 passed

16. Yetki, Güvenlik ve RAG Testleri

Sistemin departman bazlı yetkilendirme yapısını, doküman erişim kurallarını ve RAG sürecinde bilgi sızıntısı oluşup oluşmadığını doğrulamak amacıyla temel kullanım senaryoları test edilmiştir.

No

Test senaryosu

Beklenen sonuç

Gerçekleşen sonuç

Durum

1

Personelin yetkisiz olduğu departmana ait dokümanları listelemesi

Yetkisiz dokümanlar listede görünmemelidir.

İK personeli, Hukuk ve Muhasebe dokümanlarını görüntüleyememiştir.

✅ Başarılı

2

Personelin yetkisiz dokümanın içeriği hakkında AI’a soru sorması

Sistem bilgi sızdırmadan “Yetkili olduğunuz dokümanlarda bulunamadı.” cevabını vermelidir.

AI, yetkisiz dokümanın içeriğini ve kaynaklarını döndürmemiştir.

✅ Başarılı

3

Yöneticinin dokümanları listelemesi

Yönetici, tüm departmanlara ait aktif dokümanları görüntüleyebilmelidir.

Yönetici hesabında tüm departmanların aktif dokümanları görüntülenmiştir.

✅ Başarılı

4

Dokümanı yükleyen kullanıcının kendi dokümanını görüntülemesi

Kullanıcı, yüklediği dokümanı departmanından bağımsız olarak görebilmelidir.

Yükleyen kullanıcı kendi dokümanına erişebilmiştir.

✅ Başarılı

5

Geçersiz dosya yüklenmesi ve başka kullanıcıya ait sohbet oturumuna erişilmesi

Dosya doğrulama hatası oluşmalı; yetkisiz oturum erişimi 403 dönmelidir.

Geçersiz dosya reddedilmiş ve başka kullanıcının oturumuna erişim 403 ile engellenmiştir.

✅ Başarılı

Güvenlik Testi Sonucu

Toplam 5 güvenlik ve yetkilendirme senaryosunun tamamı başarıyla geçmiştir. Testlerde departmanlar arasında yetkisiz doküman erişimi veya RAG üzerinden bilgi sızıntısı tespit edilmemiştir.

17. İlk RAG Cevap Doğruluğu Ölçümü

RAG sisteminin cevap üretme başarısını değerlendirmek amacıyla farklı departmanlara ve dosya türlerine ait dokümanlar üzerinden 15 örnek soru sorulmuştur. Cevapların doküman içeriğiyle uyumu ve gösterilen kaynakların doğru departmana ait olması birlikte değerlendirilmiştir.

No

Departman

Test sorusu

Beklenen sonuç

Durum

1

Hukuk

Yüksek riskli sözleşmelerin Hukuk inceleme hedef süresi kaç iş günüdür?

5 iş günü

✅ Doğru

2

Hukuk

Sözleşme kapsamındaki bir veri ihlali en geç kaç saat içinde bildirilmelidir?

24 saat

✅ Doğru

3

Hukuk

Sözleşmeler sona erdikten sonra kayıtlar en az kaç yıl saklanmalıdır?

10 yıl

✅ Doğru

4

Hukuk

Otomatik yenilenen sözleşmeler için hangi tarihlerde bildirim oluşturulmalıdır?

Bitişten 90, 60 ve 30 gün önce

✅ Doğru

5

Hukuk

Esaslı sözleşme ihlalinde tanınan düzeltme süresi kaç gündür?

15 gün

✅ Doğru

6

Ar-Ge

Ar-Ge proje önerilerinin ön değerlendirmesinde hangi kriterler kontrol edilir?

Kriterlerin Ar-Ge dokümanlarına dayanarak açıklanması

✅ Doğru

7

Ar-Ge

Ar-Ge projelerinin ilerleme durumları hangi bilgilerle izlenir?

Takip tablosundaki alanların doğru açıklanması

✅ Doğru

8

Satın Alma

Satın alma talebinden siparişe kadar hangi adımlar uygulanır?

Süreç adımlarının doğru sırayla açıklanması

✅ Doğru

9

Satın Alma

Tedarikçi değerlendirilirken hangi kriterler dikkate alınır?

İlgili değerlendirme kriterlerinin açıklanması

✅ Doğru

10

Muhasebe

Faturaların kontrol ve onay süreci nasıl yürütülür?

Muhasebe sürecinin doğru açıklanması

✅ Doğru

11

Muhasebe

Temmuz 2026 döneminde Genel Yönetim biriminin bütçe ve gerçekleşen tutarı nedir?

Bütçe: 420.000, gerçekleşen: 397.500, sapma: -22.500

✅ Doğru

12

İnsan Kaynakları

Çalışanların izin talepleri hangi adımlarla değerlendirilir ve onaylanır?

İzin sürecinin İK dokümanlarına göre açıklanması

✅ Doğru

13

Bilgi İşlem

Kullanıcı erişim yetkileri verilirken hangi güvenlik kontrolleri uygulanır?

Yetkilendirme kontrollerinin açıklanması

✅ Doğru

14

Bilgi İşlem

Sistemlerin durumu ve sorumlu kişiler takip tablosunda nasıl izlenir?

Takip tablosundaki ilgili alanların açıklanması

✅ Doğru

15

İnsan Kaynakları

Personel oryantasyon sürecinde hangi işlemler uygulanır?

Oryantasyon adımlarının doğru açıklanması

✅ Doğru

Doğruluk Hesabı

İlk doğruluk oranı aşağıdaki formülle hesaplanmıştır:

Doğruluk oranı = Doğru cevap sayısı / Geçerli soru sayısı × 100

Doğruluk oranı = 15 / 15 × 100 = %100

Ölçüm

Sonuç

Hazırlanan toplam soru

16

Geçersiz sayılarak değiştirilen soru

1

Değerlendirilen geçerli soru

15

Doğru cevap

15

Yanlış cevap

0

İlk doğruluk oranı

%100

Yetkisiz kaynak gösterimi

0

RAG bilgi sızıntısı

0

Muhasebe takip tablosunda ödeme durumu ve vade bilgileri bulunmadığı için bu alanlarla ilgili hazırlanan ilk soru geçersiz kabul edilmiştir. Bu soru doğruluk hesabına dahil edilmemiş ve doküman içeriğiyle uyumlu bütçe-gerçekleşen sorusuyla değiştirilmiştir.

18. Tespit Edilen Hatalar ve Çözümleri

No

Hata veya bulgu

Neden

Uygulanan çözüm

Son durum

1

AI cevabındaki **5 iş günüdür** gibi Markdown işaretlerinin arayüzde doğrudan görünmesi

Mesaj içeriğinin React bileşeninde düz metin olarak gösterilmesi

react-markdown paketi eklenerek AI mesajları Markdown biçiminde gösterildi.

✅ Çözüldü

2

Muhasebe vade sorusuna “Yetkili olduğunuz dokümanlarda bulunamadı.” cevabı verilmesi

İlgili Excel dokümanında ödeme durumu ve vade bilgisi bulunmaması

Doküman parçaları SQL sorgusuyla kontrol edildi ve soru mevcut bütçe-gerçekleşen içeriğine uygun şekilde değiştirildi.

✅ Test verisi düzeltildi

3

Yetkisiz departman içeriği sorulduğunda cevap üretilememesi

Departman bazlı yetki filtresinin sorgu sırasında uygulanması

Bu durum hata değil, beklenen güvenlik davranışı olarak doğrulandı.

✅ Beklenen davranış

19. Bilinen Eksikler ve İyileştirme Önerileri

- Eski ve arşivlenmiş bazı doküman parçalarında embedding verisi bulunmamaktadır. Bu durum aktif dokümanları ve mevcut RAG aramalarını etkilememektedir.
- Yüklenen dosyalar şu an uygulamanın yerel `uploads/` klasöründe saklanmaktadır. Üretim ortamında bulut tabanlı dosya depolama kullanılmalıdır.
- PDF dosyaları tarayıcıda görüntülenebilirken DOCX ve XLSX dosyaları indirilerek açılmaktadır.
- Doküman çıkarma, parçalama ve embedding üretme işlemleri aynı yükleme akışında yürütülmektedir. Büyük dosya veya yoğun kullanım için arka plan görev sistemi eklenebilir.
- Otomatik testlerde kullanılan bazı kütüphanelerden kullanım dışı bırakılma uyarısı alınmaktadır. Bu uyarı testlerin çalışmasını etkilememektedir.
- Sistem, OpenAI API ve Supabase bağlantısına bağımlıdır. Bu servislerin erişilemez olması durumunda ilgili işlemler gerçekleştirilemez.

20. Genel Değerlendirme

Gerçekleştirilen testler sonucunda departman bazlı doküman yetkilendirmesinin hem doküman listeleme hem de pgvector tabanlı RAG araması sırasında doğru uygulandığı görülmüştür. Yetkisiz kullanıcıların doküman içeriğine doğrudan veya AI aracılığıyla erişemediği doğrulanmıştır.

Farklı departmanlara ait PDF, DOCX ve XLSX dosyaları üzerinden yapılan ilk ölçümde sistem 15 geçerli sorunun tamamına doküman içeriğiyle uyumlu cevap vermiştir. Kaynak kartlarında ilgili dokümanların gösterildiği ve yetkisiz departmanlardan kaynak kullanılmadığı gözlemlenmiştir. Bu sonuçlar sistemin ilk değerlendirmede %100 cevap doğruluğu ve %100 güvenlik senaryosu başarısı elde ettiğini göstermektedir.

Projenin mevcut durumunda veritabanı şeması ve seed dosyaları hazırlanmış, FastAPI backend uygulaması tamamlanmış, JWT kimlik doğrulama ve departman bazlı yetkilendirme uygulanmış, doküman işleme ve pgvector tabanlı RAG süreci devreye alınmış ve React arayüzündeki bütün temel ekranlar gerçek API ile çalışır hâle getirilmiştir.

Canlı geliştirme veritabanındaki aktif doküman parçalarının tamamında doğru boyutlu embedding bulunmaktadır. Arşivlenmiş eski dokümanlardaki eksik embeddingler aktif arama kapsamına girmediği için güncel RAG işleyişini etkilememektedir. Sistem, staj projesi kapsamında hedeflenen güvenli kurumsal doküman yönetimi ve kaynaklı soru-cevap işlevlerini uçtan uca yerine getirmektedir.