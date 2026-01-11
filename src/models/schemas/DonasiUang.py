from pydantic import BaseModel
from typing import Optional


class CreateDonasiUang(BaseModel):
    idDonatur: int
    idPenerima: int
    jumlah: int
    metodePembayaran: Optional[str] = None


class UpdateStatusDonasiUang(BaseModel):
    status: str


class BayarDonasiUang(BaseModel):
    metodePembayaran: str


class DonasiUangResponse(BaseModel):
    idTransaksi: int
    idDonatur: int
    idPenerima: int
    jumlah: int
    status: str
    metodePembayaran: Optional[str]
    tanggal: Optional[str]

    class Config:
        orm_mode = True
