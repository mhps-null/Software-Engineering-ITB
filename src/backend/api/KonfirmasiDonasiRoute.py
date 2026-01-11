from fastapi import APIRouter
from controllers.KonfirmasiDonasiManager import KonfirmasiDonasiManager
from schemas.KonfirmasiDonasi import *

# C-15: Konfirmasi Donasi
router = APIRouter(prefix="/konfirmasi-donasi", tags=["Konfirmasi Donasi"])
manager = KonfirmasiDonasiManager()

# Setujui Donasi
@router.patch("/{id_transaksi}/setujui")
def setujuiDonasi(id_transaksi: int):
    return manager.setujuiDonasi(id_transaksi)

# Tolak Donasi
@router.patch("/{id_transaksi}/tolak")
def tolakDonasi(id_transaksi: int):
    return manager.tolakDonasi(id_transaksi)

# Lihat Status Konfirmasi
@router.get("/{id_transaksi}/status", response_model=StatusKonfirmasiResponse)
def lihatStatusKonfirmasi(id_transaksi: int):
    status = manager.lihatStatusKonfirmasi(id_transaksi)
    return {"status": status}

# Update Status Konfirmasi (free update)
@router.patch("/{id_transaksi}/status/update")
def updateStatusKonfirmasi(id_transaksi: int, body: UpdateStatusKonfirmasiRequest):
    return manager.updateStatusKonfirmasi(id_transaksi, body.status)

# Kirim Notifikasi Konfirmasi
@router.get("/{id_transaksi}/notifikasi", response_model=NotifikasiKonfirmasiResponse)
def kirimNotifikasi(id_transaksi: int):
    pesan = manager.kirimNotifikasiKonfirmasi(id_transaksi)
    return {"pesan": pesan}