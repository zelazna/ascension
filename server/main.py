from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.main import api_router
from core.config import settings


app = FastAPI(
    title="Ascension API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
