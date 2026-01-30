from src.config import log
from src.infra.hh import operations, exceptions
import tqdm

LETTER = """Здравствуйте.

Я Python-разработчик с опытом 4+ лет в автоматизации бизнес-процессов, разработке внутренних сервисов и интеграциях с внешними API. Работал с маркетплейсами, аналитикой, обработкой данных и учетными системами, участвовал в архитектурных решениях и руководстве командой.

Быстро вникаю в задачи, довожу решения до продакшена и ориентирован на практический результат.

Буду рад обсудить вакансию.

GitHub: https://github.com/AnufrievSY"""

USERS_FILTER = [
    # {
    #     'user_name': 'SergeyAY',
    #     'variants': [
    #         {
    #             "resume_hash": "c87adc85ff0bf69c2f0039ed1f57337a6c6353",  # python-developer
    #             "letter": LETTER,
    #             "filters": {
    #                 "text": 'Python',
    #                 "area": 3,
    #             }},
    #         {
    #             "resume_hash": "c87adc85ff0bf69c2f0039ed1f57337a6c6353",  # python-developer
    #             "letter": LETTER,
    #             "filters": {
    #                 "text": 'Python',
    #                 "work_format": ["REMOTE"],
    #             }},
    #         {
    #             "resume_hash": "c87adc85ff0bf69c2f0039ed1f57337a6c6353",  # python-developer
    #             "letter": LETTER,
    #             "filters": {
    #                 "text": 'team lead',
    #                 "area": 3,
    #             }},
    #         {
    #             "resume_hash": "c87adc85ff0bf69c2f0039ed1f57337a6c6353",  # python-developer
    #             "letter": LETTER,
    #             "filters": {
    #                 "text": 'team lead',
    #                 "work_format": ["REMOTE"],
    #             }},
    #     ]
    # },
    {
        'user_name': 'ekay_ru',
        'variants': [
            # {
            #     "resume_hash": "1d4d481dff0b2220c30039ed1f5633414c6f7a",  # операционный директор
            #     "letter": "",
            #     "filters": {
            #         "text": 'маркетплейс',
            #         "area": 3,
            #     }},
            {
                "resume_hash": "25437198ff0fa11cb60039ed1f4e5556476266",  # специалист по работе с маркетплейсами
                "letter": "",
                "filters": {
                    "text": 'маркетплейс',
                    "area": 3,
                }},

        ]
    }
]


def extract(filters: dict) -> list[int]:
    df = operations.get_vacancies(**filters)
    return df['id'].unique().tolist()


def apply(user_name: str, resume_hash: str, ids: list[int], letter: str = ""):
    for _id in tqdm.tqdm(ids, total=len(ids)):
        try:
            operations.apply_vacancy(user_name=user_name, vacancy_id=_id, resume_hash=resume_hash, letter=letter)
        except Exception as e:
            if e is exceptions.LimitExceeded:
                log.info(f'Достигнут лимит отправки резюме')
                break
            log.error(e, exc_info=True)


def run():
    for user in USERS_FILTER:
        log.info(f'RUN APPLY for {user["user_name"]}')
        for v in user['variants']:
            log.info(f'FILTERS: {v['filters']}')
            ids = extract(v['filters'])
            apply(user_name=user['user_name'], resume_hash=v['resume_hash'], ids=ids, letter=v['letter'])


if __name__ == '__main__':
    run()
