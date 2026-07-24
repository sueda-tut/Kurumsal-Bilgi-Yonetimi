# Yüklenen dokümandan metin çıkarıp parçalara ayırarak veritabanına kaydeder

from pathlib import Path

from sqlalchemy.orm import Session

from ai.chunking import bolumleri_parcalara_ayir
from ai.extractors import dosyadan_metin_cikar
from app.crud.dokuman_parcasi import (
    dokuman_parcalarini_kaydet,
)
from app.models.dokuman import Dokuman
from app.models.dokuman_parcasi import DokumanParcasi


class DokumanIslemeHatasi(Exception):
    """Doküman metni çıkarılamadığında veya parçalanamadığında oluşur."""


def dokumani_isle(
    db: Session,
    dokuman: Dokuman,
    fiziksel_dosya_yolu: str | Path,
) -> list[DokumanParcasi]:
    """Dosyayı okur, chunk oluşturur ve veritabanına kaydeder."""

    try:
        bolumler = dosyadan_metin_cikar(
            fiziksel_dosya_yolu
        )

        if not bolumler:
            raise DokumanIslemeHatasi(
                "Dosyadan okunabilir metin çıkarılamadı."
            )

        parcalar = bolumleri_parcalara_ayir(bolumler)

        if not parcalar:
            raise DokumanIslemeHatasi(
                "Doküman parçaları oluşturulamadı."
            )

        return dokuman_parcalarini_kaydet(
            db=db,
            dokuman=dokuman,
            parcalar=parcalar,
        )

    except DokumanIslemeHatasi:
        raise

    except Exception as hata:
        db.rollback()

        raise DokumanIslemeHatasi(
            "Doküman işlenirken beklenmeyen bir hata oluştu."
        ) from hata