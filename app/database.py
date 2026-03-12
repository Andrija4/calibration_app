from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_EQUIPMENT_URL = "sqlite:///./calibration.db"
DATABASE_MAIL_URL = "sqlite:///./mailing.db"

engine_equipment = create_engine(
    DATABASE_EQUIPMENT_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True
)
engine_mail = create_engine(
    DATABASE_MAIL_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine_equipment)
SessionLocalMail = sessionmaker(bind=engine_mail)
Base = declarative_base()

from sqlalchemy import event

@event.listens_for(engine_equipment, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

@event.listens_for(engine_mail, "connect")
def set_sqlite_pragma_mail(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()