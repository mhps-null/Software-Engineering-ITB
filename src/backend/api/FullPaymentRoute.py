from fastapi import APIRouter
from controllers.FullPaymentManager import FullPaymentManager
from schemas.FullPayment import *

router = APIRouter(prefix="/full-payment", tags=["Full Payment"])
manager = FullPaymentManager()

# C-21: Full Payment Manager
# 1. Buat Full Payment
@router.post("/", response_model=FullPaymentResponse)
def buatFullPayment(data: CreateFullPayment):
    return manager.buatFullPayment(data.model_dump())

# 2. Hitung Total Pembelian
@router.get("/{id_transaksi}/total", response_model=TotalPembelianResponse)
def hitungTotalPembelian(id_transaksi: int):
    total = manager.hitungTotalPembelian(id_transaksi)
    return {"total": total}

# 3. Bayar Pembelian
@router.post("/{id_transaksi}/bayar")
def bayarPembelian(id_transaksi: int, body: BayarFullPayment):
    return manager.bayarPembelian(id_transaksi, body.metodePembayaran)

# 4. Batalkan Pembelian
@router.patch("/{id_transaksi}/batal")
def batalkanPembelian(id_transaksi: int):
    return manager.batalkanPembelian(id_transaksi)