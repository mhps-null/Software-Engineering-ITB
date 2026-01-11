from pydantic import BaseModel


class UpdateStatusPengirimanRequest(BaseModel):
    status: str


class KonfirmasiPenerimaanResponse(BaseModel):
    status: str
