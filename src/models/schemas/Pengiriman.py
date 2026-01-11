from pydantic import BaseModel
from typing import Optional


class CreatePengiriman(BaseModel):
    idTransaksi: int
    alamat: str
    detailAlamat: Optional[str] = None
    kota: str
    metodePengiriman: str


class PengirimanResponse(BaseModel):
    idPengiriman: int
    idTransaksi: int
    alamat: str
    detailAlamat: Optional[str]
    kota: str
    metodePengiriman: str
    status: str

    class Config:
        orm_mode = True


class BatalPengirimanResponse(BaseModel):
    status: str
