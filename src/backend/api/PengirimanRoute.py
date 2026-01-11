from fastapi import APIRouter
from controllers.PengirimanManager import PengirimanManager
from schemas.Pengiriman import *

# C-27: Pengiriman
router = APIRouter(prefix="/pengiriman", tags=["Pengiriman"])
manager = PengirimanManager()

# Buat Pengiriman
@router.post("/", response_model=PengirimanResponse)
def buatPengiriman(data: CreatePengiriman):
    return manager.buatPengiriman(data.model_dump())

# Batal Pengiriman
@router.patch("/{id_pengiriman}/batal", response_model=BatalPengirimanResponse)
def batalPengiriman(id_pengiriman: int):
    result = manager.batalPengiriman(id_pengiriman)
    return {"status": result["status"]}

# (Opsional) Ambil Detail Pengiriman — karena manager menyediakan GetPengirimanById
@router.get("/{id_pengiriman}", response_model=PengirimanResponse)
def getPengiriman(id_pengiriman: int):
    pengiriman = GetPengirimanById(id_pengiriman)
    return pengiriman