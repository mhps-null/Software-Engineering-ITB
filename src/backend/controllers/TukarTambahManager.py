from database.query.transaksi import InsertTransaksi
from datetime import datetime

# C-23
class TukarTambahManager:
    # idBarangBaru, idPembeli, nilaiTambahan

    def buatTukarTambah(self, data: dict):
        transaksi = {
            "idBarang": data["idBarangBaru"],
            "idPembeli": data["idPembeli"],
            "jumlah": data.get("nilaiTambahan", 0),
            "kuantitas": 1,
            "jenisTransaksi": "tukar_tambah",
            "status": "selesai",
            "tanggal": datetime.now(),
            "idDonatur": None,
            "idPenerima": None
        }
        return InsertTransaksi(transaksi)

    def pilihJenisTukarTambah(self, jenis: str):
        return jenis

    def validasiDataTukarTambah(self, data: dict):
        return True

    def simpanTukarTambah(self, data: dict):
        return data

    def batalTukarTambah(self, idTukar: int):
        return {"id": idTukar, "status": "cancelled"}
