from configparser import ConfigParser
import psycopg2
import colorama

from exceptions import ConfigException


class DBManager:
    def __init__(self) -> None:
        self.__config = self.__get_config()

    def __get_config(self) -> dict:
        parser = ConfigParser()
        parser.read('../database.ini')
        config = {}
        if parser.has_section('postgresql'):
            params = parser.items('postgresql')
            for param in params:
                config[param[0]] = param[1]
        else:
            raise ConfigException('Секция postgresql не найдена в database.ini')
        return config

    def __execute(self, query):
        connection = psycopg2.connect(**self.__config)
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(query)
        connection.close()

    def __insertmany(self, query, values):
        connection = psycopg2.connect(**self.__config)
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.executemany(query, values)
        connection.close()

    def __fetchall(self, query):
        connection = psycopg2.connect(**self.__config)

        with connection.cursor() as cursor:
            cursor.execute(query)
            values = cursor.fetchall()
        connection.close()
        return values

    def create_database(self) -> None:
        config = self.__config.copy()
        config['dbname'] = 'postgres'

        connection = psycopg2.connect(**config)
        connection.autocommit = True

        with connection.cursor() as cursor:
            query = f'DROP DATABASE IF EXISTS {self.__config["dbname"]}'
            cursor.execute(query)
            query = f'CREATE DATABASE {self.__config["dbname"]}'
            cursor.execute(query)

        connection.close()
        print(colorama.Fore.GREEN + f"База данных {self.__config['dbname']} создана." \
              + colorama.Fore.RESET)

    def create_table(self) -> None:
        query = """
CREATE TABLE employers (
    employer_id INT PRIMARY KEY,
    title VARCHAR(50)
);    
        """
        self.__execute(query)
        print(colorama.Fore.GREEN + "Таблица employers создана." \
              + colorama.Fore.RESET)

        query = """
CREATE TABLE vacancies (
    vacancy_id INT PRIMARY KEY,
    title VARCHAR(100),
    employer_id INT REFERENCES employers (employer_id),
    salary_min FLOAT,
    url VARCHAR(100)
);
        """
        self.__execute(query)
        print(colorama.Fore.GREEN + "Таблица vacancies создана." \
              + colorama.Fore.RESET)

    def fill_employers(self, values):
        employers = [(values, key) for key, values in values.items()]
        query = f"""
INSERT INTO employers ("employer_id", "title")
VALUES
(%s, %s)
        """
        self.__insertmany(query, employers)

    def fill_vacancies(self, values):
        vacancies = []
        for vacancy in values:
            salary_min = vacancy['salary']['from'] if vacancy['salary'] and vacancy['salary']['from'] is not None else 0
            vacancies.append((
                vacancy['id'],
                vacancy['name'],
                vacancy['employer']['id'],
                salary_min,
                vacancy['alternate_url']
            ))

        query = """
INSERT INTO vacancies ("vacancy_id", "title", "employer_id", "salary_min", "url")
VALUES
(%s, %s, %s, %s, %s)
        """
        self.__insertmany(query, vacancies)

    def get_vacancies(self):
        query = """
SELECT
    vacancies.vacancy_id
    ,vacancies.title
    ,employers.employer_id
    ,employers.title AS employers
    ,vacancies.salary_min
    ,vacancies.url
FROM vacancies
JOIN employers
    USING (employer_id)
        """
        values = self.__fetchall(query)
        return values

    def get_avg_salary(self):
        query = """
SELECT
    AVG(vacancies.salary_min)
FROM vacancies
        """
        values = self.__fetchall(query)[0][0]
        return values
