// Doküman listeleme, detay ve yükleme API işlemlerini gerçekleştirir

import api from "../api/api";


function departmanHaritasiOlustur(departmanlar) {
    return Object.fromEntries(
        departmanlar.map((departman) => [
            departman.departman_id,
            departman.departman_adi,
        ]),
    );
}


export async function departmanlariGetir() {
    const response = await api.get("/departmanlar");

    return response.data;
}


export async function detayliDokumanlariGetir() {
    const [dokumanResponse, departmanResponse] =
        await Promise.all([
            api.get("/dokumanlar", {
                params: {
                    offset: 0,
                    limit: 100,
                },
            }),
            api.get("/departmanlar"),
        ]);

    const departmanHaritasi = departmanHaritasiOlustur(
        departmanResponse.data,
    );

    return Promise.all(
        dokumanResponse.data.map(async (dokuman) => {
            const etiketResponse = await api.get(
                `/dokumanlar/${dokuman.dokuman_id}/etiketler`,
            );

            return {
                ...dokuman,
                departman_adi:
                    departmanHaritasi[dokuman.departman_id] ||
                    `Departman #${dokuman.departman_id}`,
                etiketler: etiketResponse.data.map(
                    (etiket) => etiket.etiket_adi,
                ),
            };
        }),
    );
}


export async function dokumanDetayiGetir(dokumanId) {
    const [
        dokumanResponse,
        departmanResponse,
        etiketResponse,
    ] = await Promise.all([
        api.get(`/dokumanlar/${dokumanId}`),
        api.get("/departmanlar"),
        api.get(`/dokumanlar/${dokumanId}/etiketler`),
    ]);

    const departmanHaritasi = departmanHaritasiOlustur(
        departmanResponse.data,
    );

    return {
        ...dokumanResponse.data,
        departman_adi:
            departmanHaritasi[
                dokumanResponse.data.departman_id
            ] ||
            `Departman #${dokumanResponse.data.departman_id}`,
        etiketler: etiketResponse.data.map(
            (etiket) => etiket.etiket_adi,
        ),
    };
}


// Dosyayı multipart/form-data olarak backend'e yükler
export async function dokumanYukle({
    dosya,
    baslik,
    departmanId,
}) {
    const formData = new FormData();

    formData.append("dosya", dosya);
    formData.append("baslik", baslik);
    formData.append("departman_id", departmanId);

    const response = await api.post(
        "/dokumanlar/yukle",
        formData,
    );

    return response.data;
}


// Bir dokümana etiket ekler
export async function dokumanaEtiketEkle(
    dokumanId,
    etiketAdi,
) {
    const response = await api.post(
        `/dokumanlar/${dokumanId}/etiket`,
        {
            etiket_adi: etiketAdi,
        },
    );

    return response.data;
}


// Bir dokümana departman görüntüleme yetkisi ekler
export async function dokumanaYetkiEkle(
    dokumanId,
    departmanId,
) {
    const response = await api.post(
        `/dokumanlar/${dokumanId}/yetki`,
        {
            departman_id: departmanId,
            goruntuleyebilir_mi: true,
        },
    );

    return response.data;
}


// Doküman aktif veya hata durumuna gelene kadar sorgular
export async function dokumanDurumunuBekle(
    dokumanId,
    {
        sorguAraligi = 2000,
        maksimumDeneme = 90,
    } = {},
) {
    for (
        let deneme = 0;
        deneme < maksimumDeneme;
        deneme += 1
    ) {
        const response = await api.get(
            `/dokumanlar/${dokumanId}`,
        );

        const dokuman = response.data;
        const durum = dokuman.durum.toLocaleLowerCase("tr-TR");

        if (durum === "aktif" || durum === "hata") {
            return dokuman;
        }

        await new Promise((resolve) => {
            window.setTimeout(resolve, sorguAraligi);
        });
    }

    throw new Error(
        "Doküman işleme işlemi beklenen sürede tamamlanmadı.",
    );
}

// Yetki kontrollü doküman dosyasını blob olarak getirir
export async function dokumanDosyasiniGetir(dokumanId) {
    const response = await api.get(
        `/dokumanlar/${dokumanId}/dosya`,
        {
            responseType: "blob",
        },
    );

    return response.data;
}