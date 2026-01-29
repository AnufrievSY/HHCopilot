from pydantic import BaseModel, Field

class HHConfig(BaseModel):
    """Конфигурация HH.ru"""
    user_id: int = Field(..., description="ID пользователя в HH.ru"),
    token: str = Field(..., description="Токен для доступа к API HH.ru")

class Config(BaseModel):
    """Конфигурация приложения"""
    hh: HHConfig = Field(..., description="Конфигурация для HH.ru")