# Doküman parçalarını veritabanına kaydeden CRUD işlemlerini gerçekleştirir

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from ai.chunking import ParcaTaslagi
from app.models.dokuman import Dokuman
from app.models.dokuman_parcasi import DokumanParcasi


def dokuman_parcalarini_kaydet(
    db: Session,
    dokuman: Dokuman,
    parcalar: list[ParcaTaslagi],
) -> list[DokumanParcasi]:
    """Dokümanın eski parçalarını silip yeni parçalarını kaydeder."""

    db.execute(
        delete(DokumanParcasi).where(
            DokumanParcasi.dokuman_id
            == dokuman.dokuman_id
        )
    )

    kayitlar = [
        DokumanParcasi(
            dokuman_id=dokuman.dokuman_id,
            parca_sirasi=parca_sirasi,
            parca_metni=parca.parca_metni,
            sayfa_no=parca.sayfa_no,
            token_sayisi=parca.token_sayisi,
            embedding=None,
        )
        for parca_sirasi, parca in enumerate(
            parcalar,
            start=1,
        )
    ]

    db.add_all(kayitlar)
    dokuman.durum = "Aktif"
    db.commit()

    for kayit in kayitlar:
        db.refresh(kayit)

    return kayitlar


def dokuman_parcalarini_listele(
    db: Session,
    dokuman_id: int,
) -> list[DokumanParcasi]:
    """Bir dokümana ait parçaları sırasıyla listeler."""

    sorgu = (
        select(DokumanParcasi)
        .where(
            DokumanParcasi.dokuman_id == dokuman_id
        )
        .order_by(DokumanParcasi.parca_sirasi)
    )

    return list(db.scalars(sorgu).all())