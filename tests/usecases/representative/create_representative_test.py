from src.routes.dto.representative.query_representative import QueryRepresentative
from datetime import date, timedelta

from src.usecases.representative.create_representative import (
    create_representative_usecase,
)


class TestCreateRepresentative:
    def test_create_representative_success(self, security, representative_repo):
        birthdate_more_18_years = 19 * 365
        date_19_years = date.today() - timedelta(days=birthdate_more_18_years)
        query = QueryRepresentative(
            first_name="John",
            last_name="Doe",
            birth_date=date_19_years,
            email="JohnDoe@gmail.com",
            raw_password="password",
        )
        create_representative_usecase(query, security, representative_repo)
        query_representative = representative_repo.get()
        assert query_representative[0].first_name == "John"
        assert query_representative[0].last_name == "Doe"
        assert query_representative[0].birth_date == date_19_years
