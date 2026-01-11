from sqlmodel import Session, select
from database.connection import engine
from models.models import PenggunaEntity


def GetPenggunaById(idPengguna: int):
    with Session(engine) as session:
        return session.get(PenggunaEntity, idPengguna)


def GetAllPengguna():
    with Session(engine) as session:
        return session.exec(select(PenggunaEntity)).all()


def GetPenggunaByEmail(email: str):
    with Session(engine) as session:
        return session.exec(
            select(PenggunaEntity).where(PenggunaEntity.email == email)
        ).first()


def InsertPengguna(data: dict):
    with Session(engine) as session:
        pengguna = PenggunaEntity(**data)
        session.add(pengguna)
        session.commit()
        session.refresh(pengguna)
        return pengguna


def UpdatePengguna(idPengguna: int, data: dict):
    with Session(engine) as session:
        pengguna = session.get(PenggunaEntity, idPengguna)
        if pengguna is None:
            return None
        for key, value in data.items():
            setattr(pengguna, key, value)
        session.add(pengguna)
        session.commit()
        return pengguna
