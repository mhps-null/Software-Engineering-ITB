from sqlmodel import Session, select
from database.connection import engine
from models.models import BarangDonasiEntity


def GetBarangDonasiById(idBarangDonasi: int):
    with Session(engine) as session:
        return session.get(BarangDonasiEntity, idBarangDonasi)


def GetAllBarangDonasi():
    with Session(engine) as session:
        return session.exec(select(BarangDonasiEntity)).all()


def GetBarangDonasiByDonatur(idDonatur: int):
    with Session(engine) as session:
        return session.exec(
            select(BarangDonasiEntity).where(BarangDonasiEntity.idDonatur == idDonatur)
        ).all()


def GetBarangDonasiByPenerima(idPenerima: int):
    with Session(engine) as session:
        return session.exec(
            select(BarangDonasiEntity).where(
                BarangDonasiEntity.idPenerima == idPenerima
            )
        ).all()


def InsertBarangDonasi(data: dict):
    with Session(engine) as session:
        barang = BarangDonasiEntity(**data)
        session.add(barang)
        session.commit()
        session.refresh(barang)
        return barang


def UpdateBarangDonasi(idBarangDonasi: int, data: dict):
    with Session(engine) as session:
        barang = session.get(BarangDonasiEntity, idBarangDonasi)
        if barang is None:
            return None
        for key, value in data.items():
            setattr(barang, key, value)
        session.add(barang)
        session.commit()
        return barang
