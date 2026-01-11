from database.query.transaksi import GetTransaksiById, UpdateTransaksi


# C-15
class KonfirmasiDonasiManager:
    # Accepted, Denied, Pending
    def setujuiDonasi(idTransaksi: int):
        return UpdateTransaksi(idTransaksi, {"status": "accepted"})

    def tolakDonasi(idTransaksi: int):
        return UpdateTransaksi(idTransaksi, {"status": "denied"})

    def lihatStatusKonfirmasi(idTransaksi: int):
        transaksi = GetTransaksiById(idTransaksi)
        if transaksi is None:
            return None
        return transaksi["status"]

    def updateStatusKonfirmasi(idTransaksi: int, status: str):
        return UpdateTransaksi(idTransaksi, {"status": status})

    def kirimNotifikasiKonfirmasi(idTransaksi: int):
        return f"Transaksi {idTransaksi} berhasil dikonfirmasi!"
