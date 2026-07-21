# Doküman yükleme, listeleme ve yönetim endpoint'lerini yetki kontrollü sunar

from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.crud.dokuman import (
    dokuman_getir,
    dokumanlari_listele,
    dokumani_arsivle as dokuman_kaydini_arsivle,
    yuklenen_dokumani_olustur,
)
from app.crud.etiket import dokuman_etiketi_olustur
from app.crud.yetki import dokuman_yetkisi_olustur
from app.db.database import get_db
from app.models.kullanici import Kullanici
from app.schemas.dokuman import DokumanResponse
from app.schemas.dokuman_etiketi import (
    DokumanEtiketiResponse,
    EtiketEkleRequest,
)
from app.schemas.dokuman_yetkisi import (
    DokumanYetkisiResponse,
    YetkiEkleRequest,
)
from app.services.dokuman_yetki import (
    dokumani_gorebilir_mi,
    dokumani_yonetebilir_mi,
    gorebildigi_dokuman_idleri,
)


router = APIRouter(
    prefix="/dokumanlar",
    tags=["Dokümanlar"],
)


# Yüklenen dosyaların kaydedileceği klasörü belirler
BACKEND_DIR = Path(__file__).resolve().parents[2]
UPLOADS_DIR = BACKEND_DIR / "uploads"

# En fazla 20 MB dosya yüklenmesine izin verir
MAKSIMUM_DOSYA_BOYUTU = 20 * 1024 * 1024
OKUMA_PARCA_BOYUTU = 1024 * 1024

# Desteklenen uzantıları ve MIME türlerini tanımlar
IZIN_VERILEN_DOSYALAR = {
    ".pdf": {
        "application/pdf",
    },
    ".docx": {
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document",
    },
    ".xlsx": {
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet",
    },
}


# Yeni doküman yüklenmesini sağlar
@router.post(
    "/yukle",
    response_model=DokumanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yeni doküman yükle",
)
async def dokuman_yukle(
    dosya: UploadFile = File(...),
    baslik: str | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    if current_user.departman_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kullanıcının departman bilgisi bulunmuyor.",
        )

    if not dosya.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dosya adı bulunamadı.",
        )

    uzanti = Path(dosya.filename).suffix.lower()

    if uzanti not in IZIN_VERILEN_DOSYALAR:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                "Yalnızca PDF, DOCX ve XLSX "
                "dosyaları yüklenebilir."
            ),
        )

    if dosya.content_type not in IZIN_VERILEN_DOSYALAR[uzanti]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Dosyanın MIME türü uzantısıyla uyumlu değil.",
        )

    UPLOADS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    uuid_dosya_adi = f"{uuid4().hex}{uzanti}"
    kayit_yolu = UPLOADS_DIR / uuid_dosya_adi
    toplam_boyut = 0

    try:
        with kayit_yolu.open("wb") as hedef:
            while parca := await dosya.read(OKUMA_PARCA_BOYUTU):
                toplam_boyut += len(parca)

                if toplam_boyut > MAKSIMUM_DOSYA_BOYUTU:
                    raise HTTPException(
                        status_code=(
                            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
                        ),
                        detail=(
                            "Dosya boyutu en fazla "
                            "20 MB olabilir."
                        ),
                    )

                hedef.write(parca)

        if toplam_boyut <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Boş dosya yüklenemez.",
            )

        dokuman_basligi = (
            baslik.strip()
            if baslik and baslik.strip()
            else Path(dosya.filename).stem
        )

        yeni_dokuman = yuklenen_dokumani_olustur(
            db=db,
            baslik=dokuman_basligi,
            dosya_adi=uuid_dosya_adi,
            dosya_turu=uzanti.removeprefix("."),
            dosya_yolu=f"/uploads/{uuid_dosya_adi}",
            dosya_boyutu=toplam_boyut,
            yukleyen_kullanici_id=(
                current_user.kullanici_id
            ),
            departman_id=current_user.departman_id,
        )

        return yeni_dokuman

    except HTTPException:
        if kayit_yolu.exists():
            kayit_yolu.unlink()

        raise

    except SQLAlchemyError as error:
        db.rollback()

        if kayit_yolu.exists():
            kayit_yolu.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Doküman veritabanına kaydedilemedi.",
        ) from error

    except OSError as error:
        if kayit_yolu.exists():
            kayit_yolu.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dosya diske kaydedilemedi.",
        ) from error

    finally:
        await dosya.close()


