// FastAPI isteklerini ve JWT token yönetimini merkezi olarak gerçekleştirir

import axios from "axios";


const api = axios.create({
    baseURL:
        import.meta.env.VITE_API_URL ||
        "http://127.0.0.1:8000",
});


// Her API isteğinden önce localStorage içindeki token'ı ekler
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error),
);


// Geçersiz veya süresi dolmuş token durumunda oturumu kapatır
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem("access_token");

            if (window.location.pathname !== "/giris") {
                window.location.href = "/giris";
            }
        }

        return Promise.reject(error);
    },
);


export default api;