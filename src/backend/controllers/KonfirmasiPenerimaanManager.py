from database.query.pengiriman import UpdatePengiriman

# C-29
class KonfirmasiPenerimaanManager:
    # status
    def konfirmasiPenerimaanBarang(self, idPengiriman: int):
        return UpdatePengiriman(idPengiriman, {"status": "accepted"})

    def updateStatusPengiriman(self, idPengiriman: int, status: str):
        return UpdatePengiriman(idPengiriman, {"status": status})