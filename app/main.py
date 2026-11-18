from fastapi import FastAPI
from app.api.routers import routers
from contextlib import asynccontextmanager
from app.core.config import llm_settings

async def lifespan(app: FastAPI):
    # Executing code before application startup
    import os
    os.environ['GOOGLE_API_KEY'] = llm_settings.GOOGLE_API_KEY
    yield

app = FastAPI()

app.include_router(routers)

@app.get("/")
async def root():
    return {"message": "Hello World"}