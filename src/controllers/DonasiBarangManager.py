from database.query.donatur import GetDonaturById
from database.query.penerima_donasi import GetPenerimaById, GetAllPenerima
from database.query.barang_donasi import (
    InsertBarangDonasi,
    UpdateBarangDonasi,
    GetBarangDonasiById,
    GetBarangDonasiByDonatur,
    GetBarangDonasiByPenerima,
    GetAllBarangDonasi,
)
from datetime import datetime


# C-12
class DonasiBarangManager:
    def addDonasiBarang(self, data: dict):
        # namaBarang, deskripsi, kategori, idDonatur, idPenerima, caraPengiriman
        if GetDonaturById(data["idDonatur"]) is None:
            raise ValueError("Donatur tidak ditemukan.")
        if GetPenerimaById(data["idPenerima"]) is None:
            raise ValueError("Penerima tidak ditemukan.")

        data["status"] = "pending"
        return InsertBarangDonasi(data)

    def updateStatus(self, idBarangDonasi: int, status: str):
        return UpdateBarangDonasi(idBarangDonasi, {"status": status})

    def pilihTargetDonasi(self, idBarangDonasi: int, idPenerima: int):
        if GetPenerimaById(idPenerima) is None:
            raise ValueError("Penerima tidak ditemukan.")
        return UpdateBarangDonasi(idBarangDonasi, {"idPenerima": idPenerima})

    def unggahBarang(self, idBarangDonasi: int, data: dict):
        # foto, video
        return UpdateBarangDonasi(idBarangDonasi, data)

    def copyInfoBarang(self, idBarangDonasi: int):
        barang = GetBarangDonasiById(idBarangDonasi)
        if barang is None:
            return None

        return {
            "idBarangDonasi": barang.idBarangDonasi,
            "namaBarang": barang.namaBarang,
            "kategori": barang.kategori,
            "status": barang.status,
            "idDonatur": barang.idDonatur,
            "idPenerima": barang.idPenerima,
            "caraPengiriman": barang.caraPengiriman,
        }

    def listByDonatur(self, idDonatur: int):
        try:
            return GetBarangDonasiByDonatur(idDonatur) or []
        except Exception as e:
            print(f"DonasiBarangManager.listByDonatur error: {e}")
            return []

    def listByPenerima(self, idPenerima: int):
        try:
            return GetBarangDonasiByPenerima(idPenerima) or []
        except Exception as e:
            print(f"DonasiBarangManager.listByPenerima error: {e}")
            return []

    def listPenerima(self):
        try:
            return GetAllPenerima() or []
        except Exception as e:
            print(f"DonasiBarangManager.listPenerima error: {e}")
            return []

    def listBarangDonasi(self):
        try:
            return GetAllBarangDonasi() or []
        except Exception as e:
            print(f"DonasiBarangManager.listBarangDonasi error: {e}")
            return []
