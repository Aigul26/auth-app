from fastapi import FastAPI
from app.routes import router as users_router
def main() -> FastAPI:
    app = FastAPI()

    app.include_router(users_router)

    return app

app = main()