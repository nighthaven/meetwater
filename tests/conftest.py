import pytest
from unittest.mock import Mock
from fastapi import Request
from fastapi.testclient import TestClient
from src.main import app
from src.models import get_db, Base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from typing import Dict, Optional

from src.models.admin import Admin
from src.models.pool_manager import PoolManager
from src.models.representative import Representative
from src.models.swimming_coach import SwimmingCoach
from src.repositories.booking_repository import BookingRepository
from src.repositories.coach_schedule_repository import CoachScheduleRepository
from src.repositories.pool_manager_repository import PoolManagerRepository
from src.repositories.representative_repository import RepresentativeRepository
from src.repositories.swimmer_repository import SwimmerRepository
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.repositories.swimming_pool_repository import SwimmingPoolRepository
from src.services.security import Security
from tests.fixtures.admin_factory import AdminFactory
from tests.fixtures.booking_factory import BookingFactory, SwimmerBookingFactory
from tests.fixtures.coach_schedule_factory import CoachScheduleFactory
from tests.fixtures.pool_manager_factory import PoolManagerFactory
from tests.fixtures.representative_factory import RepresentativeFactory
from tests.fixtures.swimmer_factory import SwimmerFactory, SwimmerRepresentativeFactory
from tests.fixtures.swimming_coach_factory import (
    SwimmingCoachFactory,
    SwimmerCoachFactory,
)
from tests.fixtures.swimming_pool_factory import SwimmingPoolFactory
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


@pytest.fixture
def db_session():
    """Fixture qui crée une session de base de données pour les tests."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def client(db_session):
    def override():
        yield db_session

    app.dependency_overrides[get_db] = override
    metadata.reflect(bind=engine)  # lie toutes donnée a la bdd
    metadata.drop_all(bind=engine)  # supprime tout
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

    yield TestClient(app)

    for table in reversed(metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()


@pytest.fixture(autouse=True)
def configure_factories(db_session):
    for factory in [
        UserFactory,
        SwimmingPoolFactory,
        RepresentativeFactory,
        SwimmerFactory,
        SwimmerRepresentativeFactory,
        BookingFactory,
        SwimmerBookingFactory,
        AdminFactory,
        PoolManagerFactory,
        SwimmingCoachFactory,
        SwimmerCoachFactory,
        CoachScheduleFactory,
    ]:
        factory._meta.sqlalchemy_session = db_session  # type: ignore[attr-defined]


# injection dépendance :


@pytest.fixture
def representative_repo(db_session):
    return RepresentativeRepository(db_session)


@pytest.fixture
def swimmer_repo(db_session):
    return SwimmerRepository(db_session)


@pytest.fixture
def booking_repo(db_session):
    return BookingRepository(db_session)


@pytest.fixture
def pool_manager_repo(db_session):
    return PoolManagerRepository(db_session)


@pytest.fixture
def swimming_coach_repo(db_session):
    return SwimmingCoachRepository(db_session)


@pytest.fixture
def swimming_pool_repo(db_session):
    return SwimmingPoolRepository(db_session)


@pytest.fixture
def coach_schedule_repo(db_session):
    return CoachScheduleRepository(db_session)


@pytest.fixture
def security():
    return Security()


@pytest.fixture
def authenticated_admin(db_session):
    admin = AdminFactory()
    db_session.add(admin)
    db_session.commit()
    return admin


@pytest.fixture
def authenticated_pool_manager(db_session):
    swimming_pool = SwimmingPoolFactory()
    pool_manager = PoolManagerFactory(swimming_pool_id=swimming_pool.id)
    db_session.add(swimming_pool)
    db_session.add(pool_manager)
    db_session.commit()
    return pool_manager


@pytest.fixture
def authenticated_representative(db_session):
    representative = RepresentativeFactory()
    db_session.add(representative)
    db_session.commit()
    return representative


@pytest.fixture
def authenticated_swimming_coach(db_session):
    swimming_pool = SwimmingPoolFactory()
    swimming_coach = SwimmingCoachFactory(swimming_pool_id=swimming_pool.id)
    db_session.add(swimming_pool)
    db_session.add(swimming_coach)
    db_session.commit()
    return swimming_coach


class AuthenticatedClient:
    def __init__(self, client: TestClient, token: str, user_type):
        self.client = client
        self.token = token
        self.user_type = user_type

    def _inject_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        headers = headers or {}
        headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get(self, url, **kwargs):
        kwargs["headers"] = self._inject_headers(kwargs.get("headers"))
        return self.client.get(url, **kwargs)

    def post(self, url, **kwargs):
        kwargs["headers"] = self._inject_headers(kwargs.get("headers"))
        return self.client.post(url, **kwargs)

    def delete(self, url, **kwargs):
        kwargs["headers"] = self._inject_headers(kwargs.get("headers"))
        return self.client.delete(url, **kwargs)

    def put(self, url, **kwargs):
        kwargs["headers"] = self._inject_headers(kwargs.get("headers"))
        return self.client.put(url, **kwargs)


@pytest.fixture
def make_authenticated_client(client, security):
    def _make(user_type, domain):
        token = security.create_access_token(
            {
                "user_id": str(user_type.user.id),
                "swimming_pool_id": str(domain.id),
                "admin_id": str(user_type.id) if isinstance(user_type, Admin) else None,
                "pool_manager_id": (
                    str(user_type.id) if isinstance(user_type, PoolManager) else None
                ),
                "representative_id": (
                    str(user_type.id) if isinstance(user_type, Representative) else None
                ),
                "swimming_coach_id": (
                    str(user_type.id) if isinstance(user_type, SwimmingCoach) else None
                ),
            }
        )
        return AuthenticatedClient(client, token, user_type)

    return _make


@pytest.fixture
def admin_client(db_session, make_authenticated_client):
    admin = AdminFactory()
    swimming_pool = SwimmingPoolFactory(pool_name="swimming pool for domain")
    db_session.commit()
    return make_authenticated_client(admin, swimming_pool)


@pytest.fixture
def pool_manager_client(db_session, make_authenticated_client):
    pool_manager = PoolManagerFactory()
    swimming_pool = SwimmingPoolFactory(pool_name="swimming pool for domain")
    db_session.commit()
    return make_authenticated_client(pool_manager, swimming_pool)


@pytest.fixture
def representative_client(db_session, make_authenticated_client):
    representative = RepresentativeFactory()
    swimming_pool = SwimmingPoolFactory(pool_name="swimming pool for domain")
    db_session.commit()
    return make_authenticated_client(representative, swimming_pool)


@pytest.fixture
def swimming_coach_client(db_session, make_authenticated_client):
    swimming_coach = SwimmingCoachFactory(swimmers=[SwimmerFactory()])
    swimming_pool = SwimmingPoolFactory(pool_name="swimming pool for domain")
    db_session.commit()
    return make_authenticated_client(swimming_coach, swimming_pool)


@pytest.fixture
def mock_request_with_subdomain():
    def _create_mock_request(subdomain: str):
        mock_request = Mock(spec=Request)
        mock_headers = Mock()
        mock_headers.get.return_value = subdomain
        mock_request.headers = mock_headers
        return mock_request

    return _create_mock_request
