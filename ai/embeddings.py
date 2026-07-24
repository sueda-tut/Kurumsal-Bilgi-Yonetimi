# OpenAI API kullanarak doküman parçaları için embedding vektörleri üretir

import os

from openai import OpenAI, OpenAIError


EMBEDDING_MODELI = "text-embedding-3-small"
EMBEDDING_BOYUTU = 1536
EMBEDDING_BATCH_BOYUTU = 100


class EmbeddingUretmeHatasi(Exception):
    """Embedding üretimi başarısız olduğunda oluşur."""


def embeddingleri_uret(
    metinler: list[str],
) -> list[list[float]]:
    """Metinleri gruplar hâlinde OpenAI embedding vektörlerine dönüştürür."""

    if not metinler:
        return []

    if not os.getenv("OPENAI_API_KEY"):
        raise EmbeddingUretmeHatasi(
            "OPENAI_API_KEY ortam değişkeni bulunamadı."
        )

    if any(not metin.strip() for metin in metinler):
        raise EmbeddingUretmeHatasi(
            "Boş metin için embedding üretilemez."
        )

    istemci = OpenAI()
    tum_embeddingler: list[list[float]] = []

    try:
        for baslangic in range(
            0,
            len(metinler),
            EMBEDDING_BATCH_BOYUTU,
        ):
            metin_grubu = metinler[
                baslangic:
                baslangic + EMBEDDING_BATCH_BOYUTU
            ]

            cevap = istemci.embeddings.create(
                model=EMBEDDING_MODELI,
                input=metin_grubu,
                encoding_format="float",
                dimensions=EMBEDDING_BOYUTU,
            )

            sirali_sonuclar = sorted(
                cevap.data,
                key=lambda sonuc: sonuc.index,
            )

            grup_embeddingleri = [
                sonuc.embedding
                for sonuc in sirali_sonuclar
            ]

            if len(grup_embeddingleri) != len(metin_grubu):
                raise EmbeddingUretmeHatasi(
                    "OpenAI beklenen sayıda embedding döndürmedi."
                )

            for embedding in grup_embeddingleri:
                if len(embedding) != EMBEDDING_BOYUTU:
                    raise EmbeddingUretmeHatasi(
                        "Embedding boyutu 1536 değil."
                    )

            tum_embeddingler.extend(grup_embeddingleri)

    except EmbeddingUretmeHatasi:
        raise

    except OpenAIError as hata:
        raise EmbeddingUretmeHatasi(
            "OpenAI API üzerinden embedding üretilemedi."
        ) from hata

    if len(tum_embeddingler) != len(metinler):
        raise EmbeddingUretmeHatasi(
            "Metin ve embedding sayıları eşleşmiyor."
        )

    return tum_embeddingler