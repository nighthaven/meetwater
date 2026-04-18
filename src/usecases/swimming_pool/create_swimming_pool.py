from src.models.swimming_pool import SwimmingPool
from src.repositories.swimming_pool_repository import SwimmingPoolRepository
from src.routes.dto.swimming_pool.swimming_pool_query import SwimmingPoolQuery


def create_swimming_pool_usecase(
    query: SwimmingPoolQuery,
    swimming_pool_repository: SwimmingPoolRepository,
) -> SwimmingPool:
    swimming_pool = SwimmingPool(
        pool_name=query.pool_name,
        address=query.address,
        city=query.city,
        post_code=query.post_code,
    )
    swimming_pool_repository.save(swimming_pool)
    return swimming_pool
