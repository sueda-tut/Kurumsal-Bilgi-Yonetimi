// Giriş, dashboard ve doküman sayfalarının yönlendirmelerini tanımlar

import {
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import AppLayout from "./components/AppLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import DashboardPage from "./pages/DashboardPage";
import DocumentDetailPage from "./pages/DocumentDetailPage";
import DocumentsPage from "./pages/DocumentsPage";
import LoginPage from "./pages/LoginPage";


function App() {
    return (
        <Routes>
            <Route
                path="/giris"
                element={<LoginPage />}
            />

            <Route element={<ProtectedRoute />}>
                <Route element={<AppLayout />}>
                    <Route
                        path="/panel"
                        element={<DashboardPage />}
                    />

                    <Route
                        path="/dokumanlar"
                        element={<DocumentsPage />}
                    />

                    <Route
                        path="/dokumanlar/:dokumanId"
                        element={<DocumentDetailPage />}
                    />
                </Route>
            </Route>

            <Route
                path="/"
                element={<Navigate to="/panel" replace />}
            />

            <Route
                path="*"
                element={<Navigate to="/panel" replace />}
            />
        </Routes>
    );
}


export default App;