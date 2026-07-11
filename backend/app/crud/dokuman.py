from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models.dokuman import Dokuman
from app.schemas.dokuman import DokumanCreate, DokumanUpdate


def dokuman_id_ile_getir(
    db: Session,
    dokuman_id: int
) -> Dokuman | None:
    sorgu = select(Dokuman).where(
        Dokuman.dokuman_id == dokuman_id
    )

    return db.execute(sorgu).scalar_one_or_none()


def dokumanlari_listele(
    db: Session,
    departman: str | None = None,
    dosya_turu: str | None = None,
    durum: str | None = None
) -> list[Dokuman]:
    sorgu = select(Dokuman)

    if departman is not None:
        sorgu = sorgu.where(Dokuman.departman == departman)

    if dosya_turu is not None:
        sorgu = sorgu.where(Dokuman.dosya_turu == dosya_turu)

    if durum is not None:
        sorgu = sorgu.where(Dokuman.durum == durum)

    sorgu = sorgu.order_by(Dokuman.yuklenme_tarihi.desc())

    return list(db.execute(sorgu).scalars().all())


def dokuman_olustur(
    db: Session,
    dokuman_verisi: DokumanCreate,
    dosya_adi: str,
    dosya_turu: str,
    dosya_yolu: str
) -> Dokuman:
    yeni_dokuman = Dokuman(
        baslik=dokuman_verisi.baslik,
        dosya_adi=dosya_adi,
        dosya_turu=dosya_turu,
        yukleyen_kullanici_id=dokuman_verisi.yukleyen_kullanici_id,
        departman=dokuman_verisi.departman,
        surum_no=1,
        dosya_yolu=dosya_yolu,
        durum="Isleniyor"
    )

    db.add(yeni_dokuman)
    db.commit()
    db.refresh(yeni_dokuman)

    return yeni_dokuman


def dokuman_guncelle(
    db: Session,
    dokuman: Dokuman,
    guncel_veriler: DokumanUpdate
) -> Dokuman:
    degisiklikler = guncel_veriler.model_dump(exclude_unset=True)

    for alan_adi, yeni_deger in degisiklikler.items():
        setattr(dokuman, alan_adi, yeni_deger)

    db.commit()
    db.refresh(dokuman)

    return dokuman


def dokuman_arsivle(
    db: Session,
    dokuman_id: int
) -> Dokuman | None:
    dokuman = dokuman_id_ile_getir(db, dokuman_id)

    if dokuman is None:
        return None

    db.execute(
        text("CALL sp_dokuman_arsivle(:dokuman_id)"),
        {"dokuman_id": dokuman_id}
    )
    db.commit()
    db.refresh(dokuman)

    return dokuman


def dokuman_aktiflestir(
    db: Session,
    dokuman_id: int
) -> Dokuman | None:
    dokuman = dokuman_id_ile_getir(db, dokuman_id)

    if dokuman is None:
        return None

    db.execute(
        text("CALL sp_dokuman_geri_aktiflestir(:dokuman_id)"),
        {"dokuman_id": dokuman_id}
    )
    db.commit()
    db.refresh(dokuman)

    return dokuman