# Yönetici veya yükleyenin dokümana etiket eklemesini sağlar
@router.post(
    "/{dokuman_id}/etiket",
    response_model=DokumanEtiketiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Dokümana etiket ekle",
)
def dokumana_etiket_ekle(
    dokuman_id: int,
    etiket_verisi: EtiketEkleRequest,
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    dokuman = dokuman_getir(
        db=db,
        dokuman_id=dokuman_id,
    )

    if dokuman is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doküman bulunamadı.",
        )

    if not dokumani_yonetebilir_mi(
        kullanici=current_user,
        dokuman=dokuman,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu dokümanı yönetme yetkiniz yok.",
        )

    if not etiket_verisi.etiket_adi.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Etiket adı boş olamaz.",
        )

    try:
        return dokuman_etiketi_olustur(
            db=db,
            dokuman_id=dokuman_id,
            etiket_adi=etiket_verisi.etiket_adi,
        )

    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu etiket dokümana daha önce eklenmiş.",
        ) from error


# Yönetici veya yükleyenin departman yetkisi eklemesini sağlar
@router.post(
    "/{dokuman_id}/yetki",
    response_model=DokumanYetkisiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Dokümana departman yetkisi ekle",
)
def dokumana_yetki_ekle(
    dokuman_id: int,
    yetki_verisi: YetkiEkleRequest,
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    dokuman = dokuman_getir(
        db=db,
        dokuman_id=dokuman_id,
    )

    if dokuman is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doküman bulunamadı.",
        )

    if not dokumani_yonetebilir_mi(
        kullanici=current_user,
        dokuman=dokuman,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu dokümanı yönetme yetkiniz yok.",
        )

    try:
        return dokuman_yetkisi_olustur(
            db=db,
            dokuman_id=dokuman_id,
            departman_id=yetki_verisi.departman_id,
            goruntuleyebilir_mi=(
                yetki_verisi.goruntuleyebilir_mi
            ),
        )

    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Departman bulunamadı veya bu departmana "
                "daha önce yetki verilmiş."
            ),
        ) from error


# Yönetici veya yükleyenin dokümanı arşivlemesini sağlar
@router.patch(
    "/{dokuman_id}/arsivle",
    response_model=DokumanResponse,
    summary="Dokümanı arşivle",
)
def dokuman_arsivle(
    dokuman_id: int,
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    dokuman = dokuman_getir(
        db=db,
        dokuman_id=dokuman_id,
    )

    if dokuman is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doküman bulunamadı.",
        )

    if not dokumani_yonetebilir_mi(
        kullanici=current_user,
        dokuman=dokuman,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu dokümanı yönetme yetkiniz yok.",
        )

    if dokuman.durum.casefold() == "arsiv":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Doküman zaten arşivlenmiş.",
        )

    return dokuman_kaydini_arsivle(
        db=db,
        dokuman=dokuman,
    )


# Kullanıcının görebildiği arşivlenmemiş dokümanları listeler
@router.get(
    "",
    response_model=list[DokumanResponse],
    summary="Yetkiye göre doküman listesi",
)
def dokuman_listesi(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    gorulebilir_idler = gorebildigi_dokuman_idleri(
        db=db,
        kullanici=current_user,
    )

    return dokumanlari_listele(
        db=db,
        gorulebilir_dokuman_idleri=gorulebilir_idler,
        offset=offset,
        limit=limit,
    )


# Yetki kontrolünden sonra doküman detayını döndürür
@router.get(
    "/{dokuman_id}",
    response_model=DokumanResponse,
    summary="Yetki kontrollü doküman detayı",
)
def dokuman_detayi(
    dokuman_id: int,
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    dokuman = dokuman_getir(
        db=db,
        dokuman_id=dokuman_id,
    )

    if dokuman is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doküman bulunamadı.",
        )

    if not dokumani_gorebilir_mi(
        db=db,
        kullanici=current_user,
        dokuman_id=dokuman_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu dokümanı görüntüleme yetkiniz yok.",
        )

    return dokuman