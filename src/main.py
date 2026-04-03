from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.routes.auth_routes import router as login_router
from src.routes.representative_routes import router as representative_router
from src.routes.swimmer_routes import router as swimmer_router
from src.routes.pool_manager_routes import router as pool_manager_router
from src.routes.swimming_coaches_routes import router as swimming_coach_router
from src.routes.booking_routes import router as booking_router
from src.routes.swimming_pool_routes import router as swimming_pool_router
from src.routes.coach_schedules_routes import router as coach_schedules_router
from src.routes.coach_pack_routes import router as coach_pack_router


app = FastAPI()

allowed_origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    swimming_pool_router,
    coach_schedules_router,
    coach_pack_router,
]
for router in routers:
    app.include_router(router)
