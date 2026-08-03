// Yetki kontrollü tek dokümanın bilgilerini ve fiziksel dosyasını gösterir

import {
    useEffect,
    useState,
} from "react";
import {
    Link,
    useParams,
} from "react-router-dom";

import {
    dokumanDetayiGetir,
    dokumanDosyasiniGetir,
} from "../services/dokumanService";


function tarihBicimlendir(tarih) {
    return new Intl.DateTimeFormat("tr-TR", {
        dateStyle: "long",
        timeStyle: "short",
    }).format(new Date(tarih));
}


function dosyaBoyutuBicimlendir(byte) {
    if (byte < 1024) {
        return `${byte} B`;
    }

    if (byte < 1024 * 1024) {
        return `${(byte / 1024).toFixed(1)} KB`;
    }

    return `${(byte / (1024 * 1024)).toFixed(1)} MB`;
}


// Blob biçiminde dönen API hata mesajını okur
async function dosyaHataMesajiGetir(error) {
    const hataVerisi = error.response?.data;

    if (hataVerisi instanceof Blob) {
        try {
            const metin = await hataVerisi.text();
            const json = JSON.parse(metin);

            return (
                json.error?.message ||
                json.detail ||
                "Doküman dosyası açılamadı."
            );
        } catch {
            return "Doküman dosyası açılamadı.";
        }
    }

    return (
        hataVerisi?.error?.message ||
        hataVerisi?.detail ||
        error.message ||
        "Doküman dosyası açılamadı."
    );
}


