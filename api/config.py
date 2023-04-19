from pydantic import BaseSettings


class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name: str
    database_url: str
    database_master_password: str
    vite_secret_key: str
    optimisemedia_api_key: str
    optimisemedia_contact_id: str

    class Config:
        env_file = ".env"


settings = Settings()
