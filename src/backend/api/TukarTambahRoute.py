from fastapi import APIRouter
from controllers.TukarTambahManager import TukarTambahManager
from schemas.TukarTambah import *

# C-23: Tukar Tambah
router = APIRouter(prefix="/tukar-tambah", tags=["Tukar Tambah"])
manager = TukarTambahManager()

# 1. Buat Tukar Tambah
@router.post("/", response_model=TukarTambahResponse)
def buatTukarTambah(data: CreateTukarTambah):
    return manager.buatTukarTambah(data.model_dump())

# 2. Batalkan Tukar Tambah
@router.patch("/{id_tukar}/batal", response_model=BatalTukarTambahResponse)
def batalTukarTambah(id_tukar: int):
    return manager.batalTukarTambah(id_tukar)