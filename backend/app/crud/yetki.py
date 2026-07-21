# Departman bazlı doküman yetkileri için temel CRUD işlemlerini gerçekleştirir

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.dokuman_yetkisi import DokumanYetkisi
from app.schemas.dokuman_yetkisi import (
    DokumanYetkisiCreate,
    DokumanYetkisiUpdate,
)


def yetki_getir(
    db: Session,
    yetki_id: int,
) -> DokumanYetkisi | None:
    sorgu = select(DokumanYetkisi).where(
        DokumanYetkisi.yetki_id == yetki_id
    )

    return db.scalar(sorgu)


def dokumanin_yetkilerini_listele(
    db: Session,
    dokuman_id: int,
) -> list[DokumanYetkisi]:
    sorgu = (
        select(DokumanYetkisi)
        .where(
            DokumanYetkisi.dokuman_id == dokuman_id
        )
        .order_by(DokumanYetkisi.yetki_id)
    )

    return list(db.scalars(sorgu).all())


def yetki_olustur(
    db: Session,
    yetki_verisi: DokumanYetkisiCreate,
) -> DokumanYetkisi:
    yeni_yetki = DokumanYetkisi(
        **yetki_verisi.model_dump()
    )

    db.add(yeni_yetki)
    db.commit()
    db.refresh(yeni_yetki)

    return yeni_yetki


def yetki_guncelle(
    db: Session,
    yetki_id: int,
    yetki_verisi: DokumanYetkisiUpdate,
) -> DokumanYetkisi | None:
    yetki = yetki_getir(
        db=db,
        yetki_id=yetki_id,
    )

    if yetki is None:
        return None

    yetki.goruntuleyebilir_mi = (
        yetki_verisi.goruntuleyebilir_mi
    )

    db.commit()
    db.refresh(yetki)

    return yetki

# Doküman ile departman arasında görüntüleme yetkisi oluşturur
def dokuman_yetkisi_olustur(
    db: Session,
    dokuman_id: int,
    departman_id: int,
    goruntuleyebilir_mi: bool,
) -> DokumanYetkisi:
    yeni_yetki = DokumanYetkisi(
        dokuman_id=dokuman_id,
        departman_id=departman_id,
        goruntuleyebilir_mi=goruntuleyebilir_mi,
    )

    db.add(yeni_yetki)
    db.commit()
    db.refresh(yeni_yetki)

    return yeni_yetki