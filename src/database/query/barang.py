from sqlmodel import Session, select
from database.connection import engine
from models.models import BarangEntity


def GetBarangById(idBarang: int):
    with Session(engine) as session:
        return session.get(BarangEntity, idBarang)


def GetAllBarang():
    with Session(engine) as session:
        return session.exec(select(BarangEntity)).all()


def GetBarangByPenjual(idPenjual: int):
    with Session(engine) as session:
        return session.exec(
            select(BarangEntity).where(BarangEntity.idPenjual == idPenjual)
        ).all()


def InsertBarang(data: dict):
    with Session(engine) as session:
        barang = BarangEntity(**data)
        session.add(barang)
        session.commit()
        session.refresh(barang)
        return barang


def UpdateBarang(idBarang: int, data: dict):
    with Session(engine) as session:
        barang = session.get(BarangEntity, idBarang)
        if barang is None:
            return None
        for key, value in data.items():
            setattr(barang, key, value)
        session.add(barang)
        session.commit()
        return barang
