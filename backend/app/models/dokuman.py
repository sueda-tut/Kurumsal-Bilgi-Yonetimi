# Dokümanlar tablosunun SQLAlchemy modelini tanımlar

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Dokuman(Base):
    __tablename__ = "dokumanlar"

    __table_args__ = (
        CheckConstraint(
            "dosya_turu IN ('pdf', 'docs', 'xlsx')",
            name="chk_dokumanlar_dosya_turu",
        ),
        CheckConstraint(
            "surum_no >= 1",
            name="chk_dokumanlar_surum_no",
        ),
        CheckConstraint(
            "durum IN ('Isleniyor', 'Aktif', 'Hata', 'Arsiv')",
            name="chk_dokumanlar_durum",
        ),
        CheckConstraint(
            "dosya_boyutu > 0",
            name="chk_dokumanlar_dosya_boyutu",
        ),
    )

    dokuman_id = Column(Integer, primary_key=True, index=True)

    baslik = Column(
        String(200),
        nullable=False,
    )

    dosya_adi = Column(
        String(255),
        nullable=False,
    )

    dosya_turu = Column(
        String(10),
        nullable=False,
    )

    yukleyen_kullanici_id = Column(
        Integer,
        ForeignKey("kullanicilar.kullanici_id"),
        nullable=False,
        index=True,
    )

    yuklenme_tarihi = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    departman_id = Column(
        Integer,
        ForeignKey("departmanlar.departman_id"),
        nullable=False,
        index=True,
    )

    surum_no = Column(
        Integer,
        nullable=False,
        server_default=text("1"),
    )

    dosya_yolu = Column(
        String(300),
        nullable=False,
        unique=True,
    )

    durum = Column(
        String(20),
        nullable=False,
        server_default=text("'Isleniyor'"),
    )

    dosya_boyutu = Column(
        BigInteger,
        nullable=False,
    )

    guncelleme_tarihi = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    yukleyen_kullanici = relationship(
        "Kullanici",
        back_populates="dokumanlar",
        foreign_keys=[yukleyen_kullanici_id],
    )

    departman = relationship(
        "Departman",
        back_populates="dokumanlar",
        foreign_keys=[departman_id],
    )

    parcalar = relationship(
        "DokumanParcasi",
        back_populates="dokuman",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    etiketler = relationship(
        "DokumanEtiketi",
        back_populates="dokuman",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    yetkiler = relationship(
        "DokumanYetkisi",
        back_populates="dokuman",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )