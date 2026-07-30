# Kullanıcının geçmiş sohbet mesajlarını kaynaklarıyla birlikte getirir

from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.dokuman import Dokuman
from app.models.dokuman_parcasi import DokumanParcasi
from app.models.kullanici import Kullanici
from app.models.mesaj_kaynagi import MesajKaynagi
from app.models.sohbet_mesaji import SohbetMesaji
from app.models.sohbet_oturumu import SohbetOturumu
from app.schemas.sohbet_gecmisi import (
    GecmisMesajKaynagiResponse,
    GecmisMesajResponse,
)


router = APIRouter(
    prefix="/sohbetler",
    tags=["Sohbet Geçmişi"],
)


@router.get(
    "/{oturum_id}/detay",
    response_model=list[GecmisMesajResponse],
    summary="Sohbet mesajlarını kaynaklarıyla getirir",
)
def sohbet_detayi_getir(
    oturum_id: int,
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    oturum = db.scalar(
        select(SohbetOturumu).where(
            SohbetOturumu.oturum_id == oturum_id
        )
    )

    if oturum is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sohbet oturumu bulunamadı.",
        )

    if oturum.kullanici_id != current_user.kullanici_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu sohbet oturumunu görüntüleme yetkiniz yok.",
        )

    mesajlar = list(
        db.scalars(
            select(SohbetMesaji)
            .where(SohbetMesaji.oturum_id == oturum_id)
            .order_by(SohbetMesaji.mesaj_id)
        ).all()
    )

    mesaj_idleri = [
        mesaj.mesaj_id
        for mesaj in mesajlar
    ]

    kaynaklar_by_mesaj: dict[
        int,
        list[GecmisMesajKaynagiResponse],
    ] = defaultdict(list)

    if mesaj_idleri:
        kaynak_satirlari = db.execute(
            select(
                MesajKaynagi,
                DokumanParcasi,
                Dokuman,
            )
            .join(
                DokumanParcasi,
                MesajKaynagi.parca_id
                == DokumanParcasi.parca_id,
            )
            .join(
                Dokuman,
                DokumanParcasi.dokuman_id
                == Dokuman.dokuman_id,
            )
            .where(
                MesajKaynagi.mesaj_id.in_(mesaj_idleri)
            )
            .order_by(MesajKaynagi.kaynak_id)
        ).all()

        for kaynak, parca, dokuman in kaynak_satirlari:
            kaynaklar_by_mesaj[kaynak.mesaj_id].append(
                GecmisMesajKaynagiResponse(
                    kaynak_id=kaynak.kaynak_id,
                    dokuman_id=dokuman.dokuman_id,
                    dokuman_basligi=dokuman.baslik,
                    parca_id=parca.parca_id,
                    parca_sirasi=parca.parca_sirasi,
                    sayfa_no=parca.sayfa_no,
                    benzerlik_puani=kaynak.benzerlik_puani,
                )
            )

    return [
        GecmisMesajResponse(
            mesaj_id=mesaj.mesaj_id,
            oturum_id=mesaj.oturum_id,
            gonderen_tipi=mesaj.gonderen_tipi,
            mesaj_metni=mesaj.mesaj_metni,
            olusturulma_tarihi=mesaj.olusturulma_tarihi,
            kaynaklar=kaynaklar_by_mesaj.get(
                mesaj.mesaj_id,
                [],
            ),
        )
        for mesaj in mesajlar
    ]