from sqlmodel import Session, select
from database.connection import engine
from models.models import TransaksiEntity


def GetTransaksiById(idTransaksi: int):
    with Session(engine) as session:
        return session.get(TransaksiEntity, idTransaksi)


def GetTransaksiByBarang(idBarang: int):
    with Session(engine) as session:
        return session.exec(
            select(TransaksiEntity).where(TransaksiEntity.idBarang == idBarang)
        ).all()


def GetTransaksiByPembeli(idPembeli: int):
    with Session(engine) as session:
        return session.exec(
            select(TransaksiEntity).where(TransaksiEntity.idPembeli == idPembeli)
        ).all()


def InsertTransaksi(data: dict):
    with Session(engine) as session:
        transaksi = TransaksiEntity(**data)
        session.add(transaksi)
        session.commit()
        session.refresh(transaksi)
        return transaksi


def UpdateTransaksi(idTransaksi: int, data: dict):
    with Session(engine) as session:
        transaksi = session.get(TransaksiEntity, idTransaksi)
        if transaksi is None:
            return None
        for key, value in data.items():
            setattr(transaksi, key, value)
        session.add(transaksi)
        session.commit()
        return transaksi
