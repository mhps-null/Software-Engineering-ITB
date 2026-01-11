from fastapi import APIRouter
from controllers.DonasiBarangManager import DonasiBarangManager
from schemas.DonasiBarang import *

router = APIRouter(prefix="/donasi-barang", tags=["Donasi Barang"])
manager = DonasiBarangManager()

# C-12: Donasi Barang Manager
@router.post("/", response_model=DonasiBarangResponse)
def buatDonasiBarang(data: CreateDonasiBarang):
    return manager.addDonasiBarang(data.model_dump())

# Copy Info Barang Donasi
@router.get("/{id_barang_donasi}", response_model=DonasiBarangResponse)
def copyInfoBarang(id_barang_donasi: int):
    return manager.copyInfoBarang(id_barang_donasi)

# Update Status Barang Donasi
@router.patch("/{id_barang_donasi}/status")
def updateStatus(id_barang_donasi: int, body: UpdateStatusDonasiBarang):
    return manager.updateStatus(id_barang_donasi, body.status)

# Pilih Target Penerima Donasi Barang
@router.patch("/{id_barang_donasi}/target")
def pilihTarget(id_barang_donasi: int, body: PilihTargetDonasiBarang):
    return manager.pilihTargetDonasi(id_barang_donasi, body.idPenerima)

# Unggah Foto/Video Barang Donasi
@router.patch("/{id_barang_donasi}/unggah")
def unggahBarang(id_barang_donasi: int, body: UnggahBarangRequest):
    return manager.unggahBarang(id_barang_donasi, body.model_dump())