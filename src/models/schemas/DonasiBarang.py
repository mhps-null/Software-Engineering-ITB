from pydantic import BaseModel
from typing import Optional


class CreateDonasiBarang(BaseModel):
    namaBarang: str
    deskripsi: Optional[str] = None
    kategori: Optional[str] = None
    idDonatur: int
    idPenerima: int
    caraPengiriman: str


class UpdateStatusDonasiBarang(BaseModel):
    status: str


class PilihTargetDonasiBarang(BaseModel):
    idPenerima: int


class UnggahBarangRequest(BaseModel):
    foto: Optional[str] = None
    video: Optional[str] = None


class DonasiBarangResponse(BaseModel):
    idBarangDonasi: int
    namaBarang: str
    kategori: Optional[str]
    status: str
    idDonatur: int
    idPenerima: int
    caraPengiriman: str

    class Config:
        orm_mode = True
