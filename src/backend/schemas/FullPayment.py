from pydantic import BaseModel
from typing import Optional

class CreateFullPayment(BaseModel):
    idBarang: int
    idPembeli: int
    jumlah: int
    metodePembayaran: Optional[str] = None

class BayarFullPayment(BaseModel):
    metodePembayaran: str

class FullPaymentResponse(BaseModel):
    idBarang: int
    idPembeli: int
    jumlah: int
    status: str
    metodePembayaran: Optional[str]
    jenisTransaksi: str

    class Config:
        orm_mode = True

class TotalPembelianResponse(BaseModel):
    total: int