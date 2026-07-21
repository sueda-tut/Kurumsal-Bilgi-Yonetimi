# Kullanıcının görüntüleyebileceği dokümanları merkezi olarak belirler

from sqlalchemy import exists, or_, select
from sqlalchemy.orm import Session

from app.models.dokuman import Dokuman
from app.models.dokuman_yetkisi import DokumanYetkisi
from app.models.kullanici import Kullanici


def yonetici_mi(kullanici: Kullanici) -> bool:
    rol = (kullanici.rol or "").strip().casefold()

    return rol in {
        "yonetici",
        "yönetici",
    }


def gorebildigi_dokuman_idleri(
    db: Session,
    kullanici: Kullanici,
) -> list[int]:
    """
    Kullanıcının görebileceği doküman kimliklerini döndürür.

    Kurallar:
    - Yönetici bütün dokümanları görür.
    - Personel kendi yüklediği dokümanları görür.
    - Personel kendi departmanına yetki verilmiş dokümanları görür.
    """

    if yonetici_mi(kullanici):
        sorgu = (
            select(Dokuman.dokuman_id)
            .order_by(Dokuman.dokuman_id)
        )

        return list(db.scalars(sorgu).all())

    kosullar = [
        Dokuman.yukleyen_kullanici_id == kullanici.kullanici_id
    ]

    if kullanici.departman_id is not None:
        departman_yetkisi_var = exists(
            select(DokumanYetkisi.yetki_id).where(
                DokumanYetkisi.dokuman_id
                == Dokuman.dokuman_id,
                DokumanYetkisi.departman_id
                == kullanici.departman_id,
                DokumanYetkisi.goruntuleyebilir_mi.is_(True),
            )
        )

        kosullar.append(departman_yetkisi_var)

    sorgu = (
        select(Dokuman.dokuman_id)
        .where(or_(*kosullar))
        .order_by(Dokuman.dokuman_id)
    )

    return list(db.scalars(sorgu).all())


def dokumani_gorebilir_mi(
    db: Session,
    kullanici: Kullanici,
    dokuman_id: int,
) -> bool:
    gorulebilir_idler = gorebildigi_dokuman_idleri(
        db=db,
        kullanici=kullanici,
    )

    return dokuman_id in set(gorulebilir_idler)

# Kullanıcının doküman üzerinde yönetim işlemi yapıp yapamayacağını belirler

def dokumani_yonetebilir_mi(
    kullanici: Kullanici,
    dokuman: Dokuman,
) -> bool:
    return (
        yonetici_mi(kullanici)
        or dokuman.yukleyen_kullanici_id
        == kullanici.kullanici_id
    )