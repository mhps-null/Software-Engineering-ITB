from pydantic import BaseModel

class UpdateStatusKonfirmasiRequest(BaseModel):
    status: str

class StatusKonfirmasiResponse(BaseModel):
    status: str

class NotifikasiKonfirmasiResponse(BaseModel):
    pesan: str