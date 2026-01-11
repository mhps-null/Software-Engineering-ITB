from fastapi import APIRouter
from controllers.KonfirmasiPenerimaanManager import KonfirmasiPenerimaanManager
from schemas.KonfirmasiPenerimaan import *

# C-29: Konfirmasi Penerimaan Barang
router = APIRouter(prefix="/konfirmasi-penerimaan", tags=["Konfirmasi Penerimaan"])
manager = KonfirmasiPenerimaanManager()

# Konfirmasi Penerimaan Barang (accepted)
@router.patch("/{id_pengiriman}/setujui", response_model=KonfirmasiPenerimaanResponse)
def konfirmasiPenerimaan(id_pengiriman: int):
    result = manager.konfirmasiPenerimaanBarang(id_pengiriman)
    return {"status": result["status"]}

# Update Status Pengiriman (general update)
@router.patch("/{id_pengiriman}/status")
def updateStatus(id_pengiriman: int, body: UpdateStatusPengirimanRequest):
    return manager.updateStatusPengiriman(id_pengiriman, body.status)