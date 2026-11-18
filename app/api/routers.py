from app.api.v1 import document
from fastapi import APIRouter

routers = APIRouter()
routers.include_router(document.router)
