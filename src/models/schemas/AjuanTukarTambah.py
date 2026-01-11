from pydantic import BaseModel
from typing import Optional


class SetujuiAjuanRequest(BaseModel):
    idPembeli: int
    idBarang: int
    nilaiTambahan: Optional[int] = 0


class SimpanKeputusanAjuanRequest(BaseModel):
    keputusan: str


class AjuanTolakResponse(BaseModel):
    idAjuan: int
    status: str


class AjuanKeputusanResponse(BaseModel):
    idAjuan: int
    keputusan: str


class NilaiTukarTambahResponse(BaseModel):
    nilai: int
