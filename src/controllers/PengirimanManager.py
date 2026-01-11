from database.query.pengiriman import (
    InsertPengiriman,
    GetPengirimanById,
    UpdatePengiriman,
)


# C-27
class PengirimanManager:
    # idTransaksi, alamat, detailAlamat, kota, metodePengiriman
    def buatPengiriman(data: dict):
        data["status"] = "pending"
        return InsertPengiriman(data)

    def pilihJenisPengiriman(jenis: str):
        return jenis

    def validasiDataPengiriman(data: dict):
        return True

    def simpanPengiriman(data: dict):
        data["status"] = "pending"
        return InsertPengiriman(data)

    def batalPengiriman(idPengiriman: int):
        return UpdatePengiriman(idPengiriman, {"status": "cancelled"})
