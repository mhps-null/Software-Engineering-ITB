from database.query.barang_donasi import GetBarangDonasiById, UpdateBarangDonasi


# C-17
class TerimaDonasiBarangManager:
    def copyInfoDonasiBarang(idBarangDonasi: int):
        barang = GetBarangDonasiById(idBarangDonasi)
        if barang is None:
            return None

        return {
            "namaBarang": barang.namaBarang,
            "kategori": barang.kategori,
            "status": barang.status,
            "caraPengiriman": barang.caraPengiriman,
        }

    def updateStatus(idBarangDonasi: int, status: str):
        return UpdateBarangDonasi(idBarangDonasi, {"status": status})