function DocumentDetailPage() {
    const { dokumanId } = useParams();

    const [dokuman, setDokuman] = useState(null);
    const [yukleniyor, setYukleniyor] = useState(true);
    const [hata, setHata] = useState("");
    const [dosyaAciliyor, setDosyaAciliyor] =
        useState(false);
    const [dosyaHatasi, setDosyaHatasi] =
        useState("");

    useEffect(() => {
        async function detayiYukle() {
            try {
                const sonuc = await dokumanDetayiGetir(
                    dokumanId,
                );

                setDokuman(sonuc);
            } catch (error) {
                if (error.response?.status === 403) {
                    setHata(
                        "Bu dokümanı görüntüleme yetkiniz yok.",
                    );
                } else if (error.response?.status === 404) {
                    setHata("Doküman bulunamadı.");
                } else {
                    setHata(
                        error.response?.data?.error?.message ||
                        error.response?.data?.detail ||
                        "Doküman detayı alınamadı.",
                    );
                }
            } finally {
                setYukleniyor(false);
            }
        }

        detayiYukle();
    }, [dokumanId]);


    // PDF dosyasını açar, Word ve Excel dosyasını indirir
    async function dokumanDosyasiniAc() {
        if (dosyaAciliyor || !dokuman) {
            return;
        }

        setDosyaAciliyor(true);
        setDosyaHatasi("");

        const dosyaTuru = (
            dokuman.dosya_turu || ""
        ).toLocaleLowerCase("tr-TR");

        // PDF penceresini doğrudan tıklama sırasında açarak
        // tarayıcının açılır pencereyi engellemesini önler
        const pdfPenceresi =
            dosyaTuru === "pdf"
                ? window.open("", "_blank")
                : null;

        try {
            const dosyaBlobu =
                await dokumanDosyasiniGetir(
                    dokuman.dokuman_id,
                );

            const nesneAdresi =
                URL.createObjectURL(dosyaBlobu);

            if (dosyaTuru === "pdf") {
                if (!pdfPenceresi) {
                    URL.revokeObjectURL(nesneAdresi);

                    throw new Error(
                        "Tarayıcı yeni sekme açılmasını engelledi.",
                    );
                }

                pdfPenceresi.location.href =
                    nesneAdresi;

                window.setTimeout(() => {
                    URL.revokeObjectURL(
                        nesneAdresi,
                    );
                }, 60000);

                return;
            }

            const indirmeBaglantisi =
                document.createElement("a");

            indirmeBaglantisi.href =
                nesneAdresi;

            indirmeBaglantisi.download =
                dokuman.dosya_adi;

            document.body.appendChild(
                indirmeBaglantisi,
            );

            indirmeBaglantisi.click();
            indirmeBaglantisi.remove();

            URL.revokeObjectURL(nesneAdresi);
        } catch (error) {
            if (
                pdfPenceresi &&
                !pdfPenceresi.closed
            ) {
                pdfPenceresi.close();
            }

            setDosyaHatasi(
                await dosyaHataMesajiGetir(error),
            );
        } finally {
            setDosyaAciliyor(false);
        }
    }


    if (yukleniyor) {
        return (
            <main className="page-container">
                <p className="state-message">
                    Doküman detayı yükleniyor...
                </p>
            </main>
        );
    }

    if (hata || !dokuman) {
        return (
            <main className="page-container">
                <section className="content-card">
                    <p className="error-message">
                        {hata || "Doküman bulunamadı."}
                    </p>

                    <Link
                        to="/dokumanlar"
                        className="secondary-link"
                    >
                        Dokümanlara dön
                    </Link>
                </section>
            </main>
        );
    }

    return (
        <main className="page-container">
            <Link
                to="/dokumanlar"
                className="back-link"
            >
                ← Dokümanlara dön
            </Link>

            <section className="detail-card">
                <div className="detail-heading">
                    <div>
                        <p className="eyebrow">
                            Doküman #{dokuman.dokuman_id}
                        </p>

                        <h1>{dokuman.baslik}</h1>

                        <div className="document-file-action">
                            <button
                                type="button"
                                className="document-file-link"
                                onClick={dokumanDosyasiniAc}
                                disabled={dosyaAciliyor}
                                title="Doküman dosyasını aç"
                            >
                                {dosyaAciliyor
                                    ? "Dosya açılıyor..."
                                    : dokuman.dosya_adi}
                            </button>

                            <span className="document-file-hint">
                                {dokuman.dosya_turu
                                    .toLowerCase() === "pdf"
                                    ? "Görüntülemek için tıklayın"
                                    : "İndirmek için tıklayın"}
                            </span>
                        </div>
                    </div>

                    <span className="file-type large">
                        {dokuman.dosya_turu.toUpperCase()}
                    </span>
                </div>

                {dosyaHatasi && (
                    <p className="error-message document-file-error">
                        {dosyaHatasi}
                    </p>
                )}

                <dl className="detail-grid">
                    <div>
                        <dt>Departman</dt>
                        <dd>{dokuman.departman_adi}</dd>
                    </div>

                    <div>
                        <dt>Durum</dt>
                        <dd>{dokuman.durum}</dd>
                    </div>

                    <div>
                        <dt>Sürüm</dt>
                        <dd>{dokuman.surum_no}</dd>
                    </div>

                    <div>
                        <dt>Dosya boyutu</dt>
                        <dd>
                            {dosyaBoyutuBicimlendir(
                                dokuman.dosya_boyutu,
                            )}
                        </dd>
                    </div>

                    <div>
                        <dt>Yüklenme tarihi</dt>
                        <dd>
                            {tarihBicimlendir(
                                dokuman.yuklenme_tarihi,
                            )}
                        </dd>
                    </div>

                    <div>
                        <dt>Son güncelleme</dt>
                        <dd>
                            {tarihBicimlendir(
                                dokuman.guncelleme_tarihi,
                            )}
                        </dd>
                    </div>
                </dl>

                <section className="detail-tags">
                    <h2>Etiketler</h2>

                    <div className="tag-list">
                        {dokuman.etiketler.length === 0 ? (
                            <span className="muted-tag">
                                Bu dokümana etiket eklenmemiş.
                            </span>
                        ) : (
                            dokuman.etiketler.map(
                                (etiket) => (
                                    <span
                                        key={etiket}
                                        className="tag"
                                    >
                                        {etiket}
                                    </span>
                                ),
                            )
                        )}
                    </div>
                </section>
            </section>
        </main>
    );
}


export default DocumentDetailPage;