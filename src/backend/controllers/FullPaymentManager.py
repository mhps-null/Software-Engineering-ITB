from database.query.transaksi import GetTransaksiById, UpdateTransaksi

# C-21
class FullPaymentManager:
    # idBarang, idPembeli, jumlah, metodePembayaran
    def buatFullPayment(self, data: dict):
        data["jenisTransaksi"] = "full_payment"
        data["status"] = "pending"
        return data

    def validasiDataPembelian(self, data: dict):
        return True

    def hitungTotalPembelian(self, idTransaksi: int):
        transaksi = GetTransaksiById(idTransaksi)
        if transaksi is None:
            return None

        return transaksi.jumlah

    def bayarPembelian(self, idTransaksi: int, metode: str):
        return UpdateTransaksi(idTransaksi, { "status": "dibayar", "metodePembayaran": metode })

    def simpanTransaksi(self, data: dict):
        return data

    def batalkanPembelian(self, idTransaksi: int):
        return UpdateTransaksi(idTransaksi, {"status": "cancelled"})