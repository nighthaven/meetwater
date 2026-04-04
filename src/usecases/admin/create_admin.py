from src.models.admin import Admin
from src.repositories.admin_repository import AdminRepository
from src.routes.dto.admin.admin_query import AdminQuery
from src.services.security import Security


def create_admin_usecase(
    query: AdminQuery,
    admin_repository: AdminRepository,
) -> None:
    admin = Admin(
        first_name=query.first_name,
        last_name=query.last_name,
        email=query.email,
        password=Security.hash_password(query.raw_password),
    )
    admin_repository.save(admin)
