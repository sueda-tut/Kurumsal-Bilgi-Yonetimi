# Sohbet oturumu ve mesajlarına ait veritabanı işlemlerini gerçekleştirir

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sohbet_mesaji import SohbetMesaji
from app.models.sohbet_oturumu import SohbetOturumu


# Token sahibi kullanıcı için yeni sohbet oturumu oluşturur
def sohbet_oturumu_olustur(
    db: Session,
    kullanici_id: int,
    oturum_basligi: str,
) -> SohbetOturumu:
    yeni_oturum = SohbetOturumu(
        kullanici_id=kullanici_id,
        oturum_basligi=oturum_basligi.strip(),
    )

    db.add(yeni_oturum)
    db.commit()
    db.refresh(yeni_oturum)

    return yeni_oturum


# Kullanıcının kendi sohbet oturumlarını listeler
def kullanicinin_oturumlarini_listele(
    db: Session,
    kullanici_id: int,
) -> list[SohbetOturumu]:
    sorgu = (
        select(SohbetOturumu)
        .where(
            SohbetOturumu.kullanici_id == kullanici_id
        )
        .order_by(SohbetOturumu.oturum_id.desc())
    )

    return list(db.scalars(sorgu).all())


# Sohbet oturumunu ID üzerinden getirir
def sohbet_oturumu_getir(
    db: Session,
    oturum_id: int,
) -> SohbetOturumu | None:
    sorgu = select(SohbetOturumu).where(
        SohbetOturumu.oturum_id == oturum_id
    )

    return db.scalar(sorgu)


# Belirtilen sohbet oturumundaki mesajları listeler
def oturumun_mesajlarini_listele(
    db: Session,
    oturum_id: int,
) -> list[SohbetMesaji]:
    sorgu = (
        select(SohbetMesaji)
        .where(SohbetMesaji.oturum_id == oturum_id)
        .order_by(SohbetMesaji.mesaj_id)
    )

    return list(db.scalars(sorgu).all())


# Sohbet oturumuna kullanıcı mesajı ekler
def sohbet_mesaji_olustur(
    db: Session,
    oturum_id: int,
    mesaj_metni: str,
) -> SohbetMesaji:
    yeni_mesaj = SohbetMesaji(
        oturum_id=oturum_id,
        gonderen_tipi="Kullanici",
        mesaj_metni=mesaj_metni.strip(),
    )

    db.add(yeni_mesaj)
    db.commit()
    db.refresh(yeni_mesaj)

    return yeni_mesaj