# Doküman parçaları ve pgvector embedding alanının SQLAlchemy modelini tanımlar

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class DokumanParcasi(Base):
    __tablename__ = "dokuman_parcalari"

    __table_args__ = (
        UniqueConstraint(
            "dokuman_id",
            "parca_sirasi",
            name="uq_dokuman_parcalari_dokuman_parca",
        ),
        CheckConstraint(
            "parca_sirasi >= 1",
            name="chk_dokuman_parcalari_parca_sirasi",
        ),
        CheckConstraint(
            "sayfa_no IS NULL OR sayfa_no >= 1",
            name="chk_dokuman_parcalari_sayfa_no",
        ),
        CheckConstraint(
            "token_sayisi > 0",
            name="chk_dokuman_parcalari_token_sayisi",
        ),
    )

    parca_id = Column(Integer, primary_key=True, index=True)

    dokuman_id = Column(
        Integer,
        ForeignKey(
            "dokumanlar.dokuman_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    parca_sirasi = Column(
        Integer,
        nullable=False,
    )

    parca_metni = Column(
        Text,
        nullable=False,
    )

    sayfa_no = Column(
        Integer,
        nullable=True,
    )

    token_sayisi = Column(
        Integer,
        nullable=False,
    )

    embedding = Column(
        Vector(1536),
        nullable=True,
    )

    olusturulma_tarihi = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    dokuman = relationship(
        "Dokuman",
        back_populates="parcalar",
    )

    mesaj_kaynaklari = relationship(
        "MesajKaynagi",
        back_populates="parca",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )