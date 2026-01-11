from database.query.transaksi import InsertTransaksi
from datetime import datetime


# C-23
class TukarTambahManager:
    # idBarangBaru, idPembeli, nilaiTambahan

    def buatTukarTambah(data: dict):
        transaksi = {
            "idBarang": data["idBarangBaru"],
            "idPembeli": data["idPembeli"],
            "jumlah": data.get("nilaiTambahan", 0),
            "kuantitas": 1,
            "jenisTransaksi": "tukar_tambah",
            "status": "selesai",
            "tanggal": datetime.now(),
            "idDonatur": None,
            "idPenerima": None,
        }
        return InsertTransaksi(transaksi)

    def pilihJenisTukarTambah(jenis: str):
        return jenis

    def validasiDataTukarTambah(data: dict):
        return True

    def simpanTukarTambah(data: dict):
        return data

    def batalTukarTambah(idTukar: int):
        return {"id": idTukar, "status": "cancelled"}
