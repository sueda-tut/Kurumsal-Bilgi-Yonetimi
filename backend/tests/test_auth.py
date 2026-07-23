# Başarılı ve başarısız kullanıcı girişlerini test eder

from importlib import import_module
from types import SimpleNamespace

from app.core.security import sifre_ozeti_olustur
from app.db.database import get_db


auth_router = import_module("app.routers.auth")


def sahte_db():
    yield object()


def test_dogru_bilgilerle_giris_basarili(
    client,
    monkeypatch,
):
    kullanici = SimpleNamespace(
        kullanici_id=1,
        eposta="admin@kurumsal.com",
        sifre_ozeti=sifre_ozeti_olustur("Test123!"),
        aktif_mi=True,
    )

    monkeypatch.setattr(
        auth_router,
        "eposta_ile_kullanici_bul",
        lambda db, eposta: kullanici,
    )

    client.app.dependency_overrides[get_db] = sahte_db

    response = client.post(
        "/giris",
        json={
            "eposta": "admin@kurumsal.com",
            "sifre": "Test123!",
        },
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["expires_in"] == 28800
    assert response.json()["access_token"]


def test_yanlis_sifreyle_giris_401_doner(
    client,
    monkeypatch,
):
    kullanici = SimpleNamespace(
        kullanici_id=1,
        eposta="admin@kurumsal.com",
        sifre_ozeti=sifre_ozeti_olustur("Dogru123!"),
        aktif_mi=True,
    )

    monkeypatch.setattr(
        auth_router,
        "eposta_ile_kullanici_bul",
        lambda db, eposta: kullanici,
    )

    client.app.dependency_overrides[get_db] = sahte_db

    response = client.post(
        "/giris",
        json={
            "eposta": "admin@kurumsal.com",
            "sifre": "Yanlis123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["error"]["code"] == "UNAUTHORIZED"