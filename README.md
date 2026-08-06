RAG Tabanlı Kurumsal Bilgi Yönetimi Sistemi

Yetki filtreli doküman yönetimi ve Retrieval-Augmented Generation (RAG) yaklaşımıyla çalışan kurumsal bilgi asistanıdır. Sistem; PDF, DOCX ve XLSX dosyalarını işler, doküman parçalarını PostgreSQL üzerinde vektör olarak saklar ve kullanıcıların yalnızca yetkili oldukları içeriklerden kaynaklı yanıt almasını sağlar.

Proje, Kocaeli Üniversitesi Bilişim Sistemleri Mühendisliği bölümü yaz stajı kapsamında geliştirilmiştir.

İçindekiler

Projenin Amacı

Temel Özellikler

Kullanılan Teknolojiler

Sistem Mimarisi

Veritabanı Yapısı

Güncel Proje Durumu

Yetkilendirme Modeli

RAG İş Akışı

API Endpointleri

Kurulum

Docker ile Çalıştırma

Testler

Karşılaşılan Sorunlar ve Çözümleri

Ekran Görüntüleri

Bilinen Eksikler

Proje Çıktıları

Projenin Amacı

Kurumlarda dokümanlar farklı departmanlara ve dosya türlerine dağılabilir. Bu proje; dokümanların merkezi bir sistemde saklanmasını, departman bazlı erişim kontrolünün uygulanmasını ve kullanıcıların doğal dilde soru sorarak yalnızca yetkili oldukları içeriklerden cevap almasını amaçlar.

Sistemin temel güvenlik ilkesi şudur: Kullanıcı, görüntüleme yetkisi olmayan bir dokümanı ne doküman listesinde ne de yapay zekâ yanıtlarında görebilir.

Temel Özellikler

JWT tabanlı kullanıcı girişi ve korumalı rotalar

Kullanıcı kaydı ve bcrypt ile parola özetleme

Yönetici tarafından departman oluşturma

PDF, DOCX ve XLSX doküman yükleme

Dosya uzantısı, MIME türü ve 20 MB boyut doğrulaması

Dokümanları otomatik olarak metne dönüştürme, parçalama ve embedding üretme

pgvector ile kosinüs benzerliğine dayalı arama

Yönetici, yükleyen kullanıcı ve departman yetkilerine göre erişim filtresi

Kaynak doküman ve sayfa numarası gösteren RAG cevapları

Sohbet oturumu ve mesaj geçmişi

Doküman etiketleme, yetkilendirme ve arşivleme

PDF dosyalarını tarayıcıda görüntüleme; DOCX ve XLSX dosyalarını indirme

Dashboard, doküman listesi, doküman detayı, yükleme, sohbet ve profil ekranları

Docker Compose ile tek komutta kurulum

Kullanılan Teknolojiler

Katman

Teknolojiler

Backend

Python, FastAPI, SQLAlchemy, Pydantic

Veritabanı

PostgreSQL, Supabase, pgvector

Kimlik doğrulama

JWT, python-jose, passlib, bcrypt

Yapay zekâ

OpenAI API, text-embedding-3-small

Metin işleme

PyMuPDF, python-docx, openpyxl, LangChain Text Splitters, tiktoken

Frontend

React, Vite, React Router, Axios, React Markdown

Test

Pytest, FastAPI TestClient

Dağıtım

Docker, Docker Compose, Nginx

Detaylı teknik terimler için [Teknik Kavramlar Sözlüğü](docs/notlar.md) incelenebilir.

Sistem Mimarisi

flowchart TD
    U[Kullanıcı] --> F[React arayüzü]
    F -->|JWT içeren HTTP istekleri| B[FastAPI backend]
    B --> A[Kimlik ve yetki kontrolü]
    A --> P[(PostgreSQL + pgvector)]
    B --> D[Doküman işleme hattı]
    D --> E[Metin çıkarma ve parçalama]
    E --> O[OpenAI embedding]
    O --> P
    B --> R[Yetki filtreli RAG]
    R --> P
    R --> L[OpenAI dil modeli]
    L --> F

Frontend, Axios interceptor aracılığıyla JWT tokenını her isteğin Authorization başlığına ekler. FastAPI isteği doğrular, kullanıcının erişebileceği dokümanları belirler ve veritabanı işlemlerini SQLAlchemy üzerinden gerçekleştirir.

Veritabanı Yapısı

Sistem aşağıdaki temel tablolardan oluşur:

Tablo

Açıklama

kullanicilar

Kullanıcı, rol, parola özeti ve departman bilgileri

departmanlar

Kurumdaki departmanlar

dokumanlar

Dosya bilgileri, yükleyen kullanıcı, departman ve işlem durumu

