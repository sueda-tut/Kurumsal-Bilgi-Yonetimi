# Kullanıcı tablosuna ait temel CRUD işlemlerini gerçekleştirir

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import sifre_ozeti_olustur
from app.models.kullanici import Kullanici
from app.schemas.kullanici import KullaniciCreate


def kullanici_getir(
    db: Session,
    kullanici_id: int,
) -> Kullanici | None:
    sorgu = select(Kullanici).where(
        Kullanici.kullanici_id == kullanici_id
    )

    return db.scalar(sorgu)


def kullanicilari_listele(
    db: Session,
    offset: int = 0,
    limit: int = 100,
) -> list[Kullanici]:
    sorgu = (
        select(Kullanici)
        .order_by(Kullanici.kullanici_id)
        .offset(offset)
        .limit(limit)
    )

    return list(db.scalars(sorgu).all())


def eposta_ile_kullanici_bul(
    db: Session,
    eposta: str,
) -> Kullanici | None:
    sorgu = select(Kullanici).where(
        Kullanici.eposta == eposta
    )

    return db.scalar(sorgu)


def kullanici_olustur(
    db: Session,
    kullanici_verisi: KullaniciCreate,
) -> Kullanici:
    yeni_kullanici = Kullanici(
        ad_soyad=kullanici_verisi.ad_soyad,
        eposta=str(kullanici_verisi.eposta),
        sifre_ozeti=sifre_ozeti_olustur(
            kullanici_verisi.sifre
        ),
        rol=kullanici_verisi.rol,
        departman_id=kullanici_verisi.departman_id,
        aktif_mi=kullanici_verisi.aktif_mi,
    )

    db.add(yeni_kullanici)
    db.commit()
    db.refresh(yeni_kullanici)

    return yeni_kullanici