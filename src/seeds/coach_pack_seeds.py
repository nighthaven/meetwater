from typing import List
from sqlalchemy.orm import Session

from src.models.coach_pack import CoachPack
from src.models.swimming_coach import SwimmingCoach


class CoachPackSeeds:
    def __init__(self, db: Session):
        self.db = db

    def create_coach_pack_seeds(self, swimming_coaches: List[SwimmingCoach]):
        list_coach_pack = []
        for coach in swimming_coaches:
            pack = CoachPack(  # type: ignore[call-arg]
                swimming_coach_id=coach.id,
                sessions_count=1,
                price=20.00,
                final_price=20.00,
            )
            list_coach_pack.append(pack)

        pack_multi = CoachPack(  # type: ignore[call-arg]
            swimming_coach_id=[
                coach.id for coach in swimming_coaches if coach.full_name == "Aqua Man"
            ][0],
            sessions_count=10,
            price=20.00,
            final_price=180.00,
        )
        list_coach_pack.append(pack_multi)

        self.db.add_all(list_coach_pack)
        self.db.commit()
        return list_coach_pack
