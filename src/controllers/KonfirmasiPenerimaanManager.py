from database.query.pengiriman import UpdatePengiriman


# C-29
class KonfirmasiPenerimaanManager:
    # status
    def konfirmasiPenerimaanBarang(idPengiriman: int):
        return UpdatePengiriman(idPengiriman, {"status": "accepted"})

    def updateStatusPengiriman(idPengiriman: int, status: str):
        return UpdatePengiriman(idPengiriman, {"status": status})
