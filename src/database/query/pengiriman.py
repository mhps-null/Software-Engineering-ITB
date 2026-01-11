from sqlmodel import Session, select
from database.connection import engine
from models.models import PengirimanEntity


def GetPengirimanById(idPengiriman: int):
    with Session(engine) as session:
        return session.get(PengirimanEntity, idPengiriman)


def GetAllPengiriman():
    with Session(engine) as session:
        return session.exec(select(PengirimanEntity)).all()


def GetPengirimanByTransaksi(idTransaksi: int):
    with Session(engine) as session:
        return session.exec(
            select(PengirimanEntity).where(PengirimanEntity.idTransaksi == idTransaksi)
        ).all()


def InsertPengiriman(data: dict):
    with Session(engine) as session:
        kirim = PengirimanEntity(**data)
        session.add(kirim)
        session.commit()
        session.refresh(kirim)
        return kirim


def UpdatePengiriman(idPengiriman: int, data: dict):
    with Session(engine) as session:
        kirim = session.get(PengirimanEntity, idPengiriman)
        if kirim is None:
            return None

        for key, value in data.items():
            setattr(kirim, key, value)

        session.add(kirim)
        session.commit()
        session.refresh(kirim)
        return kirim
