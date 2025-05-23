from fastapi import APIRouter

from api.routes import login, utils

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(utils.router)
