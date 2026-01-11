from database.query.pengiriman import InsertPengiriman, GetPengirimanById, UpdatePengiriman

# C-27
class PengirimanManager:
    # idTransaksi, alamat, detailAlamat, kota, metodePengiriman
    def buatPengiriman(self, data: dict):
        data["status"] = "pending"
        return InsertPengiriman(data)

    def pilihJenisPengiriman(self, jenis: str):
        return jenis

    def validasiDataPengiriman(self, data: dict):
        return True

    def simpanPengiriman(self, data: dict):
        data["status"] = "pending"
        return InsertPengiriman(data)

    def batalPengiriman(self, idPengiriman: int):
        return UpdatePengiriman(idPengiriman, {"status": "cancelled"})
