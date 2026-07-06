
-- Dokümanı Arşivleyen Procedure

CREATE OR REPLACE PROCEDURE sp_dokuman_arsivle(
    IN p_dokuman_id INTEGER
)

LANGUAGE plpgsql

AS
$$
BEGIN

    UPDATE dokumanlar
    SET durum = 'Arsivlendi'
    WHERE dokuman_id = p_dokuman_id;

END;
$$;

-- Dokümanı Geri Aktifleştiren Procedure

CREATE OR REPLACE PROCEDURE sp_dokuman_geri_aktiflestir(
    IN p_dokuman_id INTEGER
)

LANGUAGE plpgsql

AS
$$
BEGIN

    UPDATE dokumanlar
    SET durum = 'Aktif'
    WHERE dokuman_id = p_dokuman_id;

END;
$$;