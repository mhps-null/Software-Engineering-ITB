from database.query.donatur import GetDonaturById
from database.query.penerima_donasi import GetPenerimaById
from database.query.transaksi import InsertTransaksi, UpdateTransaksi, GetTransaksiById
from datetime import datetime

# C-09
class DonasiUangManager:
    def addDonasiUang(self, data: dict):
        # idDonatur, idPenerima, jumlah, metodePembayaran
        if GetDonaturById(data["idDonatur"]) is None:
            raise ValueError("Donatur tidak ditemukan.")
        if GetPenerimaById(data["idPenerima"]) is None:
            raise ValueError("Penerima tidak ditemukan.")
        data['status'] = 'pending'
        data['jenisTransaksi'] = 'donasi_uang'
        data['tanggal'] = datetime.now()
        data["idBarang"] = None
        data["idPembeli"] = None
        data["kuantitas"] = None
        return InsertTransaksi(data)
    
    def deleteDonasiUang(self, idTransaksi: int):
        transaksi = GetTransaksiById(idTransaksi)
        if transaksi is None:
            return None
        
        transaksi.status = 'deleted'
        return UpdateTransaksi(idTransaksi, {'status': 'deleted'})
    
    def copyInfoDonasiUang(self, idTransaksi: int):
        transaksi = GetTransaksiById(idTransaksi)
        if transaksi is None:
            return None
        
        return {
            "idDonatur": transaksi.idDonatur,
            "idPenerima": transaksi.idPenerima,
            "jumlah": transaksi.jumlah,
            "metodePembayaran": transaksi.metodePembayaran,
            "status": transaksi.status,
            "tanggal": transaksi.tanggal
        }

    def updateStatus(self, idTransaksi: int, status: str):
        return UpdateTransaksi(idTransaksi, {"status": status})

    def bayarDonasiUang(self, idTransaksi: int, metodePembayaran: str):
        return UpdateTransaksi(idTransaksi, {"status": "dibayar", "metodePembayaran": metodePembayaran})