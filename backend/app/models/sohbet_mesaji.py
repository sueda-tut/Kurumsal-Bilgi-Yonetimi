from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class SohbetMesaji(Base):
    __tablename__ = "sohbet_mesajlari"

    mesaj_id = Column(Integer, primary_key=True, index=True)
    oturum_id = Column(
        Integer,
        ForeignKey("sohbet_oturumlari.oturum_id"),
        nullable=False
    )
    gonderen_tipi = Column(String(20), nullable=False)
    mesaj_metni = Column(Text, nullable=False)
    olusturulma_tarihi = Column(DateTime, nullable=False, server_default=func.now())

    oturum = relationship(
        "SohbetOturumu",
        back_populates="mesajlar"
    )