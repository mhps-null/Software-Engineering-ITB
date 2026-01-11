from fastapi import APIRouter
from controllers.PenjualanManager import PenjualanManager
from schemas.Penjualan import *

# C-19: Penjualan
router = APIRouter(prefix="/penjualan", tags=["Penjualan"])
manager = PenjualanManager()

# 1. Buat Penjualan
@router.post("/", response_model=PenjualanResponse)
def buatPenjualan(data: CreatePenjualan):
    return manager.buatPenjualan(data.model_dump())

# 2. Tambah/Ganti Barang pada Transaksi Penjualan
@router.patch("/{id_transaksi}/tambah-barang")
def tambahBarang(id_transaksi: int, body: TambahBarangPenjualanRequest):
    return manager.tambahBarangPenjualan(id_transaksi, body.idBarang)

# 3. Hapus Barang dari Transaksi Penjualan
@router.patch("/{id_transaksi}/hapus-barang")
def hapusBarang(id_transaksi: int):
    return manager.hapusBarangPenjualan(id_transaksi)

# 4. Hitung Total Penjualan
@router.get("/{id_transaksi}/total", response_model=TotalPenjualanResponse)
def hitungTotal(id_transaksi: int):
    total = manager.hitungTotalPenjualan(id_transaksi)
    return {"total": total}

# 5. Konfirmasi Penjualan
@router.patch("/{id_transaksi}/konfirmasi")
def konfirmasiPenjualan(id_transaksi: int):
    return manager.konfirmasiPenjualan(id_transaksi)

# 6. Batalkan Penjualan
@router.patch("/{id_transaksi}/batal")
def batalkanPenjualan(id_transaksi: int):
    return manager.batalkanPenjualan(id_transaksi)