# Doküman etiketleri için temel CRUD işlemlerini gerçekleştirir

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.dokuman_etiketi import DokumanEtiketi
from app.schemas.dokuman_etiketi import DokumanEtiketiCreate


def etiket_getir(
    db: Session,
    dokuman_etiket_id: int,
) -> DokumanEtiketi | None:
    sorgu = select(DokumanEtiketi).where(
        DokumanEtiketi.dokuman_etiket_id
        == dokuman_etiket_id
    )

    return db.scalar(sorgu)


def dokumanin_etiketlerini_listele(
    db: Session,
    dokuman_id: int,
) -> list[DokumanEtiketi]:
    sorgu = (
        select(DokumanEtiketi)
        .where(
            DokumanEtiketi.dokuman_id == dokuman_id
        )
        .order_by(
            DokumanEtiketi.dokuman_etiket_id
        )
    )

    return list(db.scalars(sorgu).all())


def etiket_olustur(
    db: Session,
    etiket_verisi: DokumanEtiketiCreate,
) -> DokumanEtiketi:
    yeni_etiket = DokumanEtiketi(
        **etiket_verisi.model_dump()
    )

    db.add(yeni_etiket)
    db.commit()
    db.refresh(yeni_etiket)

    return yeni_etiket