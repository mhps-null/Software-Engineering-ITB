from sqlmodel import Session, select
from database.connection import engine
from models.models import PenerimaDonasiEntity


def GetPenerimaById(idPenerima: int):
    with Session(engine) as session:
        return session.get(PenerimaDonasiEntity, idPenerima)


def GetPenerimaByEmail(email: str):
    with Session(engine) as session:
        return session.exec(
            select(PenerimaDonasiEntity).where(PenerimaDonasiEntity.email == email)
        ).first()


def GetPenerimaByPengguna(idPengguna: int):
    with Session(engine) as session:
        return session.exec(
            select(PenerimaDonasiEntity).where(
                PenerimaDonasiEntity.idPengguna == idPengguna
            )
        ).first()


def GetAllPenerima():
    with Session(engine) as session:
        return session.exec(select(PenerimaDonasiEntity)).all()


def InsertPenerima(data: dict):
    with Session(engine) as session:
        penerima = PenerimaDonasiEntity(**data)
        session.add(penerima)
        session.commit()
        session.refresh(penerima)
        return penerima


def UpdatePenerima(idPenerima: int, data: dict):
    with Session(engine) as session:
        penerima = session.get(PenerimaDonasiEntity, idPenerima)
        if penerima is None:
            return None
        for key, value in data.items():
            setattr(penerima, key, value)
        session.add(penerima)
        session.commit()
        return penerima
