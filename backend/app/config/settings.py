from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "xmum留学"
    DEBUG: bool = True
    
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/master_application"
    
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 5242880
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
