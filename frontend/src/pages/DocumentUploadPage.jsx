// Dosya, etiket ve departman yetkileriyle doküman yükleme formunu oluşturur

import {
    useEffect,
    useMemo,
    useState,
} from "react";
import {
    Link,
    useNavigate,
} from "react-router-dom";

import {
    departmanlariGetir,
    dokumanDurumunuBekle,
    dokumanaEtiketEkle,
    dokumanaYetkiEkle,
    dokumanYukle,
} from "../services/dokumanService";


const MAKSIMUM_DOSYA_BOYUTU = 20 * 1024 * 1024;
const IZIN_VERILEN_UZANTILAR = ["pdf", "docx", "xlsx"];


function hataMesajiGetir(error) {
    return (
        error.response?.data?.error?.message ||
        error.response?.data?.detail ||
        error.message ||
        "Doküman yüklenemedi."
    );
}


function DocumentUploadPage() {
    const navigate = useNavigate();

    const [departmanlar, setDepartmanlar] = useState([]);
    const [dosya, setDosya] = useState(null);
    const [baslik, setBaslik] = useState("");
    const [departmanId, setDepartmanId] = useState("");
    const [etiketMetni, setEtiketMetni] = useState("");
    const [yetkiliDepartmanlar, setYetkiliDepartmanlar] =
        useState([]);
    const [durum, setDurum] = useState("hazir");
    const [hata, setHata] = useState("");
    const [yuklenenDokumanId, setYuklenenDokumanId] =
        useState(null);

    useEffect(() => {
        async function verileriYukle() {
            try {
                const sonuc = await departmanlariGetir();

                setDepartmanlar(sonuc);

                if (sonuc.length > 0) {
                    setDepartmanId(
                        String(sonuc[0].departman_id),
                    );
                }
            } catch (error) {
                setHata(hataMesajiGetir(error));
            }
        }

        verileriYukle();
    }, []);

    const etiketler = useMemo(
        () =>
            [
                ...new Set(
                    etiketMetni
                        .split(",")
                        .map((etiket) =>
                            etiket.trim().toLocaleLowerCase(
                                "tr-TR",
                            ),
                        )
                        .filter(Boolean),
                ),
            ],
        [etiketMetni],
    );

    function dosyaSecildi(event) {
        const secilenDosya = event.target.files?.[0] || null;

        setHata("");
        setDosya(secilenDosya);

        if (secilenDosya && !baslik.trim()) {
            setBaslik(
                secilenDosya.name.replace(/\.[^.]+$/, ""),
            );
        }
    }

    function yetkiDegistir(secilenDepartmanId) {
        setYetkiliDepartmanlar((mevcut) => {
            if (mevcut.includes(secilenDepartmanId)) {
                return mevcut.filter(
                    (id) => id !== secilenDepartmanId,
                );
            }

            return [...mevcut, secilenDepartmanId];
        });
    }

    function formuDogrula() {
        if (!dosya) {
            return "Yüklenecek dosyayı seçin.";
        }

        const uzanti =
            dosya.name.split(".").pop()?.toLowerCase() || "";

        if (!IZIN_VERILEN_UZANTILAR.includes(uzanti)) {
            return "Yalnızca PDF, DOCX ve XLSX dosyaları yüklenebilir.";
        }

        if (dosya.size > MAKSIMUM_DOSYA_BOYUTU) {
            return "Dosya boyutu en fazla 20 MB olabilir.";
        }

        if (!baslik.trim()) {
            return "Doküman başlığı boş bırakılamaz.";
        }

        if (!departmanId) {
            return "Doküman departmanını seçin.";
        }

        return "";
    }

    async function formuGonder(event) {
        event.preventDefault();

        const dogrulamaHatasi = formuDogrula();

        if (dogrulamaHatasi) {
            setHata(dogrulamaHatasi);
            return;
        }

        setHata("");
        setDurum("yukleniyor");

        try {
            const dokuman = await dokumanYukle({
                dosya,
                baslik: baslik.trim(),
                departmanId,
            });

            setYuklenenDokumanId(dokuman.dokuman_id);
            setDurum("isleniyor");

            await Promise.all([
                ...etiketler.map((etiket) =>
                    dokumanaEtiketEkle(
                        dokuman.dokuman_id,
                        etiket,
                    ),
                ),
                ...yetkiliDepartmanlar.map(
                    (secilenDepartmanId) =>
                        dokumanaYetkiEkle(
                            dokuman.dokuman_id,
                            secilenDepartmanId,
                        ),
                ),
            ]);

            const islenmisDokuman =
                await dokumanDurumunuBekle(
                    dokuman.dokuman_id,
                );

            if (
                islenmisDokuman.durum.toLocaleLowerCase(
                    "tr-TR",
                ) === "hata"
            ) {
                setDurum("hata");
                setHata(
                    "Dosya kaydedildi ancak AI işleme aşamasında hata oluştu.",
                );
                return;
            }

            setDurum("aktif");

            window.setTimeout(() => {
                navigate(
                    `/dokumanlar/${dokuman.dokuman_id}`,
                );
            }, 1200);
        } catch (error) {
            setDurum("hata");
            setHata(hataMesajiGetir(error));
        }
    }

    const islemDevamEdiyor = [
        "yukleniyor",
        "isleniyor",
    ].includes(durum);

    return (
        <main className="page-container">
            <Link
                to="/dokumanlar"
                className="back-link"
            >
                ← Dokümanlara dön
            </Link>

            <div className="page-heading">
                <div>
                    <p className="eyebrow">Doküman yönetimi</p>
                    <h1>Yeni doküman yükle</h1>
                    <p>
                        Dosyanızı yükleyin; sistem metni çıkarıp
                        parçalara ayırarak embedding oluşturacaktır.
                    </p>
                </div>
            </div>

            <div className="upload-layout">
                <form
                    className="upload-card"
                    onSubmit={formuGonder}
                >
                    <div className="form-field">
                        <label htmlFor="dosya">
                            Dosya
                        </label>

                        <input
                            id="dosya"
                            type="file"
                            accept=".pdf,.docx,.xlsx"
                            onChange={dosyaSecildi}
                            disabled={islemDevamEdiyor}
                        />

                        <small>
                            PDF, DOCX veya XLSX — en fazla 20 MB
                        </small>
                    </div>

                    <div className="form-field">
                        <label htmlFor="baslik">
                            Başlık
                        </label>

                        <input
                            id="baslik"
                            type="text"
                            value={baslik}
                            onChange={(event) =>
                                setBaslik(event.target.value)
                            }
                            disabled={islemDevamEdiyor}
                            placeholder="Doküman başlığı"
                        />
                    </div>

                    <div className="form-field">
                        <label htmlFor="departman">
                            Dokümanın departmanı
                        </label>

                        <select
                            id="departman"
                            value={departmanId}
                            onChange={(event) =>
                                setDepartmanId(
                                    event.target.value,
                                )
                            }
                            disabled={islemDevamEdiyor}
                        >
                            {departmanlar.map((departman) => (
                                <option
                                    key={departman.departman_id}
                                    value={departman.departman_id}
                                >
                                    {departman.departman_adi}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="form-field">
                        <label htmlFor="etiketler">
                            Etiketler
                        </label>

                        <input
                            id="etiketler"
                            type="text"
                            value={etiketMetni}
                            onChange={(event) =>
                                setEtiketMetni(
                                    event.target.value,
                                )
                            }
                            disabled={islemDevamEdiyor}
                            placeholder="politika, güvenlik, personel"
                        />

                        <small>
                            Birden fazla etiketi virgülle ayırın.
                        </small>
                    </div>

                    <fieldset
                        className="permission-fieldset"
                        disabled={islemDevamEdiyor}
                    >
                        <legend>
                            Görüntüleyebilecek departmanlar
                        </legend>

                        <div className="permission-grid">
                            {departmanlar.map((departman) => {
                                const id =
                                    departman.departman_id;

                                return (
                                    <label
                                        key={id}
                                        className="checkbox-row"
                                    >
                                        <input
                                            type="checkbox"
                                            checked={
                                                yetkiliDepartmanlar
                                                    .includes(id)
                                            }
                                            onChange={() =>
                                                yetkiDegistir(id)
                                            }
                                        />

                                        <span>
                                            {
                                                departman.departman_adi
                                            }
                                        </span>
                                    </label>
                                );
                            })}
                        </div>
                    </fieldset>

                    {hata && (
                        <p className="error-message">
                            {hata}
                        </p>
                    )}

                    <button
                        type="submit"
                        className="upload-button"
                        disabled={islemDevamEdiyor}
                    >
                        {islemDevamEdiyor
                            ? "İşlem devam ediyor..."
                            : "Dokümanı yükle"}
                    </button>
                </form>

                <aside className="processing-card">
                    <p className="eyebrow">İşlem durumu</p>
                    <h2>AI hazırlık süreci</h2>

                    <ol className="process-list">
                        <li
                            className={
                                durum !== "hazir"
                                    ? "completed"
                                    : ""
                            }
                        >
                            Dosya seçimi
                        </li>

                        <li
                            className={
                                [
                                    "isleniyor",
                                    "aktif",
                                ].includes(durum)
                                    ? "completed"
                                    : durum === "yukleniyor"
                                      ? "current"
                                      : ""
                            }
                        >
                            Sunucuya yükleme
                        </li>

                        <li
                            className={
                                durum === "aktif"
                                    ? "completed"
                                    : durum === "isleniyor"
                                      ? "current"
                                      : durum === "hata"
                                        ? "failed"
                                        : ""
                            }
                        >
                            Metin çıkarma ve embedding
                        </li>

                        <li
                            className={
                                durum === "aktif"
                                    ? "completed"
                                    : durum === "hata"
                                      ? "failed"
                                      : ""
                            }
                        >
                            AI kullanımına hazır
                        </li>
                    </ol>

                    {durum === "isleniyor" && (
                        <p className="processing-message">
                            Doküman işleniyor. Bu sayfayı
                            kapatmayın.
                        </p>
                    )}

                    {durum === "aktif" && (
                        <p className="success-message">
                            Doküman aktif ve AI kullanımına hazır.
                        </p>
                    )}

                    {yuklenenDokumanId && (
                        <small>
                            Doküman ID: {yuklenenDokumanId}
                        </small>
                    )}
                </aside>
            </div>
        </main>
    );
}


export default DocumentUploadPage;