# Personelin yetkisiz dokümana erişiminin engellendiğini test eder

from importlib import import_module
from types import SimpleNamespace

from app.core.dependencies import get_current_user
from app.db.database import get_db


dokuman_router = import_module("app.routers.dokuman")


def sahte_db():
    yield object()


def sahte_personel():
    return SimpleNamespace(
        kullanici_id=2,
        ad_soyad="Ahmet Yılmaz",
        eposta="ahmet.yilmaz@kurumsal.com",
        rol="Personel",
        departman_id=4,
        aktif_mi=True,
    )


def test_personel_yetkisiz_dokumana_erisemez(
    client,
    monkeypatch,
):
    dokuman = SimpleNamespace(
        dokuman_id=3,
        yukleyen_kullanici_id=3,
        durum="Aktif",
    )

    monkeypatch.setattr(
        dokuman_router,
        "dokuman_getir",
        lambda db, dokuman_id: dokuman,
    )
    monkeypatch.setattr(
        dokuman_router,
        "dokumani_gorebilir_mi",
        lambda db, kullanici, dokuman_id: False,
    )

    client.app.dependency_overrides[get_db] = sahte_db
    client.app.dependency_overrides[
        get_current_user
    ] = sahte_personel

    response = client.get("/dokumanlar/3")

    assert response.status_code == 403
    assert response.json()["success"] is False
    assert response.json()["error"]["code"] == "FORBIDDEN"
    assert response.json()["path"] == "/dokumanlar/3"