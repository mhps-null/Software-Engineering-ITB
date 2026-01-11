from database.query.transaksi import GetTransaksiById, UpdateTransaksi


# C-21
class FullPaymentManager:
    # idBarang, idPembeli, jumlah, metodePembayaran
    def buatFullPayment(data: dict):
        data["jenisTransaksi"] = "full_payment"
        data["status"] = "pending"
        return data

    def validasiDataPembelian(data: dict):
        return True

    def hitungTotalPembelian(idTransaksi: int):
        transaksi = GetTransaksiById(idTransaksi)
        if transaksi is None:
            return None

        return transaksi.jumlah

    def bayarPembelian(idTransaksi: int, metode: str):
        return UpdateTransaksi(
            idTransaksi, {"status": "dibayar", "metodePembayaran": metode}
        )

    def simpanTransaksi(data: dict):
        return data

    def batalkanPembelian(idTransaksi: int):
        return UpdateTransaksi(idTransaksi, {"status": "cancelled"})
