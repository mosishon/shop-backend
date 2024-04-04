from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field

class ApplicationCofiguration(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")
    env:str
    timezone:str
    secret_key:str
    jwt_expire_after_minute:int
    str_time_format:str
    static_files_path:str

settings = ApplicationCofiguration()
