# Doküman tablosuna ait temel CRUD işlemlerini gerçekleştirir

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.dokuman import Dokuman
from app.schemas.dokuman import (
    DokumanCreate,
    DokumanDurumu,
)


def dokuman_getir(
    db: Session,
    dokuman_id: int,
) -> Dokuman | None:
    sorgu = select(Dokuman).where(
        Dokuman.dokuman_id == dokuman_id
    )

    return db.scalar(sorgu)


# Kullanıcının görebildiği dokümanları sayfalayarak listeler

def dokumanlari_listele(
    db: Session,
    gorulebilir_dokuman_idleri: list[int],
    offset: int = 0,
    limit: int = 100,
) -> list[Dokuman]:
    if not gorulebilir_dokuman_idleri:
        return []

    sorgu = (
        select(Dokuman)
        .where(
            Dokuman.dokuman_id.in_(
                gorulebilir_dokuman_idleri
            )
        )
        .order_by(Dokuman.dokuman_id)
        .offset(offset)
        .limit(limit)
    )

    return list(db.scalars(sorgu).all())


def dokuman_olustur(
    db: Session,
    dokuman_verisi: DokumanCreate,
) -> Dokuman:
    yeni_dokuman = Dokuman(
        **dokuman_verisi.model_dump()
    )

    db.add(yeni_dokuman)
    db.commit()
    db.refresh(yeni_dokuman)

    return yeni_dokuman


def dokuman_durumu_guncelle(
    db: Session,
    dokuman_id: int,
    yeni_durum: DokumanDurumu,
) -> Dokuman | None:
    dokuman = dokuman_getir(
        db=db,
        dokuman_id=dokuman_id,
    )

    if dokuman is None:
        return None

    dokuman.durum = yeni_durum

    db.commit()
    db.refresh(dokuman)

    return dokuman