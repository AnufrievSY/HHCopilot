from src.config import log, ROOT
from src.common.readers import yaml_read
from src.core.shemas import User
from src.infra.hh import operations, exceptions
import tqdm

def load_filters():
    fp = ROOT / 'data' / 'users.yaml'
    data = yaml_read(fp)
    return [User(**d) for d in data]


def extract(**kwargs) -> list[int]:
    df = operations.get_vacancies(**kwargs)
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
    users_filters = load_filters()
    for user in users_filters:
        log.info(f'RUN APPLY for {user.user_name}')
        for v in user.variants:
            log.info(f'FILTERS: {v.resume.name}')
            ids = extract(**v.filters)
            apply(user_name=user.user_name, resume_hash=v.resume.hash, ids=ids, letter=v.letter)


if __name__ == '__main__':
    run()
