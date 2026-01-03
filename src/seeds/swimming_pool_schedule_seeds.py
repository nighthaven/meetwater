from sqlalchemy.orm import Session
from datetime import time
from typing import List

from src.models.enums.day_of_week import DayOfWeek
from src.models.swimming_pool import SwimmingPool
from src.models.swimming_pool_schedule import SwimmingPoolSchedule


class SwimmingPoolScheduleSeeds:
    def __init__(self, db: Session):
        self.db = db

    def create_swimming_pool_schedule(self, swimming_pools: List[SwimmingPool]) -> None:
        list_schedules = []
        for swimming_pool in swimming_pools:
            for day in DayOfWeek:
                schedule = SwimmingPoolSchedule(  # type: ignore[call-arg]
                    swimming_pool_id=swimming_pool.id,
                    day_of_week=day,
                    opening_time=time(hour=10, minute=0),
                    closing_time=time(hour=18, minute=0),
                )
                list_schedules.append(schedule)
        self.db.add_all(list_schedules)
        self.db.commit()
