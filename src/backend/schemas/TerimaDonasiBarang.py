from pydantic import BaseModel

class UpdateStatusDonasiBarang(BaseModel):
    status: str

class DonasiBarangInfoResponse(BaseModel):
    namaBarang: str
    kategori: str
    status: str
    caraPengiriman: str