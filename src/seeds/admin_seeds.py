from src.models.admin import Admin
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.services.security import Security


class AdminSeeds:
    twenty_years = datetime.now() - timedelta(days=365 * 20)

    def __init__(self, db: Session):
        self.db = db

    def create_admin_seeds(self) -> Admin:
        admin = Admin(
            first_name="Boris",
            last_name="Le Bon",
            email="boris@example.com",
            password=Security.hash_password("pass"),
        )

        self.db.add(admin)
        self.db.flush()

        return admin
