from src.seeds.admin_seeds import AdminSeeds
from src.seeds.bookings_seeds import BookingsSeeds
from src.seeds.coach_schedule_seeds import CoachScheduleSeeds
from src.seeds.representative_seeds import RepresentativeSeeds
from src.models import SessionLocal
from src.seeds.clear_tables import clear_tables
from src.seeds.swimmer_seeds import SwimmerSeeds
from src.seeds.swimming_coach_seeds import SwimmingCoachSeeds
from src.seeds.swimming_pool_seeds import SwimmingPoolSeeds


def seed_all() -> None:
    session = SessionLocal()
    clear_tables(session)  # type: ignore

    admin_seeds = AdminSeeds(db=session)
    representative_seeds = RepresentativeSeeds(db=session)
    swimmer_seeds = SwimmerSeeds(db=session)
    swimming_pool_seeds = SwimmingPoolSeeds(db=session)
    swimming_coach_seeds = SwimmingCoachSeeds(db=session)
    coaches_schedules_seeds = CoachScheduleSeeds(db=session)
    booking_seeds = BookingsSeeds(db=session)

    admin_seeds.create_admin_seeds()
    representatives = representative_seeds.create_representatives_seeds()
    swimmers = swimmer_seeds.create_swimmer_seeds(representatives)
    swimming_pools = swimming_pool_seeds.create_swimming_pool_seeds()
    swimming_coaches = swimming_coach_seeds.create_swimming_coach_seeds(
        swimmers, swimming_pools
    )
    coaches_schedules_seeds.create_coach_schedule(swimming_coaches)
    booking_seeds.create_bookings_seeds(representatives)

    session.commit()
    session.close()
    print("seeds all done with success!")


if __name__ == "__main__":
    seed_all()
