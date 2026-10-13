from pydantic import computed_field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: SecretStr

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        # Usando URL.create para montar a string de forma segura e limpa
        return URL.create(
            drivername="mysql+pymysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD.get_secret_value(),  # Resolve o problema do "**********"
            host="db",
            port=3306,
            database=self.MYSQL_DATABASE,
        ).render_as_string(hide_password=False)  # Retorna a string pronta para o engine do SQLAlchemy
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )



settings = Settings()
