# Sohbet oturumları ve mesajları için temel CRUD işlemlerini gerçekleştirir

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sohbet_mesaji import SohbetMesaji
from app.models.sohbet_oturumu import SohbetOturumu
from app.schemas.sohbet_mesaji import SohbetMesajiCreate
from app.schemas.sohbet_oturumu import SohbetOturumuCreate


def sohbet_oturumu_getir(
    db: Session,
    oturum_id: int,
) -> SohbetOturumu | None:
    sorgu = select(SohbetOturumu).where(
        SohbetOturumu.oturum_id == oturum_id
    )

    return db.scalar(sorgu)


def sohbet_oturumu_olustur(
    db: Session,
    oturum_verisi: SohbetOturumuCreate,
) -> SohbetOturumu:
    yeni_oturum = SohbetOturumu(
        **oturum_verisi.model_dump()
    )

    db.add(yeni_oturum)
    db.commit()
    db.refresh(yeni_oturum)

    return yeni_oturum


def kullanicinin_oturumlarini_listele(
    db: Session,
    kullanici_id: int,
) -> list[SohbetOturumu]:
    sorgu = (
        select(SohbetOturumu)
        .where(
            SohbetOturumu.kullanici_id == kullanici_id
        )
        .order_by(SohbetOturumu.oturum_id)
    )

    return list(db.scalars(sorgu).all())


def oturumun_mesajlarini_listele(
    db: Session,
    oturum_id: int,
) -> list[SohbetMesaji]:
    sorgu = (
        select(SohbetMesaji)
        .where(
            SohbetMesaji.oturum_id == oturum_id
        )
        .order_by(SohbetMesaji.mesaj_id)
    )

    return list(db.scalars(sorgu).all())


def mesaj_ekle(
    db: Session,
    mesaj_verisi: SohbetMesajiCreate,
) -> SohbetMesaji:
    yeni_mesaj = SohbetMesaji(
        **mesaj_verisi.model_dump()
    )

    db.add(yeni_mesaj)
    db.commit()
    db.refresh(yeni_mesaj)

    return yeni_mesaj