dokuman_parcalari

Metin parçaları, token/sayfa bilgileri ve 1536 boyutlu embedding

dokuman_etiketleri

Dokümanlara ait normalize edilmiş etiketler

dokuman_yetkileri

Doküman–departman görüntüleme yetkileri

sohbet_oturumlari

Kullanıcıların sohbet oturumları

sohbet_mesajlari

Kullanıcı ve yapay zekâ mesajları

mesaj_kaynaklari

Yapay zekâ cevaplarında kullanılan doküman parçaları

ER Diyagramı

ER diyagramı aşağıdaki konuma eklendiğinde README üzerinde görüntülenir:



Önemli ilişkiler:

Bir departmanın birden fazla kullanıcısı ve dokümanı olabilir.

Bir kullanıcı birden fazla doküman yükleyebilir ve sohbet oturumu başlatabilir.

Bir dokümanın birden fazla parçası, etiketi ve departman yetkisi olabilir.

Bir sohbet oturumu birden fazla mesaj içerir.

Bir yapay zekâ mesajı birden fazla doküman parçasını kaynak gösterebilir.

Güncel Proje Durumu

Geliştirme ve doğrulama çalışmaları sonunda canlı veritabanında ulaşılan son durum aşağıdaki gibidir:

Veri

Sayı

Departman

6

Kullanıcı

9

Doküman

38

Aktif doküman

19

Arşivlenmiş doküman

19

Doküman parçası

120

Doküman etiketi

65

Doküman yetkisi

31

Sohbet oturumu

18

Sohbet mesajı

79

Mesaj kaynağı

47

Aktif dokümanların 7'si PDF, 6'sı DOCX ve 6'sı XLSX formatındadır. Aktif dokümanlara ait 56 parçanın tamamında text-embedding-3-small modeliyle üretilmiş doğru boyutlu (1536) embedding bulunmaktadır. Toplam 120 parçanın 77'sinde embedding vardır; embedding bulunmayan 43 parça yalnızca arşivlenmiş eski dokümanlara aittir ve aktif RAG aramalarına katılmaz.

Yetkilendirme Modeli

Merkezi gorebildigi_dokuman_idleri fonksiyonu kullanıcıya göre erişilebilir doküman kimliklerini hesaplar:

Yönetici: Arşivlenmemiş tüm dokümanları görebilir.

Yükleyen kullanıcı: Kendi yüklediği dokümanları görebilir ve yönetebilir.

Personel: Kendi departmanına açık olan dokümanları görebilir.

Yetkisiz kullanıcı: Doküman detayına ve başka bir kullanıcının sohbet oturumuna erişemez.

Aynı filtre pgvector aramasının SQL WHERE koşulunda da kullanılır. Böylece yetkisiz içerik, dil modeline gönderilen bağlama hiçbir zaman eklenmez.

RAG İş Akışı

Doküman işleme

Kullanıcı PDF, DOCX veya XLSX dosyasını yükler.

Uzantı, MIME türü ve dosya boyutu doğrulanır.

Dosya UUID adıyla uploads/ klasörüne kaydedilir.

Doküman kaydı isleniyor durumuyla oluşturulur.

Dosya türüne uygun yöntemle metin çıkarılır.

Metin yaklaşık 600 tokenlık ve %10–15 örtüşmeli parçalara ayrılır.

Her parçanın token sayısı, sırası ve sayfa numarası hesaplanır.

text-embedding-3-small ile 1536 boyutlu embedding üretilir.

Metin ve embedding doğrudan dokuman_parcalari tablosuna kaydedilir.

İşlem başarılıysa durum aktif, hata oluşursa hata yapılır.

Soru-cevap

Kullanıcının sorusu embedding vektörüne dönüştürülür.

Kullanıcının görüntüleyebildiği doküman kimlikleri hesaplanır.

Yetki filtresi ve kosinüs benzerliği tek SQL sorgusunda uygulanır.

En ilgili 4–5 doküman parçası seçilir.

Sistem talimatı, numaralı bağlam parçaları ve soru dil modeline gönderilir.

Cevap, sohbet mesajı ve kullanılan kaynaklar veritabanına kaydedilir.

Arayüzde cevapla birlikte doküman başlığı ve sayfa numarası gösterilir.

Bağlamda yeterli bilgi yoksa sistem “Yetkili olduğunuz dokümanlarda bulunamadı.” yanıtını verir.

API Endpointleri

Uygulama çalışırken Swagger arayüzüne http://127.0.0.1:8000/docs adresinden ulaşılabilir.

Kimlik doğrulama ve profil

Metot

Endpoint

Açıklama

POST

/kayit

Yeni personel hesabı oluşturur

