from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config.database import engine, Base
from app.routers import auth, universities, majors, guides, collections, cases
from app.routers.statistics import router as statistics_router
from app.config.settings import get_settings
import os

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="xmum留学平台API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router)
app.include_router(universities.router)
app.include_router(majors.router)
app.include_router(guides.router)
app.include_router(collections.router)
app.include_router(cases.router)
app.include_router(statistics_router)

@app.get("/")
def root():
    return {
        "message": "欢迎使用xmum留学平台API",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
