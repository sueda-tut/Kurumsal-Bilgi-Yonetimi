// Giriş yapan kullanıcının profil bilgilerini API üzerinden getirir

import api from "../api/api";


export async function profilGetir() {
    const response = await api.get("/profil");

    return response.data;
}