# Doküman yükleme uzantı, MIME ve boyut doğrulamalarını test eder

from importlib import import_module
from types import SimpleNamespace

from app.core.dependencies import get_current_user
from app.db.database import get_db


dokuman_router = import_module("app.routers.dokuman")


def sahte_db():
    yield object()


def sahte_yonetici():
    return SimpleNamespace(
        kullanici_id=1,
        ad_soyad="Murat Aydın",
        eposta="admin@kurumsal.com",
        rol="Yonetici",
        departman_id=1,
        aktif_mi=True,
    )


def bagimliliklari_ayarla(client):
    client.app.dependency_overrides[get_db] = sahte_db
    client.app.dependency_overrides[
        get_current_user
    ] = sahte_yonetici


def test_gecersiz_uzanti_415_doner(client):
    bagimliliklari_ayarla(client)

    response = client.post(
        "/dokumanlar/yukle",
        files={
            "dosya": (
                "zararli.txt",
                b"ornek metin",
                "text/plain",
            )
        },
        data={"baslik": "Geçersiz dosya"},
    )

    assert response.status_code == 415
    assert response.json()["error"]["code"] == (
        "UNSUPPORTED_MEDIA_TYPE"
    )


def test_uyumsuz_mime_turu_415_doner(client):
    bagimliliklari_ayarla(client)

    response = client.post(
        "/dokumanlar/yukle",
        files={
            "dosya": (
                "ornek.pdf",
                b"ornek metin",
                "text/plain",
            )
        },
        data={"baslik": "MIME testi"},
    )

    assert response.status_code == 415
    assert response.json()["error"]["code"] == (
        "UNSUPPORTED_MEDIA_TYPE"
    )


def test_yirmi_mb_uzeri_dosya_413_doner(
    client,
    monkeypatch,
    tmp_path,
):
    bagimliliklari_ayarla(client)

    gecici_uploads = tmp_path / "uploads"

    monkeypatch.setattr(
        dokuman_router,
        "UPLOADS_DIR",
        gecici_uploads,
    )

    buyuk_dosya = b"0" * (
        dokuman_router.MAKSIMUM_DOSYA_BOYUTU + 1
    )

    response = client.post(
        "/dokumanlar/yukle",
        files={
            "dosya": (
                "buyuk.pdf",
                buyuk_dosya,
                "application/pdf",
            )
        },
        data={"baslik": "Boyut testi"},
    )

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "FILE_TOO_LARGE"

    if gecici_uploads.exists():
        assert list(gecici_uploads.iterdir()) == []