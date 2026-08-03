// Departman listeleme ve oluşturma API işlemlerini gerçekleştirir

import api from "../api/api";


export async function departmanlariGetir() {
    const response = await api.get("/departmanlar");

    return response.data;
}


export async function departmanOlustur(departmanAdi) {
    const response = await api.post(
        "/departmanlar",
        {
            departman_adi: departmanAdi,
        },
    );

    return response.data;
}