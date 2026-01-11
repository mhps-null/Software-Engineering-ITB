from database.query.transaksi import (
    InsertTransaksi,
    GetTransaksiById,
    UpdateTransaksi,
    GetTransaksiByPembeli,
)
from database.query.barang import GetBarangById
from database.query.pembeli import GetPembeliById
from datetime import datetime


# C-19
class PenjualanManager:
    # idBarang, idPembeli, kuantitas, metodePembayaran
    def buatPenjualan(data: dict):
        if GetBarangById(data["idBarang"]) is None:
            raise ValueError("Barang tidak ditemukan.")
        if GetPembeliById(data["idPembeli"]) is None:
            raise ValueError("Pembeli tidak ditemukan.")

        data["jenisTransaksi"] = "jual_beli"
        data["status"] = "created"
        data["tanggal"] = datetime.now()
        data["idDonatur"] = None
        data["idPenerima"] = None
        data["jumlah"] = None

        return InsertTransaksi(data)

    def tambahBarangPenjualan(idTransaksi: int, idBarang: int):
        return UpdateTransaksi(idTransaksi, {"idBarang": idBarang})

    def hapusBarangPenjualan(idTransaksi: int):
        return UpdateTransaksi(idTransaksi, {"idBarang": None})

    def hitungTotalPenjualan(idTransaksi: int):
        transaksi = GetTransaksiById(idTransaksi)
        if transaksi is None:
            return None
        return transaksi.jumlah * transaksi.kuantitas

    def konfirmasiPenjualan(idTransaksi: int):
        return UpdateTransaksi(idTransaksi, {"status": "confirmed"})

    def simpanPenjualan(data: dict):
        return InsertTransaksi(data)

    def batalkanPenjualan(idTransaksi: int):
        return UpdateTransaksi(idTransaksi, {"status": "cancelled"})

    def getTransaksiPembeli(idPembeli: int):
        try:
            return GetTransaksiByPembeli(idPembeli) or []
        except Exception as e:
            print(f"PenjualanManager.getTransaksiPembeli error: {e}")
            return []
