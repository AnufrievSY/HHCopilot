import pandas as pd

from src.config import ROOT, log

from src.infra.hh.client import Base as Client
from src.infra.hh import schemas

from src.common.readers import save_csv


def get_areas():
    response = Client().meta.get_areas()
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error getting areas: {response.status_code}\n{response.text}")


def get_dictionary_values(dictionary: str):
    response = Client().meta.get_dictionaries()
    if response.status_code == 200:
        data = response.json()
        return data.get(dictionary)
    else:
        raise Exception(f"Error getting dictionary_values: {response.status_code}\n{response.text}")


def get_search_fields(text: str):
    response = Client().meta.get_search_fields(text=text)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error getting search_fields: {response.status_code}\n{response.text}")


def get_vacancies(
        text: str = "",
        experience: list[schemas.Experience] = None,
        work_format: list[schemas.WorkFormat] = None,
        employment_form: list[schemas.EmploymentForm] = None,
        area: int = None
):
    offset = 0
    total = None
    data = []

    while offset != total:
        response = Client().vacancy.get_vacancy_list(
            offset=offset,
            limit=100,
            text=text,
            experience=experience,
            work_format=work_format,
            employment_form=employment_form,
            area=area,
        )
        if response.status_code == 200:
            answer = response.json()
            total = answer.get("pages")
            offset += 1
            data += answer.get("items")
        else:
            raise Exception(f"Error getting vacancies: {response.status_code}\n{response.text}")
    df = pd.DataFrame(data)

    save_csv(df, ROOT / "temp" / "vacancies.csv")
    return df

def apply_vacancy(user_name: str, vacancy_id: int):
    client = Client(user_name=user_name)

    vacancy_info_response = client.vacancy.get_vacancy_info(vacancy_id=vacancy_id)
    if vacancy_info_response.status_code == 200:
        resume_hash = vacancy_info_response.json()["lastResponseResumeHash"]
    else:
        raise Exception(f"Error getting vacancy_info_response: {vacancy_info_response.status_code}\n"
                        f"{vacancy_info_response.text}")

    apply_vacancy_response = client.vacancy.post_vacancy_accept(vacancy_id=vacancy_id, resume_hash=resume_hash)
    if apply_vacancy_response.status_code == 200:
        log.info(f"[{vacancy_id}] Успешный отклик")
        return True
    if apply_vacancy_response.status_code == 400:
        if apply_vacancy_response.json()['error'] == 'alreadyApplied':
            log.warning(f"[{vacancy_id}] Уже откликнулись")
            return False
        if apply_vacancy_response.json()['error'] == 'letter-required':
            log.warning(f"[{vacancy_id}] Обязательно сопроводительное письмо")
            return False
    raise Exception(f"[{vacancy_id}] Error getting apply_vacancy_response: {apply_vacancy_response.status_code}\n"
                    f"{apply_vacancy_response.text}")