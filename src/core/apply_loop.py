from src.config import log
from src.infra.hh import operations

USERS_FILTER = [
    {
        'user_name': 'SergeyAY',
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

def apply(user_name: str, ids: list[int]):
    for _id in ids:
        try:
            operations.apply_vacancy(user_name=user_name, vacancy_id=_id)
        except Exception as e:
            log.error(e, exc_info=True)

def run():
    for user in USERS_FILTER:
        log.info(f'RUN APPLY for {user["user_name"]}')
        for f in user['filters']:
            log.info(f'FILTERS: {f}')
            ids = extract(f)
            apply(user['user_name'], ids)


if __name__ == '__main__':
    run()
