from sqlmodel import Session, select
from database.connection import engine
from models.models import PembeliEntity


def GetPembeliById(idPembeli: int):
    with Session(engine) as session:
        return session.get(PembeliEntity, idPembeli)


def GetAllPembeli():
    with Session(engine) as session:
        return session.exec(select(PembeliEntity)).all()


def GetPembeliByEmail(email: str):
    with Session(engine) as session:
        return session.exec(
            select(PembeliEntity).where(PembeliEntity.email == email)
        ).first()


def InsertPembeli(data: dict):
    with Session(engine) as session:
        pembeli = PembeliEntity(**data)
        session.add(pembeli)
        session.commit()
        session.refresh(pembeli)
        return pembeli


def UpdatePembeli(idPembeli: int, data: dict):
    with Session(engine) as session:
        pembeli = session.get(PembeliEntity, idPembeli)
        if pembeli is None:
            return None
        for key, value in data.items():
            setattr(pembeli, key, value)
        session.add(pembeli)
        session.commit()
        return pembeli
