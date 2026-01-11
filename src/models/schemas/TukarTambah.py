from pydantic import BaseModel
from typing import Optional


class CreateTukarTambah(BaseModel):
    idBarangBaru: int
    idPembeli: int
    nilaiTambahan: Optional[int] = 0


class TukarTambahResponse(BaseModel):
    idTransaksi: int
    idBarang: int
    idPembeli: int
    jumlah: int
    kuantitas: int
    status: str
    jenisTransaksi: str
    tanggal: str

    class Config:
        orm_mode = True


class BatalTukarTambahResponse(BaseModel):
    id: int
    status: str
