from fastapi import FastAPI

from api.v100.router import router


def get_application() -> FastAPI:
    application = FastAPI()

    application.include_router(router, prefix="/v100")
    return application


app = get_application()


@app.get("/")
def home():
    return {"Service": "API users"}

