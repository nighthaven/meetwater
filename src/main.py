from fastapi import FastAPI

from src.routes.auth_routes import router as login_router
from src.routes.representative_routes import router as representative_router
from src.routes.swimmer_routes import router as swimmer_router
from src.routes.pool_manager_routes import router as pool_manager_router
from src.routes.swimming_coach_routes import router as swimming_coach_router
from src.routes.booking_routes import router as booking_router


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


routers = [
    login_router,
    representative_router,
    swimmer_router,
    pool_manager_router,
    swimming_coach_router,
    booking_router,
]
for router in routers:
    app.include_router(router)
