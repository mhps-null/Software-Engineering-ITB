from pydantic import BaseModel
from typing import Optional

class UpdateStatusDonasiUang(BaseModel):
    status: str

class DonasiUangInfoResponse(BaseModel):
    jumlah: int
    status: str
    metodePembayaran: Optional[str]
    tanggal: Optional[str]