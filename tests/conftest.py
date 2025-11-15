import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models import get_db
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config

from src.repository.user_repository import UserRepository
from src.services.security import Security
from tests.fixtures.user_factory import UserFactory
import os


SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOSTNAME')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
metadata = MetaData()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db_session():
    """Fixture qui crée une session de base de données pour les tests."""
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture
def client(db_session):
    metadata.reflect(bind=engine)  # lie toutes donnée a la bdd
    metadata.drop_all(bind=engine)  # supprime tout
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

    UserFactory._meta.sqlalchemy_session = db_session

    yield TestClient(app)

    for table in reversed(metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()


# injection dépendance :


@pytest.fixture
def user_repo(db_session):
    return UserRepository(db_session)


@pytest.fixture
def security():
    return Security()  # type: ignore[no-untyped-call]
