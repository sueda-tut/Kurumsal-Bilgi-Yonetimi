# Çıkarılan metinleri token tabanlı ve örtüşmeli parçalara ayırır

from collections import OrderedDict
from dataclasses import dataclass

import tiktoken
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from ai.extractors import MetinBolumu


HEDEF_TOKEN_SAYISI = 600
OVERLAP_TOKEN_SAYISI = 75
TOKEN_ENCODING_ADI = "cl100k_base"

tokenizer = tiktoken.get_encoding(TOKEN_ENCODING_ADI)


@dataclass(frozen=True, slots=True)
class ParcaTaslagi:
    parca_metni: str
    sayfa_no: int | None
    token_sayisi: int


def token_sayisini_hesapla(metin: str) -> int:
    """Metnin tiktoken ile gerçek token sayısını hesaplar."""

    return len(tokenizer.encode(metin))


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=HEDEF_TOKEN_SAYISI,
    chunk_overlap=OVERLAP_TOKEN_SAYISI,
    length_function=token_sayisini_hesapla,
    separators=[
        "\n\n",
        "\n",
        ". ",
        "? ",
        "! ",
        "; ",
        ", ",
        " ",
        "",
    ],
)


def bolumleri_gruplandir(
    bolumler: list[MetinBolumu],
) -> list[tuple[str, int | None]]:
    """
    PDF bölümlerini sayfaya, Excel bölümlerini çalışma
    sayfasına göre gruplandırır. Word metnini birlikte tutar.
    """

    gruplar: OrderedDict[
        tuple[str, str | int],
        dict[str, object],
    ] = OrderedDict()

    for bolum in bolumler:
        if bolum.sayfa_no is not None:
            grup_anahtari = ("pdf", bolum.sayfa_no)
            sayfa_no = bolum.sayfa_no
            metin = bolum.metin

        elif bolum.sayfa_adi is not None:
            grup_anahtari = ("excel", bolum.sayfa_adi)
            sayfa_no = None

            konum = f"Çalışma sayfası: {bolum.sayfa_adi}"

            if bolum.satir_no is not None:
                konum += f", Satır: {bolum.satir_no}"

            metin = f"[{konum}]\n{bolum.metin}"

        else:
            grup_anahtari = ("word", "belge")
            sayfa_no = None
            metin = bolum.metin

        if grup_anahtari not in gruplar:
            gruplar[grup_anahtari] = {
                "sayfa_no": sayfa_no,
                "metinler": [],
            }

        metinler = gruplar[grup_anahtari]["metinler"]

        if isinstance(metinler, list):
            metinler.append(metin)

    sonuc: list[tuple[str, int | None]] = []

    for grup in gruplar.values():
        metinler = grup["metinler"]
        sayfa_no = grup["sayfa_no"]

        if isinstance(metinler, list):
            birlesik_metin = "\n\n".join(metinler).strip()

            if birlesik_metin:
                sonuc.append(
                    (
                        birlesik_metin,
                        (
                            sayfa_no
                            if isinstance(sayfa_no, int)
                            else None
                        ),
                    )
                )

    return sonuc


def bolumleri_parcalara_ayir(
    bolumler: list[MetinBolumu],
) -> list[ParcaTaslagi]:
    """Metin bölümlerini yaklaşık 600 tokenlık parçalara ayırır."""

    parcalar: list[ParcaTaslagi] = []

    for metin, sayfa_no in bolumleri_gruplandir(bolumler):
        ayrilmis_metinler = text_splitter.split_text(metin)

        for parca_metni in ayrilmis_metinler:
            temiz_parca = parca_metni.strip()

            if not temiz_parca:
                continue

            token_sayisi = token_sayisini_hesapla(
                temiz_parca
            )

            if token_sayisi <= 0:
                continue

            parcalar.append(
                ParcaTaslagi(
                    parca_metni=temiz_parca,
                    sayfa_no=sayfa_no,
                    token_sayisi=token_sayisi,
                )
            )

    return parcalar