from pydantic_settings import BaseSettings, SettingsConfigDict
import redis


class Settings(BaseSettings):
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: int
    
    model_config = SettingsConfigDict(env_file='.env')
    

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

settings = Settings()