import requests
from src.exceptions import ParsingError


class HeadHunter():
    url = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.params = {
            "per_page": 100,
            "page": None,
            "archived": False,
            "employer_id": None
        }
        self.headers = {
            "User-Agent": "MyImportantApp 1.0"
        }
        self.vacancies = []

    def get_requests(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()["items"]

    def get_vacancies(self, employer_id, pages_count=3):
        vacancies = []  # Очищаем список вакансий
        for page in range(pages_count):
            self.params["page"] = page
            self.params["employer_id"] = employer_id
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_requests()
            except ParsingError as error:
                print(error)
            else:
                vacancies.extend(page_vacancies)
                print(f"Загружено вакансий (employer_id =  {employer_id}): {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break
        return vacancies
