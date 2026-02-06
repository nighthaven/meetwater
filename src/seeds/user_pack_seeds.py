from sqlalchemy.orm import Session
from typing import List

from src.models.enums.pack_status import PackStatus
from src.models.representative import Representative
from src.models.swimming_coach import SwimmingCoach
from src.models.user_pack import UserPack


class UserPackSeeds:
    def __init__(self, db: Session):
        self.db = db

    def create_user_pack(
        self,
        representatives: List[Representative],
        swimming_coaches: List[SwimmingCoach],
    ):
        coulson_user_pack = UserPack(  # type: ignore[call-arg]
            representative_id=[
                representative.id
                for representative in representatives
                if representative.full_name == "Phil Coulson"
            ][0],
            swimming_coach_id=[
                coach.id for coach in swimming_coaches if coach.full_name == "Aqua Man"
            ][0],
            sessions_total=1,
            sessions_remaining=1,
            price_paid=20.00,
            status=PackStatus.PAID,
        )
        old_pack_coulson = UserPack(  # type: ignore[call-arg]
            representative_id=[
                representative.id
                for representative in representatives
                if representative.full_name == "Phil Coulson"
            ][0],
            swimming_coach_id=[
                coach.id for coach in swimming_coaches if coach.full_name == "Aqua Man"
            ][0],
            sessions_total=10,
            sessions_remaining=0,
            price_paid=180.00,
            status=PackStatus.USED,
        )
        self.db.add_all([coulson_user_pack, old_pack_coulson])
        self.db.commit()
        return [coulson_user_pack, old_pack_coulson]
