import requests
from src.config import ROOT, log
from src.common.readers import read_json
from src.infra.hh import schemas

BASE_URL = "https://ekaterinburg.hh.ru"


class Base:
    _session: requests.Session
    _cookies: dict
    _headers: dict

    def __init__(self, user_name: str = None):
        self.user_name = user_name
        self._make_session()
        self.meta = Meta(session=self._session, cookies=self._cookies, headers=self._headers)
        self.vacancy = Vacancy(session=self._session, cookies=self._cookies, headers=self._headers)

    def _make_session(self):
        if self.user_name is None:
            self.user_name = "default"
            self._cookies = {}
            self._session = requests.Session()
            self._headers = {}
            return

        self._cookies = read_json(ROOT / 'data' / 'cookies' / f"{self.user_name}.json")

        if not self._cookies.get('_xsrf'):
            raise ValueError("X-XSRFTOKEN not found in Cookies")

        self._session = requests.Session()
        self._session.cookies.update(self._cookies)

        self._headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-XSRFTOKEN": self._cookies.get('_xsrf'),
            "Origin": BASE_URL,
        }


class Meta:
    _session: requests.Session
    _cookies: dict
    _headers: dict

    def __init__(self, session, cookies, headers):
        self._session = session
        self._cookies = cookies
        self._headers = headers

    @staticmethod
    def get_dictionaries() -> requests.Response:
        return requests.get(url='https://api.hh.ru/dictionaries')

    @staticmethod
    def get_areas() -> requests.Response:
        return requests.get(url='https://api.hh.ru/areas')

    @staticmethod
    def get_search_fields(text: str) -> requests.Response:
        return requests.get(url='https://api.hh.ru/suggests/vacancy_search_keyword', params={'text': text})


class Vacancy:
    _session: requests.Session
    _cookies: dict
    _headers: dict

    def __init__(self, session, cookies, headers):
        self._session = session
        self._cookies = cookies
        self._headers = headers

    @staticmethod
    def get_vacancy_list(offset: int = 0, limit: int = 1, text: str = "",
                         experience: list[schemas.Experience] = None,
                         work_format: list[schemas.WorkFormat] = None,
                         employment_form: list[schemas.EmploymentForm] = None,
                         area: int = None
                         ) -> requests.Response:
        if limit > 100:
            raise ValueError("per_page must be less than or equal to 100")
        return requests.get(
            url='https://api.hh.ru/vacancies',
            params={
                "page": offset,
                "per_page": limit,
                "text": text,
                "search_field": None,
                "experience": experience,
                "area": area,
                "metro": None,
                "professional_role": None,
                "industry": None,
                "employer_id": None,
                "currency": None,
                "salary": None,
                "label": None,
                "only_with_salary": None,
                "period": None,
                "date_from": None,
                "date_to": None,
                "top_lat": None,
                "bottom_lat": None,
                "left_lng": None,
                "right_lng": None,
                "order_by": None,
                "sort_point_lat": None,
                "sort_point_lng": None,
                "clusters": None,
                "describe_arguments": None,
                "no_magic": None,
                "premium": None,
                "responses_count_enabled": None,
                "accept_temporary": None,
                "employment_form": employment_form,
                "work_schedule_by_days": None,
                "working_hours": None,
                "work_format": work_format,
                "excluded_text": None,
                "education": None,
                "driver_license_types": None,
                "host": "hh.ru",
                "locale": "RU",
            }
        )

    def get_vacancy_info(self, vacancy_id: str) -> requests.Response:
        if not self._cookies.get('_xsrf'):
            raise ValueError("X-XSRFTOKEN not found in Cookies")

        headers = self._headers
        headers["referer"] = f"{BASE_URL}/vacancy/{vacancy_id}"

        return self._session.get(
            url=f"{BASE_URL}/applicant/vacancy_response/popup",
            headers=self._headers,
            params={
                "vacancyId": str(vacancy_id),
                "isTest": "no",
                "withoutTest": "no",
                "lux": "true",
                "alreadyApplied": "false",
                "_xsrf": self._cookies['_xsrf']
            })

    def post_vacancy_accept(self, vacancy_id: str, resume_hash: str) -> requests.Response:
        if not self._cookies.get('_xsrf'):
            raise ValueError("X-XSRFTOKEN not found in Cookies")

        headers = self._headers
        headers["referer"] = f"{BASE_URL}/vacancy/{vacancy_id}"

        return self._session.post(
            url=f"{BASE_URL}/applicant/vacancy_response/popup",
            headers=self._headers,
            data={
                "_xsrf": self._cookies['_xsrf'],
                "vacancy_id": str(vacancy_id),
                "resume_hash": resume_hash,
                "ignore_postponed": "true",
                "incomplete": "false",
                "mark_applicant_visible_in_vacancy_country": "false",
                "country_ids": "[]",
                "letter": "",
                "lux": "true",
                "withoutTest": "no",
                "hhtmFromLabel": "",
                "hhtmSourceLabel": "",
            })
