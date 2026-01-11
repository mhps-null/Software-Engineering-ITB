from fastapi import APIRouter
from controllers.AjuanTukarTambahManager import AjuanTukarTambahManager
from schemas.AjuanTukarTambah import *

# C-25: Ajuan Tukar Tambah
router = APIRouter(prefix="/ajuan-tukar-tambah", tags=["Ajuan Tukar Tambah"])
manager = AjuanTukarTambahManager()

# Setujui Ajuan
@router.post("/setujui")
def setujuiAjuan(data: SetujuiAjuanRequest):
    return manager.setujuiAjuan(data.model_dump())

# Tolak Ajuan
@router.patch("/{id_ajuan}/tolak", response_model=AjuanTolakResponse)
def tolakAjuan(id_ajuan: int):
    return manager.tolakAjuan(id_ajuan)

# Simpan Keputusan Ajuan
@router.patch("/{id_ajuan}/keputusan", response_model=AjuanKeputusanResponse)
def simpanKeputusan(id_ajuan: int, body: SimpanKeputusanAjuanRequest):
    return manager.simpanKeputusanAjuan(id_ajuan, body.keputusan)

# Hitung Nilai Tukar Tambah
@router.get("/{id_ajuan}/nilai", response_model=NilaiTukarTambahResponse)
def hitungNilai(id_ajuan: int):
    nilai = manager.hitungNilaiTukarTambah(id_ajuan)
    return {"nilai": nilai}