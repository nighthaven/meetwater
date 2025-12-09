from src.seeds.admin_seeds import AdminSeeds
from src.seeds.representative_seeds import RepresentativeSeeds
from src.models import SessionLocal
from src.seeds.clear_tables import clear_tables
from src.seeds.swimmer_seeds import SwimmerSeeds


def seed_all() -> None:
    session = SessionLocal()
    clear_tables(session)  # type: ignore

    admin_seeds = AdminSeeds(db=session)
    representative_seeds = RepresentativeSeeds(db=session)
    swimmer_seeds = SwimmerSeeds(db=session)

    admin_seeds.create_admin_seeds()
    representatives = representative_seeds.create_representatives_seeds()
    swimmer_seeds.create_swimmer_seeds(representatives)

    session.commit()
    session.close()
    print("seeds all done with success!")


if __name__ == "__main__":
    seed_all()
