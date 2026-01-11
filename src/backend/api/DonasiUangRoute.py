from fastapi import APIRouter
from controllers.DonasiUangManager import DonasiUangManager
from schemas.DonasiUang import *

router = APIRouter(prefix="/donasi-uang", tags=["Donasi Uang"])
manager = DonasiUangManager()

# C-09: Donasi Uang Manager
# 1. Tambah Donasi Uang
@router.post("/", response_model=DonasiUangResponse)
def buatDonasiUang(data: CreateDonasiUang):
    return manager.addDonasiUang(data.model_dump())

# 2. Copy Info Donasi Uang
@router.get("/{id_transaksi}", response_model=DonasiUangResponse)
def copyInfoDonasiUang(id_transaksi: int):
    return manager.copyInfoDonasiUang(id_transaksi)

# 3. Update Status Donasi Uang
@router.patch("/{id_transaksi}/status")
def updateStatus(id_transaksi: int, body: UpdateStatusDonasiUang):
    return manager.updateStatus(id_transaksi, body.status)

# 4. Bayar Donasi Uang
@router.post("/{id_transaksi}/bayar")
def bayarDonasiUang(id_transaksi: int, body: BayarDonasiUang):
    return manager.bayarDonasiUang(id_transaksi, body.metodePembayaran)

# 5. Hapus Donasi Uang
@router.delete("/{id_transaksi}")
def hapusDonasiUang(id_transaksi: int):
    return manager.deleteDonasiUang(id_transaksi)