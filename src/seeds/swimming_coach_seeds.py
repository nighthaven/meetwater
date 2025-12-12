from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta

from src.models.link.swimmers_coachs import SwimmerCoach
from src.models.swimmer import Swimmer
from src.models.swimming_coach import SwimmingCoach
from src.models.swimming_pool import SwimmingPool


class SwimmingCoachSeeds:
    two_years = date.today() - timedelta(days=365 * 2)
    six_month = date.today() - timedelta(days=182)

    def __init__(self, db: Session):
        self.db = db

    def create_swimming_coach_seeds(
        self, swimmers: List[Swimmer], swimming_pools: List[SwimmingPool]
    ) -> List[SwimmingCoach]:
        swimming_coach_without_swimmer = SwimmingCoach(
            first_name="Bruce",
            last_name="Wayne",
            last_caep_certification_date=self.two_years,
            last_pse_certification_date=self.six_month,
            email="brucewayne@example.com",
            password="pass",
            swimming_pool_id=swimming_pools[0].id,
        )

        swimming_coach_1 = SwimmingCoach(
            first_name="Aqua",
            last_name="Man",
            last_caep_certification_date=self.two_years,
            last_pse_certification_date=self.six_month,
            swimming_pool_id=swimming_pools[0].id,
            email="aquaman@example.com",
            password="pass",
        )
        swimming_coach_1.swimmers = [
            SwimmerCoach(swimmer=swimmer)
            for swimmer in swimmers
            if swimmer.full_name == "Daisy Johnson"
        ]

        swimming_coach_2 = SwimmingCoach(
            first_name="Diana",
            last_name="Prince",
            last_caep_certification_date=self.two_years,
            last_pse_certification_date=self.six_month,
            swimming_pool_id=swimming_pools[0].id,
            email="wonderwoman@example.com",
            password="pass",
        )
        swimming_coach_2.swimmers = [
            SwimmerCoach(swimmer=swimmer)
            for swimmer in swimmers
            if swimmer.full_name == "River Tam"
        ]

        swimming_coach_with_two_swimmers = SwimmingCoach(
            first_name="Klark",
            last_name="Kent",
            last_caep_certification_date=self.two_years,
            last_pse_certification_date=self.six_month,
            swimming_pool_id=swimming_pools[0].id,
            email="superman@example.com",
            password="pass",
        )
        swimming_coach_with_two_swimmers.swimmers = [
            SwimmerCoach(swimmer=s)
            for s in swimmers
            if s.full_name in ["Amos Burton", "Alex Kamal"]
        ]

        swimming_coach_from_other_swimming_pool = SwimmingCoach(
            first_name="Peter",
            last_name="Parker",
            last_caep_certification_date=self.two_years,
            last_pse_certification_date=self.six_month,
            swimming_pool_id=swimming_pools[1].id,
            email="peterparker@example.com",
            password="pass",
        )

        coaches = [
            swimming_coach_without_swimmer,
            swimming_coach_1,
            swimming_coach_2,
            swimming_coach_with_two_swimmers,
            swimming_coach_from_other_swimming_pool,
        ]

        self.db.add_all(coaches)
        self.db.flush()

        return coaches
