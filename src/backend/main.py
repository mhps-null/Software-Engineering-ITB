from fastapi import FastAPI
from models.models import *
from database.connection import create_db_and_tables
from api.DonasiUangRoute import router as DonasiUangRouter
from api.DonasiBarangRoute import router as DonasiBarangRouter
from api.FullPaymentRoute import router as FullPaymentRouter
from api.AjuanTukarTambahRoute import router as AjuanTukarTambahRouter
from api.KonfirmasiDonasiRoute import router as KonfirmasiDonasiRouter
from api.KonfirmasiPenerimaanRoute import router as KonfirmasiPenerimaanRouter
from api.PengirimanRoute import router as PengirimanRouter
from api.PenjualanRoute import router as PenjualanRouter
from api.TerimaDonasiBarangRoute import router as TerimaDonasiBarangRouter
from api.TerimaDonasiUangRoute import router as TerimaDonasiUangRouter
from api.TukarTambahRoute import router as TukarTambahRouter

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(DonasiUangRouter)
app.include_router(DonasiBarangRouter)
app.include_router(FullPaymentRouter)
app.include_router(AjuanTukarTambahRouter)
app.include_router(KonfirmasiDonasiRouter)
app.include_router(KonfirmasiPenerimaanRouter)
app.include_router(PengirimanRouter)
app.include_router(PenjualanRouter)
app.include_router(TerimaDonasiBarangRouter)
app.include_router(TerimaDonasiUangRouter)
app.include_router(TukarTambahRouter)

@app.get("/")
async def root():
    return {"message": "Hello World"}