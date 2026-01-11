from pydantic import BaseModel
from typing import Optional

class CreatePenjualan(BaseModel):
    idBarang: int
    idPembeli: int
    kuantitas: int
    metodePembayaran: Optional[str] = None

class TambahBarangPenjualanRequest(BaseModel):
    idBarang: int

class TotalPenjualanResponse(BaseModel):
    total: int

class PenjualanResponse(BaseModel):
    idTransaksi: int
    idBarang: Optional[int]
    idPembeli: int
    kuantitas: int
    status: str
    metodePembayaran: Optional[str]
    jenisTransaksi: str

    class Config:
        orm_mode = True