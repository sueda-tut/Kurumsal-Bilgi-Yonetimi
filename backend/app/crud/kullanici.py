from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.kullanici import Kullanici
from app.schemas.kullanici import KullaniciCreate, KullaniciUpdate 

def kullanici_id_ile_getir(db: Session, kullanici_id: int) -> Kullanici | None:
    sorgu = select(Kullanici).where(Kullanici.kullanici_id == kullanici_id)
    return db.execute(sorgu).scalar_one_or_none()


def eposta_ile_kullanici_getir(db: Session, eposta: str) -> Kullanici | None:
    sorgu = select(Kullanici).where(Kullanici.eposta == eposta)
    return db.execute(sorgu).scalar_one_or_none()


def kullanicilari_listele(db: Session) -> list[Kullanici]:
    sorgu = select(Kullanici).order_by(Kullanici.kullanici_id)
    return list(db.execute(sorgu).scalars().all())


def kullanici_olustur(
    db: Session,
    kullanici_verisi: KullaniciCreate,
    sifre_ozeti: str
) -> Kullanici:
    yeni_kullanici = Kullanici(
        ad_soyad=kullanici_verisi.ad_soyad,
        eposta=kullanici_verisi.eposta,
        sifre_ozeti=sifre_ozeti,
        rol=kullanici_verisi.rol,
        departman=kullanici_verisi.departman
    )

    db.add(yeni_kullanici)
    db.commit()
    db.refresh(yeni_kullanici)

    return yeni_kullanici

def kullanici_guncelle(
    db: Session,
    kullanici: Kullanici,
    guncel_veriler: KullaniciUpdate,
    yeni_sifre_ozeti: str | None = None
) -> Kullanici:
    degisiklikler = guncel_veriler.model_dump(exclude_unset=True)

    sifre = degisiklikler.pop("sifre", None)

    for alan_adi, yeni_deger in degisiklikler.items():
        setattr(kullanici, alan_adi, yeni_deger)

    if sifre is not None and yeni_sifre_ozeti is not None:
        kullanici.sifre_ozeti = yeni_sifre_ozeti

    db.commit()
    db.refresh(kullanici)

    return kullanici

def kullanici_sil(
    db: Session,
    kullanici: Kullanici
) -> None:
    db.delete(kullanici)
    db.commit()