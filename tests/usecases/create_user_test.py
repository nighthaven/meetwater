from datetime import datetime

from src.routes.dto.user.user_query import UserQuery
from src.usecases.create_user import create_user
from datetime import date


class TestCreateUser:
    def test_create_user(self, user_repo, security):
        birth_date = date.today().replace(year=date.today().year - 18)
        payload = UserQuery(
            email="hello123@gmail.com",
            password="pass",
            first_name="Tom",
            last_name="Bombadil",
            birth_date=birth_date,
        )
        create_user(payload, user_repo, security)

        query_user = user_repo.get()
        assert query_user[0].email == "hello123@gmail.com"
        assert security.verify_password("pass", query_user[0].password)
        assert query_user[0].first_name == "Tom"
        assert query_user[0].last_name == "Bombadil"
        assert query_user[0].created_at.replace(
            microsecond=0
        ) == datetime.now().replace(microsecond=0)
        assert query_user[0].birth_date == birth_date
