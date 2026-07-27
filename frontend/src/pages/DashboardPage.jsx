// Kullanıcının görebildiği doküman ve son sohbet özetlerini gösterir

import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api from "../api/api";


function tarihBicimlendir(tarih) {
    return new Intl.DateTimeFormat("tr-TR", {
        dateStyle: "medium",
        timeStyle: "short",
    }).format(new Date(tarih));
}


function DashboardPage() {
    const [dokumanSayisi, setDokumanSayisi] = useState(0);
    const [sohbetler, setSohbetler] = useState([]);
    const [yukleniyor, setYukleniyor] = useState(true);
    const [hata, setHata] = useState("");

    useEffect(() => {
        async function dashboardVerileriniGetir() {
            try {
                const [
                    dokumanResponse,
                    sohbetResponse,
                ] = await Promise.all([
                    api.get("/dokumanlar", {
                        params: {
                            offset: 0,
                            limit: 100,
                        },
                    }),
                    api.get("/sohbetler"),
                ]);

                setDokumanSayisi(
                    dokumanResponse.data.length,
                );

                setSohbetler(
                    sohbetResponse.data.slice(0, 5),
                );
            } catch (error) {
                setHata(
                    error.response?.data?.error?.message ||
                    "Dashboard bilgileri alınamadı.",
                );
            } finally {
                setYukleniyor(false);
            }
        }

        dashboardVerileriniGetir();
    }, []);

    if (yukleniyor) {
        return (
            <main className="page-container">
                <p className="state-message">
                    Dashboard yükleniyor...
                </p>
            </main>
        );
    }

    return (
        <main className="page-container">
            <section className="page-heading">
                <div>
                    <p className="eyebrow">Genel görünüm</p>
                    <h1>Dashboard</h1>
                    <p>
                        Yetkili olduğunuz dokümanları ve son
                        sohbetlerinizi görüntüleyin.
                    </p>
                </div>

                <Link
                    to="/dokumanlar"
                    className="primary-link"
                >
                    Dokümanları görüntüle
                </Link>
            </section>

            {hata && (
                <p className="error-message">{hata}</p>
            )}

            <section className="summary-grid">
                <article className="summary-card">
                    <span>Görülebilen doküman</span>
                    <strong>{dokumanSayisi}</strong>
                    <p>
                        Yetki modeline göre erişebildiğiniz
                        arşivlenmemiş doküman sayısı.
                    </p>
                </article>

                <article className="summary-card">
                    <span>Son sohbetler</span>
                    <strong>{sohbetler.length}</strong>
                    <p>
                        En son oluşturduğunuz sohbet
                        oturumlarından gösterilen kayıtlar.
                    </p>
                </article>
            </section>

            <section className="content-card">
                <div className="section-heading">
                    <div>
                        <h2>Son sohbetler</h2>
                        <p>Kendi sohbet oturumlarınız</p>
                    </div>
                </div>

                {sohbetler.length === 0 ? (
                    <p className="empty-state">
                        Henüz sohbet oturumunuz bulunmuyor.
                    </p>
                ) : (
                    <div className="conversation-list">
                        {sohbetler.map((sohbet) => (
                            <article
                                key={sohbet.oturum_id}
                                className="conversation-item"
                            >
                                <div>
                                    <strong>
                                        {sohbet.oturum_basligi}
                                    </strong>

                                    <span>
                                        Oturum #{sohbet.oturum_id}
                                    </span>
                                </div>

                                <time>
                                    {tarihBicimlendir(
                                        sohbet.baslangic_tarihi,
                                    )}
                                </time>
                            </article>
                        ))}
                    </div>
                )}
            </section>
        </main>
    );
}


export default DashboardPage;