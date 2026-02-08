from uuid import UUID
import pytest

from src.exceptions.coach_pack.coach_pack_do_not_belong_to_coach import (
    CoachPackDoNotBelongToCoach,
)
from src.usecases.coach_pack.delete_coach_pack_usecase import delete_coach_pack_usecase
from tests.fixtures.coach_pack_factory import CoachPackFactory


class TestDeleteCoachPackUsecase:
    def test_delete_coach_pack(self, authenticated_swimming_coach, coach_pack_repo):
        coach_pack = CoachPackFactory(swimming_coach=authenticated_swimming_coach)

        delete_coach_pack_usecase(
            coach_pack.id, authenticated_swimming_coach, coach_pack_repo
        )

        coach_pack_query = coach_pack_repo.get()
        assert not coach_pack_query

    def test_delete_coach_pack_not_found(
        self, authenticated_swimming_coach, coach_pack_repo
    ):

        with pytest.raises(CoachPackDoNotBelongToCoach):
            delete_coach_pack_usecase(
                UUID("9b23ba83-435e-4eb3-80d8-d42439f20523"),
                authenticated_swimming_coach,
                coach_pack_repo,
            )

    def test_delete_coach_pack_doesnt_belong_to_current_coach(
        self, authenticated_swimming_coach, coach_pack_repo
    ):
        coach_pack = CoachPackFactory()
        with pytest.raises(CoachPackDoNotBelongToCoach):
            delete_coach_pack_usecase(
                coach_pack.id,
                authenticated_swimming_coach,
                coach_pack_repo,
            )
