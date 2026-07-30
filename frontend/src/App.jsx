// Uygulamanın giriş ve korumalı sayfa yönlendirmelerini tanımlar

import {
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import AppLayout from "./components/AppLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import ChatPage from "./pages/ChatPage";
import DashboardPage from "./pages/DashboardPage";
import DocumentDetailPage from "./pages/DocumentDetailPage";
import DocumentsPage from "./pages/DocumentsPage";
import DocumentUploadPage from "./pages/DocumentUploadPage";
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
                        path="/sohbet"
                        element={<ChatPage />}
                    />

                    <Route
                        path="/dokumanlar"
                        element={<DocumentsPage />}
                    />

                    <Route
                        path="/dokumanlar/yukle"
                        element={<DocumentUploadPage />}
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