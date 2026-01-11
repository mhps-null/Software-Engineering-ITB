from database.query.transaksi import InsertTransaksi
from datetime import datetime

# C-25
class AjuanTukarTambahManager:
    # idPembeli, idBarang, nilaiTambahan

    def validasiAjuan(self, data: dict):
        return True

    def setujuiAjuan(self, data: dict):
        transaksi = {
            "idBarang": data["idBarang"],
            "idPembeli": data["idPembeli"],
            "jumlah": data.get("nilaiTambahan", 0),
            "kuantitas": 1,
            "jenisTransaksi": "tukar_tambah",
            "status": "approved",
            "tanggal": datetime.now(),
            "idDonatur": None,
            "idPenerima": None,
        }

        return InsertTransaksi(transaksi)

    def tolakAjuan(self, idAjuan: int):
        return {"idAjuan": idAjuan, "status": "denied"}

    def simpanKeputusanAjuan(self, idAjuan: int, keputusan: str):
        return {"idAjuan": idAjuan, "keputusan": keputusan}

    def hitungNilaiTukarTambah(self, idAjuan: int):
        return 10000
