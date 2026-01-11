from fastapi import APIRouter
from controllers.TerimaDonasiBarangManager import TerimaDonasiBarangManager
from schemas.TerimaDonasiBarang import *

# C-17: Terima Donasi Barang
router = APIRouter(prefix="/terima-donasi-barang", tags=["Terima Donasi Barang"])
manager = TerimaDonasiBarangManager()

# 1. Copy Info Donasi Barang
@router.get("/{id_barang_donasi}", response_model=DonasiBarangInfoResponse)
def copyInfo(id_barang_donasi: int):
    return manager.copyInfoDonasiBarang(id_barang_donasi)

# 2. Update Status Donasi Barang
@router.patch("/{id_barang_donasi}/status")
def updateStatus(id_barang_donasi: int, body: UpdateStatusDonasiBarang):
    return manager.updateStatus(id_barang_donasi, body.status)