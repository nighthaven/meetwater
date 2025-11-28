from src.models.representative import Representative
from src.repositories.representative_repository import RepresentativeRepository
from src.routes.dto.representative.query_representative import QueryRepresentative
from src.services.security import Security


def create_representative_usecase(
    query_representative: QueryRepresentative,
    security: Security,
    representative_repository: RepresentativeRepository,
) -> None:
    representative = Representative(
        first_name=query_representative.first_name,
        last_name=query_representative.last_name,
        birth_date=query_representative.birth_date,
        email=query_representative.email,
        password=security.hash_password(query_representative.raw_password),
    )

    representative_repository.save(representative)

    return
