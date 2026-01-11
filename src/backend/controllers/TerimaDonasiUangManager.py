from database.query.transaksi import GetTransaksiById, UpdateTransaksi

# C-13
class TerimaDonasiUangManager:
    def copyInfoDonasiUang(self, idTransaksi: int):
        transaksi = GetTransaksiById(idTransaksi)
        if transaksi is None:
            return None

        return {
            "jumlah": transaksi.jumlah,
            "status": transaksi.status,
            "metodePembayaran": transaksi.metodePembayaran,
            "tanggal": transaksi.tanggal
        }

    def updateStatus(self, idTransaksi: int, status: str):
        return UpdateTransaksi(idTransaksi, {"status": status})