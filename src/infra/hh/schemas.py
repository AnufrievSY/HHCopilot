from typing import Literal, TypeAlias

Experience: TypeAlias = Literal['noExperience', 'between1And3', 'between3And6', 'moreThan6']
Experience.description = {
    "noExperience": "Нет опыта",
    'between1And3': "От 1 года до 3 лет",
    'between3And6': "От 3 до 6 лет",
    'moreThan6': "Более 6 лет",
}

EmploymentForm: TypeAlias = Literal["FULL", "PART", "PROJECT", "FLY_IN_FLY_OUT"]
EmploymentForm.description = {
    'FULL': 'Полная занятость',
    'PART': 'Частичная занятость',
    'PROJECT': 'Подработка',
    'FLY_IN_FLY_OUT': 'Вахта',
}

WorkFormat: TypeAlias = Literal["ON_SITE", "REMOTE", "HYBRID", "FIELD_WORK"]
WorkFormat.description = {
    'ON_SITE': 'На месте работодателя',
    'REMOTE': 'Удалённо',
    'HYBRID': 'Гибрид',
    'FIELD_WORK': 'Разъездной',
}
