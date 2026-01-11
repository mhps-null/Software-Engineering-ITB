from database.query.donatur import GetDonaturById
from database.query.penerima_donasi import GetPenerimaById
from database.query.barang_donasi import InsertBarangDonasi, UpdateBarangDonasi, GetBarangDonasiById
from datetime import datetime

# C-12
class DonasiBarangManager:
    def addDonasiBarang(self, data: dict):
        # namaBarang, deskripsi, kategori, idDonatur, idPenerima, caraPengiriman
        if GetDonaturById(data["idDonatur"]) is None:
            raise ValueError("Donatur tidak ditemukan.")
        if GetPenerimaById(data["idPenerima"]) is None:
            raise ValueError("Penerima tidak ditemukan.")
        
        data['status'] = 'pending'
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
            "caraPengiriman": barang.caraPengiriman
        }