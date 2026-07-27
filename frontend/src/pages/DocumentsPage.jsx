// Yetkiye göre görülebilen dokümanları departman ve etiketleriyle listeler

import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { detayliDokumanlariGetir } from "../services/dokumanService";


function tarihBicimlendir(tarih) {
    return new Intl.DateTimeFormat("tr-TR", {
        dateStyle: "medium",
    }).format(new Date(tarih));
}


function DocumentsPage() {
    const [dokumanlar, setDokumanlar] = useState([]);
    const [yukleniyor, setYukleniyor] = useState(true);
    const [hata, setHata] = useState("");

    useEffect(() => {
        async function dokumanlariYukle() {
            try {
                const sonuc = await detayliDokumanlariGetir();
                setDokumanlar(sonuc);
            } catch (error) {
                setHata(
                    error.response?.data?.error?.message ||
                    "Dokümanlar alınamadı.",
                );
            } finally {
                setYukleniyor(false);
            }
        }

        dokumanlariYukle();
    }, []);

    if (yukleniyor) {
        return (
            <main className="page-container">
                <p className="state-message">
                    Dokümanlar yükleniyor...
                </p>
            </main>
        );
    }

    return (
        <main className="page-container">
            <section className="page-heading">
                <div>
                    <p className="eyebrow">Kurumsal içerikler</p>
                    <h1>Dokümanlar</h1>
                    <p>
                        Yalnızca görüntüleme yetkiniz bulunan
                        dokümanlar listelenmektedir.
                    </p>
                </div>

                <span className="result-count">
                    {dokumanlar.length} doküman
                </span>
            </section>

            {hata && (
                <p className="error-message">{hata}</p>
            )}

            {!hata && dokumanlar.length === 0 ? (
                <section className="content-card">
                    <p className="empty-state">
                        Görüntüleyebileceğiniz doküman
                        bulunmuyor.
                    </p>
                </section>
            ) : (
                <section className="document-grid">
                    {dokumanlar.map((dokuman) => (
                        <article
                            key={dokuman.dokuman_id}
                            className="document-card"
                        >
                            <div className="document-card-top">
                                <span className="file-type">
                                    {dokuman.dosya_turu.toUpperCase()}
                                </span>

                                <span className="document-status">
                                    {dokuman.durum}
                                </span>
                            </div>

                            <h2>{dokuman.baslik}</h2>

                            <dl className="document-meta">
                                <div>
                                    <dt>Departman</dt>
                                    <dd>{dokuman.departman_adi}</dd>
                                </div>

                                <div>
                                    <dt>Yüklenme tarihi</dt>
                                    <dd>
                                        {tarihBicimlendir(
                                            dokuman.yuklenme_tarihi,
                                        )}
                                    </dd>
                                </div>
                            </dl>

                            <div className="tag-list">
                                {dokuman.etiketler.length === 0 ? (
                                    <span className="muted-tag">
                                        Etiket yok
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

                            <Link
                                to={`/dokumanlar/${dokuman.dokuman_id}`}
                                className="detail-link"
                            >
                                Detayları görüntüle
                            </Link>
                        </article>
                    ))}
                </section>
            )}
        </main>
    );
}


export default DocumentsPage;