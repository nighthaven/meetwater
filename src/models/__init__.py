# ruff: noqa: F401
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.config import settings


def install_models() -> None:
    from src.models import user
    from src.models import representative
    from src.models import swimmer
    from src.models.link import swimmer_representative
    from src.models import booking
    from src.models.link import swimmers_bookings
    from src.models import swimming_coach
    from src.models.link import swimmers_coachs
    from src.models import pool_manager
    from src.models import admin


SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # type: ignore
install_models()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
