from src.models.admin import Admin
from src.routes.dto.admin.admin_query import AdminQuery
from src.usecases.admin.create_admin import create_admin_usecase


class TestCreateAdmin:
    def test_create_admin(self, admin_repo):
        query = AdminQuery(
            first_name="Tom",
            last_name="Valoteau",
            email="tom@meetwater.fr",
            raw_password="password123!",
        )

        create_admin_usecase(query, admin_repo)

        assert admin_repo.count() == 1
        admin = admin_repo.db.query(Admin).first()
        assert admin.first_name == query.first_name
        assert admin.last_name == query.last_name
        assert admin.user.email == query.email
