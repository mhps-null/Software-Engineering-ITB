from sqlmodel import Session, select
from database.connection import engine
from models.models import DonaturEntity


def GetDonaturById(idDonatur: int):
    with Session(engine) as session:
        return session.get(DonaturEntity, idDonatur)


def GetAllDonatur():
    with Session(engine) as session:
        return session.exec(select(DonaturEntity)).all()


def GetDonaturByEmail(email: str):
    with Session(engine) as session:
        return session.exec(
            select(DonaturEntity).where(DonaturEntity.email == email)
        ).first()


def InsertDonatur(data: dict):
    with Session(engine) as session:
        donatur = DonaturEntity(**data)
        session.add(donatur)
        session.commit()
        session.refresh(donatur)
        return donatur


def UpdateDonatur(idDonatur: int, data: dict):
    with Session(engine) as session:
        donatur = session.get(DonaturEntity, idDonatur)
        if donatur is None:
            return None
        for key, value in data.items():
            setattr(donatur, key, value)
        session.add(donatur)
        session.commit()
        return donatur
