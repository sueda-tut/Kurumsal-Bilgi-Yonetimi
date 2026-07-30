// Yetki filtreli, kaynak gösteren AI sohbet ekranını oluşturur

import {
    useEffect,
    useRef,
    useState,
} from "react";

import {
    sohbetleriGetir,
    sohbetMesajlariniGetir,
    soruSor,
} from "../services/sohbetService";


function hataMesajiGetir(error) {
    return (
        error.response?.data?.error?.message ||
        error.response?.data?.detail ||
        error.message ||
        "İşlem sırasında bir hata oluştu."
    );
}


function tarihFormatla(tarih) {
    if (!tarih) {
        return "";
    }

    return new Intl.DateTimeFormat(
        "tr-TR",
        {
            dateStyle: "short",
            timeStyle: "short",
        },
    ).format(new Date(tarih));
}


function ChatPage() {
    const mesajSonuRef = useRef(null);

    const [oturumlar, setOturumlar] = useState([]);
    const [aktifOturumId, setAktifOturumId] =
        useState(null);
    const [mesajlar, setMesajlar] = useState([]);
    const [soru, setSoru] = useState("");
    const [cevapBekleniyor, setCevapBekleniyor] =
        useState(false);
    const [oturumYukleniyor, setOturumYukleniyor] =
        useState(false);
    const [hata, setHata] = useState("");

    useEffect(() => {
        oturumlariYukle();
    }, []);

    useEffect(() => {
        mesajSonuRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [mesajlar, cevapBekleniyor]);

    async function oturumlariYukle() {
        try {
            const sonuc = await sohbetleriGetir();

            setOturumlar(sonuc);
        } catch (error) {
            setHata(hataMesajiGetir(error));
        }
    }

    async function oturumSec(oturumId) {
        if (cevapBekleniyor) {
            return;
        }

        setAktifOturumId(oturumId);
        setOturumYukleniyor(true);
        setHata("");

        try {
            const sonuc =
                await sohbetMesajlariniGetir(oturumId);

            setMesajlar(
                sonuc.map((mesaj) => ({
                    mesajId: mesaj.mesaj_id,
                    gonderenTipi: mesaj.gonderen_tipi,
                    mesajMetni: mesaj.mesaj_metni,
                    olusturulmaTarihi:
                        mesaj.olusturulma_tarihi,
                        kaynaklar: mesaj.kaynaklar || [],
                })),
            );
        } catch (error) {
            setHata(hataMesajiGetir(error));
        } finally {
            setOturumYukleniyor(false);
        }
    }

    function yeniSohbetBaslat() {
        if (cevapBekleniyor) {
            return;
        }

        setAktifOturumId(null);
        setMesajlar([]);
        setSoru("");
        setHata("");
    }

    async function soruGonder(event) {
        event.preventDefault();

        const temizSoru = soru.trim();

        if (!temizSoru || cevapBekleniyor) {
            return;
        }

        const geciciMesajId = `gecici-${Date.now()}`;

        setMesajlar((mevcutMesajlar) => [
            ...mevcutMesajlar,
            {
                mesajId: geciciMesajId,
                gonderenTipi: "Kullanici",
                mesajMetni: temizSoru,
                olusturulmaTarihi:
                    new Date().toISOString(),
                kaynaklar: [],
            },
        ]);

        setSoru("");
        setHata("");
        setCevapBekleniyor(true);

        try {
            const sonuc = await soruSor({
                soru: temizSoru,
                oturumId: aktifOturumId,
                oturumBasligi: aktifOturumId
                    ? null
                    : temizSoru.slice(0, 80),
            });

            setAktifOturumId(sonuc.oturum_id);

            setMesajlar((mevcutMesajlar) => [
                ...mevcutMesajlar.map((mesaj) =>
                    mesaj.mesajId === geciciMesajId
                        ? {
                            ...mesaj,
                            mesajId:
                                sonuc.kullanici_mesaj_id,
                        }
                        : mesaj
                ),
                {
                    mesajId: sonuc.ai_mesaj_id,
                    gonderenTipi: "AI",
                    mesajMetni: sonuc.cevap,
                    olusturulmaTarihi:
                        new Date().toISOString(),
                    kaynaklar: sonuc.kaynaklar || [],
                },
            ]);

            await oturumlariYukle();
        } catch (error) {
            setMesajlar((mevcutMesajlar) =>
                mevcutMesajlar.filter(
                    (mesaj) =>
                        mesaj.mesajId !== geciciMesajId,
                ),
            );

            setSoru(temizSoru);
            setHata(hataMesajiGetir(error));
        } finally {
            setCevapBekleniyor(false);
        }
    }

    function klavyeKontrol(event) {
        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {
            event.preventDefault();
            event.currentTarget.form?.requestSubmit();
        }
    }

    return (
        <main className="chat-page">
            <aside className="chat-sidebar">
                <div className="chat-sidebar-heading">
                    <div>
                        <p className="eyebrow">AI sohbet</p>
                        <h1>Sohbetler</h1>
                    </div>

                    <button
                        type="button"
                        className="new-chat-button"
                        onClick={yeniSohbetBaslat}
                        disabled={cevapBekleniyor}
                    >
                        + Yeni
                    </button>
                </div>

                <div className="chat-session-list">
                    {oturumlar.length === 0 && (
                        <p className="chat-empty">
                            Henüz sohbet bulunmuyor.
                        </p>
                    )}

                    {oturumlar.map((oturum) => (
                        <button
                            key={oturum.oturum_id}
                            type="button"
                            className={
                                aktifOturumId ===
                                oturum.oturum_id
                                    ? "chat-session active"
                                    : "chat-session"
                            }
                            onClick={() =>
                                oturumSec(
                                    oturum.oturum_id,
                                )
                            }
                            disabled={cevapBekleniyor}
                        >
                            <strong>
                                {oturum.oturum_basligi}
                            </strong>

                            <time>
                                {tarihFormatla(
                                    oturum.baslangic_tarihi,
                                )}
                            </time>
                        </button>
                    ))}
                </div>
            </aside>

            <section className="chat-workspace">
                <header className="chat-heading">
                    <div>
                        <p className="eyebrow">
                            Kurumsal asistan
                        </p>

                        <h2>
                            {aktifOturumId
                                ? "Sohbete devam et"
                                : "Yeni bir soru sor"}
                        </h2>
                    </div>

                    <span className="rag-status">
                        Yetki filtreli RAG
                    </span>
                </header>

                <div className="message-area">
                    {oturumYukleniyor && (
                        <p className="chat-empty">
                            Mesajlar yükleniyor...
                        </p>
                    )}

                    {!oturumYukleniyor &&
                        mesajlar.length === 0 && (
                            <div className="chat-welcome">
                                <span className="chat-ai-icon">
                                    AI
                                </span>

                                <h2>
                                    Kurumsal dokümanlarınıza
                                    soru sorun
                                </h2>

                                <p>
                                    Yalnızca görüntüleme
                                    yetkinizin bulunduğu
                                    dokümanlar kullanılır.
                                </p>
                            </div>
                        )}

                    {!oturumYukleniyor &&
                        mesajlar.map((mesaj) => {
                            const kullaniciMesaji =
                                mesaj.gonderenTipi
                                    .toLocaleLowerCase(
                                        "tr-TR",
                                    ) === "kullanici";

                            return (
                                <article
                                    key={mesaj.mesajId}
                                    className={
                                        kullaniciMesaji
                                            ? "message-row user"
                                            : "message-row ai"
                                    }
                                >
                                    <div className="message-avatar">
                                        {kullaniciMesaji
                                            ? "S"
                                            : "AI"}
                                    </div>

                                    <div className="message-content">
                                        <div className="message-bubble">
                                            {mesaj.mesajMetni}
                                        </div>

                                        <time className="message-time">
                                            {tarihFormatla(
                                                mesaj.olusturulmaTarihi,
                                            )}
                                        </time>

                                        {!kullaniciMesaji &&
                                            mesaj.kaynaklar
                                                .length > 0 && (
                                                <div className="source-section">
                                                    <p className="source-title">
                                                        Kaynaklar
                                                    </p>

                                                    <div className="source-grid">
                                                        {mesaj.kaynaklar.map(
                                                            (kaynak) => (
                                                                <a
                                                                    key={
                                                                        kaynak.kaynak_id
                                                                    }
                                                                    href={`/dokumanlar/${kaynak.dokuman_id}`}
                                                                    className="source-card"
                                                                >
                                                                    <span>
                                                                        Doküman
                                                                    </span>

                                                                    <strong>
                                                                        {
                                                                            kaynak.dokuman_basligi
                                                                        }
                                                                    </strong>

                                                                    <small>
                                                                        {kaynak.sayfa_no
                                                                            ? `Sayfa ${kaynak.sayfa_no}`
                                                                            : `Parça ${kaynak.parca_sirasi}`}
                                                                    </small>
                                                                </a>
                                                            ),
                                                        )}
                                                    </div>
                                                </div>
                                            )}
                                    </div>
                                </article>
                            );
                        })}

                    {cevapBekleniyor && (
                        <article className="message-row ai">
                            <div className="message-avatar">
                                AI
                            </div>

                            <div className="message-content">
                                <div className="message-bubble typing-bubble">
                                    <span />
                                    <span />
                                    <span />
                                </div>

                                <small className="ai-waiting-text">
                                    Yetkili dokümanlar
                                    taranıyor...
                                </small>
                            </div>
                        </article>
                    )}

                    <div ref={mesajSonuRef} />
                </div>

                <div className="chat-composer-wrapper">
                    {hata && (
                        <p className="error-message">
                            {hata}
                        </p>
                    )}

                    <form
                        className="chat-composer"
                        onSubmit={soruGonder}
                    >
                        <textarea
                            value={soru}
                            onChange={(event) =>
                                setSoru(event.target.value)
                            }
                            onKeyDown={klavyeKontrol}
                            disabled={cevapBekleniyor}
                            maxLength={4000}
                            rows={2}
                            placeholder="Kurumsal dokümanlar hakkında sorunuzu yazın..."
                        />

                        <button
                            type="submit"
                            disabled={
                                cevapBekleniyor ||
                                !soru.trim()
                            }
                        >
                            Gönder
                        </button>
                    </form>

                    <small className="chat-disclaimer">
                        AI yalnızca yetkili olduğunuz
                        dokümanlardaki bilgileri kullanır.
                    </small>
                </div>
            </section>
        </main>
    );
}


export default ChatPage;