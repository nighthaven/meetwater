from typing import List

from src.models.enums.swimmer_level import SwimmerLevel
from src.models.link.swimmer_representative import SwimmerRepresentative
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
        swimmer_1 = Swimmer(  # type: ignore[call-arg]
            first_name="Daisy",
            last_name="Johnson",
            birth_date=ten_years,
            level=SwimmerLevel.INTERMEDIATE,
        )
        swimmer_2 = Swimmer(  # type: ignore[call-arg]
            first_name="River",
            last_name="Tam",
            birth_date=ten_years,
            level=SwimmerLevel.INTERMEDIATE,
        )
        swimmer_3 = Swimmer(  # type: ignore[call-arg]
            first_name="Amos",
            last_name="Burton",
            birth_date=ten_years,
            level=SwimmerLevel.INTERMEDIATE,
        )
        swimmer_4 = Swimmer(  # type: ignore[call-arg]
            first_name="Alex",
            last_name="Kamal",
            birth_date=ten_years,
            level=SwimmerLevel.INTERMEDIATE,
        )
        swimmer_without_coach = Swimmer(  # type: ignore[call-arg]
            first_name="Klaes",
            last_name="Ashford",
            birth_date=ten_years,
            level=SwimmerLevel.INTERMEDIATE,
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

        swimmer_1_representative = SwimmerRepresentative(  # type: ignore[call-arg]
            swimmer_id=swimmer_1.id,
            representative_id=[
                representative.id
                for representative in representatives
                if representative.full_name == "Phil Coulson"
            ][0],
        )
        swimmer_2_representative = SwimmerRepresentative(  # type: ignore[call-arg]
            swimmer_id=swimmer_2.id,
            representative_id=[
                representative.id
                for representative in representatives
                if representative.full_name == "Malcolm Reynolds"
            ][0],
        )
        swimmer_3_representative = SwimmerRepresentative(  # type: ignore[call-arg]
            swimmer_id=swimmer_3.id,
            representative_id=[
                representative.id
                for representative in representatives
                if representative.full_name == "James Holden"
            ][0],
        )
        swimmer_4_representative = SwimmerRepresentative(  # type: ignore[call-arg]
            swimmer_id=swimmer_4.id,
            representative_id=[
                representative.id
                for representative in representatives
                if representative.full_name == "James Holden"
            ][0],
        )
        swimmer_without_coach_representative = SwimmerRepresentative(  # type: ignore[call-arg]
            swimmer_id=swimmer_without_coach.id,
            representative_id=[
                representative.id
                for representative in representatives
                if representative.full_name == "James Holden"
            ][0],
        )
        list_swimmers_representatives = [
            swimmer_1_representative,
            swimmer_2_representative,
            swimmer_3_representative,
            swimmer_4_representative,
            swimmer_without_coach_representative,
        ]
        self.db.add_all(list_swimmers_representatives)
        self.db.flush()

        return list_swimmers
