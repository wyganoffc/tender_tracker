from pydantic_settings import BaseSettings


# класс настроек с шаблоном ссылки, ключа и класса подключения к .env
class Settings(BaseSettings):
    """Шаблон настроек"""
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        """Информация для подключения к .env"""
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
