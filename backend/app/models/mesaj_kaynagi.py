# AI mesajları ile kaynak doküman parçaları arasındaki ilişkiyi tanımlar

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class MesajKaynagi(Base):
    __tablename__ = "mesaj_kaynaklari"

    __table_args__ = (
        UniqueConstraint(
            "mesaj_id",
            "parca_id",
            name="uq_mesaj_kaynaklari_mesaj_parca",
        ),
        CheckConstraint(
            "benzerlik_puani >= 0 AND benzerlik_puani <= 1",
            name="chk_mesaj_kaynaklari_benzerlik_puani",
        ),
    )

    kaynak_id = Column(Integer, primary_key=True, index=True)

    mesaj_id = Column(
        Integer,
        ForeignKey(
            "sohbet_mesajlari.mesaj_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    parca_id = Column(
        Integer,
        ForeignKey(
            "dokuman_parcalari.parca_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    benzerlik_puani = Column(
        Numeric(5, 4),
        nullable=False,
    )

    mesaj = relationship(
        "SohbetMesaji",
        back_populates="kaynaklar",
    )

    parca = relationship(
        "DokumanParcasi",
        back_populates="mesaj_kaynaklari",
    )