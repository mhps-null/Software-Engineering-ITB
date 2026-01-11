from sqlmodel import Session, select
from database.connection import engine
from models.models import PenjualEntity


def GetPenjualById(idPenjual: int):
    with Session(engine) as session:
        return session.get(PenjualEntity, idPenjual)


def GetAllPenjual():
    with Session(engine) as session:
        return session.exec(select(PenjualEntity)).all()


def GetPenjualByEmail(email: str):
    with Session(engine) as session:
        return session.exec(
            select(PenjualEntity).where(PenjualEntity.email == email)
        ).first()


def InsertPenjual(data: dict):
    with Session(engine) as session:
        penjual = PenjualEntity(**data)
        session.add(penjual)
        session.commit()
        session.refresh(penjual)
        return penjual


def UpdatePenjual(idPenjual: int, data: dict):
    with Session(engine) as session:
        penjual = session.get(PenjualEntity, idPenjual)
        if penjual is None:
            return None
        for key, value in data.items():
            setattr(penjual, key, value)
        session.add(penjual)
        session.commit()
        return penjual
