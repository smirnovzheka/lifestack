from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.base import Base, engine
import app.models  # noqa: F401 — register all models with Base
from app.routers import projects, routines

app = FastAPI(title="LifeStack API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(projects.router, prefix="/api")
app.include_router(routines.router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