POST

/giris

E-posta ve parola karşılığında JWT üretir

GET

/korumali-test

Token doğrulamasını test eder

GET

/profil

Giriş yapan kullanıcının profilini getirir

Dokümanlar

Metot

Endpoint

Açıklama

GET

/dokumanlar

Yetkiye göre aktif dokümanları listeler

GET

/dokumanlar/{dokuman_id}

Yetki kontrollü doküman detayını getirir

GET

/dokumanlar/{dokuman_id}/dosya

Fiziksel dosyayı açar veya indirir

POST

/dokumanlar/yukle

Dosya yükler ve AI işleme hattını başlatır

POST

/dokumanlar/{dokuman_id}/etiket

Dokümana etiket ekler

POST

/dokumanlar/{dokuman_id}/yetki

Departman görüntüleme yetkisi ekler

PATCH

/dokumanlar/{dokuman_id}/arsivle

Dokümanı arşivler

Sohbet ve RAG

Metot

Endpoint

Açıklama

POST

/sohbetler

Yeni sohbet oturumu oluşturur

GET

/sohbetler

Kullanıcının sohbet oturumlarını listeler

GET

/sohbetler/{oturum_id}

Yetki kontrollü sohbet geçmişini getirir

POST

/sohbetler/{oturum_id}/mesaj

Oturuma düz mesaj ekler

POST

/sor

Yetki filtreli RAG cevabı ve kaynakları üretir

Departman ve sistem

Metot

Endpoint

Açıklama

GET

/departmanlar

Departmanları listeler

POST

/departmanlar

Yönetici hesabıyla departman oluşturur

GET

/db-test

Veritabanı bağlantısını doğrular

Kurulum

Gereksinimler

Python 3.12+

Node.js 22+

PostgreSQL ve pgvector veya bir Supabase projesi

OpenAI API anahtarı

1. Depoyu klonlayın

git clone https://github.com/sueda-tut/Kurumsal-Bilgi-Yonetimi.git
cd Kurumsal-Bilgi-Yonetimi

2. Backend ortamını hazırlayın

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt

backend/.env.example dosyasını backend/.env adıyla kopyalayın ve gerçek değerleri girin:

DATABASE_URL=postgresql+psycopg2://kullanici:parola@sunucu:5432/veritabani
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET_KEY=uzun_ve_rastgele_bir_deger
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=8
LOG_LEVEL=INFO
OPENAI_CHAT_MODEL=your_chat_model

Veritabanı ilk kurulumu için sırasıyla database/schema.sql ve database/seed.sql dosyalarını çalıştırın.

Backend'i başlatın:

python -m uvicorn app.main:app --app-dir backend --reload

3. Frontend ortamını hazırlayın

cd frontend
npm.cmd install
Copy-Item .env.example .env
npm.cmd run dev

Frontend varsayılan olarak http://localhost:5173, backend ise http://127.0.0.1:8000 adresinde çalışır. Port doluysa Vite bir sonraki kullanılabilir portu seçebilir.

Docker ile Çalıştırma

Docker Desktop çalışırken proje kökündeki .env.example dosyasını .env adıyla kopyalayın:

Copy-Item .env.example .env

.env içindeki DATABASE_URL, OPENAI_API_KEY ve JWT_SECRET_KEY değerlerini doldurun. Ardından:

docker compose up --build -d
docker compose ps

Servisler sağlıklı olduğunda:

Frontend: http://localhost:5173

Backend: http://127.0.0.1:8000

Swagger: http://127.0.0.1:8000/docs

Containerları durdurmak için:

docker compose down

.env dosyaları ve API anahtarları Git'e eklenmemelidir.

Testler

Backend testlerini çalıştırmak için proje kökünde:

python -m pytest backend/tests -v

Metin çıkarma testleri:

python -m pytest ai/tests -v

Frontend kontrolleri:

cd frontend
npm.cmd run lint
npm.cmd run build

Son doğrulama sonuçları:

Test grubu

Sonuç

Backend kritik senaryoları

7 geçti

PDF, DOCX ve XLSX metin çıkarma

3 geçti

Toplam otomatik test

10 geçti

Güvenlik ve yetkilendirme senaryoları

5/5 geçti

RAG cevap doğruluğu

15/15 (%100)

Doğrulanan kritik senaryolar:

Doğru ve yanlış bilgilerle kullanıcı girişi

Personelin yetkisiz dokümana erişememesi

Yetki filtreli pgvector aramasında veri sızıntısının engellenmesi

Geçersiz uzantı ve uyumsuz MIME türünün reddedilmesi

20 MB üzerindeki dosyanın reddedilmesi

