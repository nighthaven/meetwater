from typing import List

from src.models.enums.swimmer_level import SwimmerLevel
from src.models.representative import Representative
from src.models.swimmer import Swimmer
from datetime import datetime, timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from src.models import get_db

ten_years = datetime.now() - timedelta(days=365 * 10)


class SwimmerSeeds:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create_swimmer_seeds(
        self, representatives: List[Representative]
    ) -> List[Swimmer]:
        swimmer_1 = Swimmer(
            first_name="Daisy",
            last_name="Johnson",
            birth_date=ten_years,
            level=SwimmerLevel.INTERMEDIATE,
            representatives_list=[  # type: ignore
                representative
                for representative in representatives
                if representative.full_name == "Phil Coulson"
            ],
        )
        swimmer_2 = Swimmer(
            first_name="River",
            last_name="Tam",
            birth_date=ten_years,
            level=SwimmerLevel.INTERMEDIATE,
            representatives_list=[  # type: ignore
                representative
                for representative in representatives
                if representative.full_name == "Malcolm Reynolds"
            ],
        )
        swimmer_3 = Swimmer(
            first_name="Amos",
            last_name="Burton",
            birth_date=ten_years,
            level=SwimmerLevel.INTERMEDIATE,
            representatives_list=[  # type: ignore
                representative
                for representative in representatives
                if representative.full_name == "James Holden"
            ],
        )
        swimmer_4 = Swimmer(
            first_name="Alex",
            last_name="Kamal",
            birth_date=ten_years,
            level=SwimmerLevel.INTERMEDIATE,
            representatives_list=[  # type: ignore
                representative
                for representative in representatives
                if representative.full_name == "James Holden"
            ],
        )
        swimmer_without_coach = Swimmer(
            first_name="Klaes",
            last_name="Ashford",
            birth_date=ten_years,
            level=SwimmerLevel.INTERMEDIATE,
            representatives_list=[  # type: ignore
                representative
                for representative in representatives
                if representative.full_name == "James Holden"
            ],
        )
        list_swimmers = [
            swimmer_1,
            swimmer_2,
            swimmer_3,
            swimmer_4,
            swimmer_without_coach,
        ]

        self.db.add_all(list_swimmers)
        self.db.flush()

        return list_swimmers
