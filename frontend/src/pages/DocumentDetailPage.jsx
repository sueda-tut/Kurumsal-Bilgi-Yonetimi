// Yetki kontrollü tek doküman bilgisini detaylı olarak gösterir

import { useEffect, useState } from "react";
import {
    Link,
    useParams,
} from "react-router-dom";

import { dokumanDetayiGetir } from "../services/dokumanService";


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


function DocumentDetailPage() {
    const { dokumanId } = useParams();

    const [dokuman, setDokuman] = useState(null);
    const [yukleniyor, setYukleniyor] = useState(true);
    const [hata, setHata] = useState("");

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
                        "Doküman detayı alınamadı.",
                    );
                }
            } finally {
                setYukleniyor(false);
            }
        }

        detayiYukle();
    }, [dokumanId]);

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

                        <p>{dokuman.dosya_adi}</p>
                    </div>

                    <span className="file-type large">
                        {dokuman.dosya_turu.toUpperCase()}
                    </span>
                </div>

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
                            dokuman.etiketler.map((etiket) => (
                                <span
                                    key={etiket}
                                    className="tag"
                                >
                                    {etiket}
                                </span>
                            ))
                        )}
                    </div>
                </section>
            </section>
        </main>
    );
}


export default DocumentDetailPage;