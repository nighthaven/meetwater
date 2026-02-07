from src.routes.dto.coach_pack.coach_pack_query import CoachPackQuery
from src.usecases.coach_pack.create_coach_pack_usecase import create_coach_pack_usecase
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory


class TestCreateCoachPackUsecase:
    def test_create_coach_pack_usecase(self, coach_pack_repo):
        swimming_coach = SwimmingCoachFactory()

        query = CoachPackQuery(
            sessions_count=1,
            price=2000,
            final_price=2000,
        )
        create_coach_pack_usecase(query, coach_pack_repo, swimming_coach)

        query_coach_pack = coach_pack_repo.get()
        assert len(query_coach_pack) == 1
        assert query_coach_pack[0].swimming_coach_id == swimming_coach.id
        assert query_coach_pack[0].sessions_count == 1
        assert query_coach_pack[0].final_price == 2000
        assert query_coach_pack[0].price == 2000
        assert query_coach_pack[0].active
