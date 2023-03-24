from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://mongodb:27017/stats"
    KAFKA_BOOTSTRAP_SERVERS: str = 'kafka:9093'
    KAFKA_TOPIC: str = 'statistics'

    class Config:
        env_file = ".env"


settings = Settings()