PDF, DOCX ve XLSX dosyalarından metin çıkarılması

Güvenlik ve yetkilendirme doğrulaması

Senaryo

Sonuç

Personelin yetkisiz departman dokümanlarını listeleyememesi

Başarılı

Yetkisiz içerik sorulduğunda RAG bilgi sızıntısı oluşmaması

Başarılı

Yöneticinin tüm aktif dokümanları görebilmesi

Başarılı

Yükleyen kullanıcının kendi dokümanını görebilmesi

Başarılı

Geçersiz dosyanın reddedilmesi ve başkasının sohbetine erişimin 403 dönmesi

Başarılı

İlk RAG doğruluk ölçümü

Hukuk, Ar-Ge, Satın Alma, Muhasebe, İnsan Kaynakları ve Bilgi İşlem departmanlarına ait PDF, DOCX ve XLSX içerikleri üzerinden 15 geçerli soru değerlendirilmiştir. Soruların tamamı doküman içeriğine uygun ve doğru kaynaklarla cevaplanmış; yetkisiz kaynak gösterimi veya RAG bilgi sızıntısı gözlenmemiştir.

Bu sonuç kontrollü ilk değerlendirme kümesine aittir; farklı ve daha geniş soru kümeleriyle yeniden ölçülmesi önerilir.

Karşılaşılan Sorunlar ve Çözümleri

Sorun

Neden

Çözüm

AI cevaplarında **kalın metin** işaretlerinin düz görünmesi

Mesajların düz metin olarak render edilmesi

react-markdown eklenerek Markdown biçimlendirmesi uygulandı

İçeriği bulunmayan bir Muhasebe sorusuna cevap alınamaması

Test sorusundaki vade bilgisinin dokümanda yer almaması

Parçalar SQL ile incelendi ve soru mevcut bütçe–gerçekleşen verisine göre düzeltildi

Yetkisiz departman sorusunda cevap üretilememesi

Yetki filtresinin retrieval sorgusunda doğru uygulanması

Bunun beklenen güvenlik davranışı olduğu doğrulandı

OpenAI embedding isteğinin 429 dönmesi

API kotasının bulunmaması

API kredisi tanımlanarak embedding üretimi yeniden doğrulandı

passlib ve güncel bcrypt uyumsuzluğu

Kütüphane sürümleri arasındaki uyumsuzluk

Uyumlu bcrypt sürümü sabitlendi

Docker ortamında eski verilerin görünmesi

Yerel PostgreSQL containerının Supabase yerine kullanılması

Docker backend bağlantısı Supabase DATABASE_URL değerine yönlendirildi

DOCX dokümanlardan sonra API'nin erişilemez olması

Geliştirme sunucusunun dosya değişikliklerini izleyerek yeniden başlaması

Sunucu kararlı çalıştırma biçimine ve Docker ortamına geçirildi

Ekran Görüntüleri

Ekran görüntüleri docs/images/ klasörüne eklendikten sonra aşağıdaki alanlarda görüntülenecektir.

Giriş ve Dashboard





Doküman Yönetimi





Yetki Filtreli AI Sohbet



Bilinen Eksikler

OpenAI API kullanımı internet bağlantısına ve hesabın API kotasına bağlıdır.

DOCX ve XLSX dosyaları tarayıcı içinde önizlenmek yerine indirilir.

Doküman işleme şu an aynı istek akışında tamamlanmaktadır; yoğun kullanım için görev kuyruğu eklenebilir.

Otomatik test kapsamı kritik akışları doğrulasa da tüm frontend etkileşimlerini kapsayan uçtan uca testler bulunmamaktadır.

Arşivlenmiş eski seed dokümanlarına ait bazı embedding alanları boştur; aktif dokümanların embeddingleri eksiksizdir.

Proje Çıktıları

Proje sonunda aşağıdaki işlevler tamamlanmıştır:

Rol ve departman temelli güvenli doküman erişimi

Üç dosya türü için otomatik metin çıkarma ve parçalama

PostgreSQL üzerinde doğrudan pgvector embedding saklama

Yetki filtresi ile benzerlik aramasını birleştiren RAG altyapısı

Kaynak doküman ve sayfa numarası gösteren yapay zekâ cevapları

Gerçek API'ye bağlı React kullanıcı arayüzü

Kullanıcı kaydı, departman yönetimi ve doküman görüntüleme

Otomatik testler, hata yönetimi ve temel loglama

Docker Compose ile tekrar üretilebilir kurulum

Lisans ve Kullanım

Bu proje eğitim ve staj çalışması kapsamında geliştirilmiştir.

Geliştirici: Sueda TutBölüm: Kocaeli Üniversitesi, Bilişim Sistemleri Mühendisliği