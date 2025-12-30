from src.models.swimmer import Swimmer
from src.usecases.swimmers.delete_swimmer import delete_swimmer_usecase
from tests.fixtures.representative_factory import RepresentativeFactory
from tests.fixtures.swimmer_factory import SwimmerFactory


class TestDeleteSwimmer:
    def test_delete_swimmer_linked_to_only_representative(
        self, swimmer_repo, authenticated_representative, db_session
    ):

        swimmer = SwimmerFactory(representatives=[authenticated_representative])

        delete_swimmer_usecase(swimmer.id, swimmer_repo, authenticated_representative)

        assert not authenticated_representative.swimmers
        swimmer_query = db_session.query(Swimmer).all()
        assert not swimmer_query

    def test_unassign_swimmer_linked_to_multiple_representatives(
        self, swimmer_repo, authenticated_representative, db_session
    ):
        another_representative = RepresentativeFactory()
        swimmer = SwimmerFactory(
            representatives=[authenticated_representative, another_representative]
        )

        delete_swimmer_usecase(swimmer.id, swimmer_repo, authenticated_representative)

        assert not authenticated_representative.swimmers
        swimmer_query = db_session.query(Swimmer).all()
        assert swimmer_query == [swimmer]

    def test_try_deleting_swimmer_assigned_to_other_representative(
        self, swimmer_repo, authenticated_representative, db_session
    ):
        another_representative = RepresentativeFactory()
        swimmer = SwimmerFactory(representatives=[another_representative])

        delete_swimmer_usecase(swimmer.id, swimmer_repo, authenticated_representative)

        swimmer_query = db_session.query(Swimmer).all()
        assert swimmer_query == [swimmer]
        assert (
            swimmer_query[0].representatives[0].representative == another_representative
        )
