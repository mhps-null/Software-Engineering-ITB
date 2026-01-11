from fastapi import APIRouter
from controllers.TerimaDonasiUangManager import TerimaDonasiUangManager
from schemas.TerimaDonasiUang import *

# C-13: Terima Donasi Uang
router = APIRouter(prefix="/terima-donasi-uang", tags=["Terima Donasi Uang"])
manager = TerimaDonasiUangManager()

# 1. Copy Info Donasi Uang
@router.get("/{id_transaksi}", response_model=DonasiUangInfoResponse)
def copyInfoDonasiUang(id_transaksi: int):
    return manager.copyInfoDonasiUang(id_transaksi)

# 2. Update Status Donasi Uang
@router.patch("/{id_transaksi}/status")
def updateStatus(id_transaksi: int, body: UpdateStatusDonasiUang):
    return manager.updateStatus(id_transaksi, body.status)