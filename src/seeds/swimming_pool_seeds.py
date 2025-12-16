from sqlalchemy.orm import Session
from typing import List

from src.models.swimming_pool import SwimmingPool


class SwimmingPoolSeeds:
    def __init__(self, db: Session):
        self.db = db

    def create_swimming_pool_seeds(self) -> List[SwimmingPool]:
        swimming_pool_for_local_domain_test = SwimmingPool(
            pool_name="Test pool",
            address="11 Route de la Ramaz",
            city="Les tests",
            post_code="72170",
        )
        swimming_pool_1 = SwimmingPool(
            pool_name="Piscine de neuilly",
            address="hotel neuilly passy",
            city="Neuilly",
            post_code="92200",
        )
        swimming_pool_2 = SwimmingPool(
            pool_name="Piscine de la Grande Ourse",
            address="1111 Route de la Ramaz",
            city="Les Betex",
            post_code="74170",
        )

        list_swimming_pool = [
            swimming_pool_for_local_domain_test,
            swimming_pool_1,
            swimming_pool_2,
        ]

        self.db.add_all(list_swimming_pool)
        self.db.flush()

        return list_swimming_pool
