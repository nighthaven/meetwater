from src.models.representative import Representative
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List


class RepresentativeSeeds:
    twenty_years = datetime.now() - timedelta(days=365 * 20)

    def __init__(self, db: Session):
        self.db = db

    def create_representatives_seeds(self) -> List[Representative]:
        representative_1 = Representative(
            first_name="Phil",
            last_name="Coulson",
            birth_date=self.twenty_years,
            email="philcoulson@example.com",
            password="pass",
        )
        representative_2 = Representative(
            first_name="Malcolm",
            last_name="Reynolds",
            birth_date=self.twenty_years,
            email="malcolm@example.com",
            password="pass",
        )
        representative_3 = Representative(
            first_name="James",
            last_name="Holden",
            birth_date=self.twenty_years,
            email="james@example.com",
            password="pass",
        )

        self.db.add_all([representative_1, representative_2, representative_3])
        self.db.flush()

        rep = [representative_1, representative_2, representative_3]
        return rep
