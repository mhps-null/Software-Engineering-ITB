from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from sqlalchemy.engine import make_url

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/yareu"

# Memastikan database sudah exist, sebaliknya maka database dibuat
def initialize_db(url: str) -> None:
    target = make_url(url)
    main_url = target.set(database="postgres")
    engine = create_engine(main_url, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": target.database},
        ).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{target.database}"'))

initialize_db(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session