// Başarılı girişten sonra görüntülenen korumalı deneme sayfasını oluşturur

import { useNavigate } from "react-router-dom";


function DashboardPage() {
    const navigate = useNavigate();

    function cikisYap() {
        localStorage.removeItem("access_token");

        navigate("/giris", {
            replace: true,
        });
    }

    return (
        <main className="dashboard-page">
            <header className="dashboard-header">
                <div>
                    <span className="brand-badge">KB</span>
                    <strong>Kurumsal Bilgi Yönetimi</strong>
                </div>

                <button
                    type="button"
                    className="logout-button"
                    onClick={cikisYap}
                >
                    Çıkış yap
                </button>
            </header>

            <section className="dashboard-content">
                <p className="success-label">
                    Giriş başarılı
                </p>

                <h1>Korumalı sayfaya ulaştınız.</h1>

                <p>
                    Bu sayfa yalnızca geçerli token bulunan
                    kullanıcılar tarafından görüntülenebilir.
                </p>
            </section>
        </main>
    );
}


export default DashboardPage;
