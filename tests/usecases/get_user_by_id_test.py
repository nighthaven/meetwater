from src.usecases.get_user import get_user_by_id_usecase
from tests.fixtures.swimmer_factory import SwimmerFactory
from tests.fixtures.user_factory import UserFactory


class TestGetUserById:
    def test_get_user_by_id_success(self, user_repo, db_session):
        user = UserFactory()
        swimmer = SwimmerFactory(link_user=user)

        db_session.commit()

        response = get_user_by_id_usecase(user.id, user_repo)

        assert response["first_name"] == user.first_name
        assert response["last_name"] == user.last_name
        assert response["email"] == user.email
        assert response["swimmers"][0]["first_name"] == swimmer.first_name
        assert response["swimmers"][0]["last_name"] == swimmer.last_name
        assert response["swimmers"][0]["birth_date"] == swimmer.birth_date
        assert response["swimmers"][0]["level"] == swimmer.level
