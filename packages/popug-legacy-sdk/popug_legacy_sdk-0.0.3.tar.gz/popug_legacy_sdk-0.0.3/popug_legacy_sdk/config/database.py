from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    username: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    database_name: str = "test"

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.username}:"
            f"{self.password}@{self.host}:"
            f"{self.port}/{self.database_name}"
        )


