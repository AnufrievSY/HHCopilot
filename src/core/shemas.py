from typing import Any
from pydantic import BaseModel, Field
from src.config import ROOT
from src.common.readers import txt_read

class Resume(BaseModel):
    name: str = Field(..., description="Название резюме")
    hash: str = Field(..., description="Хэш резюме")

class Variant(BaseModel):
    resume: Resume = Field(..., description="Резюме")
    letter: str = Field(..., description="Текст сопроводительного письма")
    filters: dict[str, Any] = Field(..., description="Фильтры для поиска вакансий")

class User:
    user_name: str = Field(..., description="Никнейм пользователя")
    resumes: dict[int, Resume] = Field(..., description="Список резюме пользователя")
    variants: list[Variant] = Field(..., description="Список вариантов для отправки резюме")

    def __init__(self, user_name: str, resumes: dict[int, dict[str, str]], variants: list[dict]):
        self.user_name = user_name
        self.resumes = {i: Resume(**resume) for i, resume in resumes.items()}
        self.variants = [self._get_variant(**variant) for variant in variants]
    def _get_variant(self, resume: int, letter: str, filters: dict[str, str]) -> Variant:
        return Variant(
            resume=self.resumes[resume],
            letter='\n'.join(txt_read( ROOT / "data" / f'{letter}.txt')) if letter else '',
            filters=filters
        )
