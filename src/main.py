from fastapi import FastAPI, Depends
from src.routes.user_routes import router as user_router
from src.routes.auth_routes import router as login_router
from src.models.user import User
from src.services.security import Security

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

routers = [
    user_router,
    login_router,
]
for router in routers:
    app.include_router(router)

