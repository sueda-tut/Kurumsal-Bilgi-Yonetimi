# pgvector aramasında Ahmet'in Muhasebe chunk'larını göremediğini test eder

from types import SimpleNamespace

from app.services import vektor_arama


class SahteMappingSonucu:
    def __init__(self, satirlar):
        self.satirlar = satirlar

    def mappings(self):
        return self

    def all(self):
        return self.satirlar


class SahteDb:
    def __init__(self):
        self.calistirilan_sorgu = None
        self.parametreler = None

    def execute(self, sorgu, parametreler):
        self.calistirilan_sorgu = str(sorgu)
        self.parametreler = parametreler

        # PostgreSQL'in yetki filtresinden sonra döndürdüğü
        # İnsan Kaynakları dokümanı örneklenir
        return SahteMappingSonucu(
            [
                {
                    "parca_id": 41,
                    "dokuman_id": 1,
                    "parca_sirasi": 1,
                    "parca_metni": (
                        "Personel izin işlemleri sistem "
                        "üzerinden yürütülür."
                    ),
                    "sayfa_no": 1,
                    "baslik": "Personel El Kitabı",
                    "benzerlik_puani": 0.82,
                }
            ]
        )


def test_ahmet_muhasebe_chunkini_goremez(
    monkeypatch,
):
    ahmet = SimpleNamespace(
        kullanici_id=2,
        ad_soyad="Ahmet Yılmaz",
        eposta="ahmet.yilmaz@kurumsal.com",
        rol="Personel",
        departman_id=4,
        aktif_mi=True,
    )

    db = SahteDb()

    # Ahmet'in yalnızca 1 ve 2 numaralı dokümanları
    # görebildiği örneklenir
    monkeypatch.setattr(
        vektor_arama,
        "gorebildigi_dokuman_idleri",
        lambda db, kullanici: [1, 2],
    )

    # Test sırasında gerçek OpenAI API çağrısı yapılmaz
    monkeypatch.setattr(
        vektor_arama,
        "embeddingleri_uret",
        lambda metinler: [[0.0] * 1536],
    )

    sonuclar = vektor_arama.ilgili_parcalari_ara(
        db=db,
        kullanici=ahmet,
        soru="Faturalar nasıl onaylanır?",
        limit=5,
    )

    donen_dokuman_idleri = {
        sonuc.dokuman_id
        for sonuc in sonuclar
    }

    # Muhasebe dokümanları 3 ve 4 sonuçlarda bulunmamalı
    assert 3 not in donen_dokuman_idleri
    assert 4 not in donen_dokuman_idleri

    # Yetkili ID'lerin SQL sorgusuna aktarıldığını doğrular
    assert db.parametreler["dokuman_idleri"] == [1, 2]
    assert db.parametreler["sonuc_limiti"] == 5

    # Yetki ve benzerlik işlemlerinin aynı SQL'de olduğunu doğrular
    assert "dp.dokuman_id IN" in db.calistirilan_sorgu
    assert "dp.embedding <=>" in db.calistirilan_sorgu
    