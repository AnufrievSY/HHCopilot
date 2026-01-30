from src.config import log
from src.infra.hh import operations

LETTER = """Здравствуйте.

Я Python-разработчик с опытом 4+ лет в автоматизации бизнес-процессов, разработке внутренних сервисов и интеграциях с внешними API. Работал с маркетплейсами, аналитикой, обработкой данных и учетными системами, участвовал в архитектурных решениях и руководстве командой.

Быстро вникаю в задачи, довожу решения до продакшена и ориентирован на практический результат.

Буду рад обсудить вакансию.

GitHub: https://github.com/AnufrievSY"""

USERS_FILTER = [
    {
        'user_name': 'SergeyAY',
        "resume_hash": "c87adc85ff0bf69c2f0039ed1f57337a6c6353",
        "letter": LETTER,
        'filters': [
            {
                "text": 'Python',
                "area": 3
            },
            {
                "text": 'Python',
                "work_format": ["REMOTE"],
                "area": 3
            },
        ]
    }
]

def extract(filters: dict) -> list[int]:
    df = operations.get_vacancies(**filters)
    return df['id'].unique().tolist()

def apply(user_name: str, resume_hash: str, ids: list[int], letter: str = ""):
    for _id in ids:
        try:
            operations.apply_vacancy(user_name=user_name, vacancy_id=_id, resume_hash=resume_hash, letter=letter)
        except Exception as e:
            log.error(e, exc_info=True)

def run():
    for user in USERS_FILTER:
        log.info(f'RUN APPLY for {user["user_name"]}')
        for f in user['filters']:
            log.info(f'FILTERS: {f}')
            ids = extract(f)
            apply(user_name=user['user_name'], resume_hash=user['resume_hash'], ids=ids, letter=user['letter'])


if __name__ == '__main__':
    run()
