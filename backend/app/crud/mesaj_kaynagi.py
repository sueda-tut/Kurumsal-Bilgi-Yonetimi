# AI mesajlarının kullandığı doküman parçalarını mesaj_kaynaklari tablosuna kaydeder

from sqlalchemy.orm import Session

from app.models.mesaj_kaynagi import MesajKaynagi


# AI mesajı ile kullanılan doküman parçası arasında kaynak kaydı oluşturur
def mesaj_kaynagi_olustur(
    db: Session,
    mesaj_id: int,
    parca_id: int,
    benzerlik_puani: float,
    commit: bool = True,
) -> MesajKaynagi:
    # Numeric(5, 4) ve CHECK sınırına uygun değer oluşturur
    sinirli_puan = max(
        0.0,
        min(1.0, float(benzerlik_puani)),
    )

    yeni_kaynak = MesajKaynagi(
        mesaj_id=mesaj_id,
        parca_id=parca_id,
        benzerlik_puani=round(sinirli_puan, 4),
    )

    db.add(yeni_kaynak)

    if commit:
        db.commit()
        db.refresh(yeni_kaynak)
    else:
        db.flush()

    return yeni_kaynak