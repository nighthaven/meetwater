from src.models.link.swimmer_user_link import SwimmerUserLink
from src.models.swimmer import Swimmer
import factory

from tests.fixtures.user_factory import UserFactory


class SwimmerFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = Swimmer
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birth_date = factory.Faker("date_of_birth", minimum_age=5, maximum_age=17)

    user_links = factory.LazyFunction(lambda: [])

    @factory.post_generation
    def link_user(self, create, extracted, **kwargs):

        user = extracted or UserFactory()
        link = SwimmerUserLinkFactory(user=user, swimmer=self)
        self.user_links.append(link)


class SwimmerUserLinkFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = SwimmerUserLink
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    user = factory.SubFactory(UserFactory)
    swimmer = factory.SubFactory(SwimmerFactory)
