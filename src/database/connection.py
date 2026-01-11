from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from sqlalchemy.engine import make_url
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/yareu"


# Memastikan database sudah exist, sebaliknya maka database dibuat
def initialize_db(url: str) -> None:
    try:
        target = make_url(url)
        main_url = target.set(database="postgres")
        engine = create_engine(main_url, isolation_level="AUTOCOMMIT")

        with engine.connect() as conn:
            # Cek apakah database sudah ada
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": target.database},
            ).scalar()

            if not exists:
                logger.info(
                    f"Database '{target.database}' tidak ditemukan. Membuat database baru..."
                )
                conn.execute(text(f'CREATE DATABASE "{target.database}"'))
                logger.info(f"Database '{target.database}' berhasil dibuat!")
            else:
                logger.info(f"Database '{target.database}' sudah ada.")

        engine.dispose()
    except Exception as e:
        logger.error(f"Error saat initialize database: {e}")
        raise


# Initialize database
initialize_db(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    try:
        from models.models import (
            PenggunaEntity,
            DonaturEntity,
            PenerimaDonasiEntity,
            PenjualEntity,
            PembeliEntity,
            BarangEntity,
            BarangDonasiEntity,
            TransaksiEntity,
            PengirimanEntity,
        )

        logger.info("Membuat tables di database...")
        SQLModel.metadata.create_all(engine)
        logger.info("Semua tables berhasil dibuat!")
    except Exception as e:
        logger.error(f"Error saat membuat tables: {e}")
        raise


def get_session():
    with Session(engine) as session:
        yield session
