from DBManager import DBManager
from src.HH import HeadHunter
from src.exceptions import ConfigException
from utils import get_employers
import psycopg2
import colorama


def main():
    vacancies = []

    # Создание базы данных и таблиц
    try:
        db_manager = DBManager()
        db_manager.create_database()
        db_manager.create_table()
    except FileNotFoundError as e:
        print(colorama.Fore.RED + f"Ошибка чтения файла конфигурации: {e}" \
              + colorama.Fore.RESET)
        exit()
    except ConfigException as e:
        print(colorama.Fore.RED + f"Ошибка чтения файла конфигурации: {e}" \
              + colorama.Fore.RESET)
        exit()
    except psycopg2.Error as e:
        print(colorama.Fore.RED + f"Ошибка чтения файла конфигурации: {e}" \
              + colorama.Fore.RESET)
        exit()

    employers = get_employers()
    db_manager.fill_employers(employers)

    # Парсинг вакансий (HH.ru)
    hh = HeadHunter()
    for employers_id in employers.values():
        vacancies.extend(hh.get_vacancies(employers_id))

    # Заполнение таблицы vacancies
    db_manager.fill_vacancies(vacancies)

    # Вывод результатов запроса
    while True:
        user_input = input("""
1 - Вывести все вакансии
2 - Получить среднию ЗП
3 - Получает список всех компаний и количество вакансий
4 - Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
5 - Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
exit - Завершить работу\n""")

        if user_input == "1":
            vacancies = db_manager.get_vacancies()
            for vacancy in vacancies:
                print(vacancy)

        if user_input == "2":
            res = db_manager.get_avg_salary()
            res = round(res, 2)
            print(colorama.Fore.MAGENTA + str(res) + colorama.Fore.RESET)

        if user_input == "3":
            res = db_manager.get_companies_and_vacancies_count()
            for employer, vacancy in res:
                print(f"{employer} - {colorama.Fore.MAGENTA + str(vacancy) + colorama.Fore.RESET} вакансий")

        if user_input == "4":
            res = db_manager.get_vacancies_with_higher_salary()
            for vacancy_id, title, employer_id, salary_min, url in res:
                print(vacancy_id, title, employer_id,
                      colorama.Fore.MAGENTA + str(salary_min) + colorama.Fore.RESET, url)

        if user_input == "5":
            user_inputs = input("Введите искомое слово: ")
            res = db_manager.get_vacancies_with_keyword(user_inputs)
            if len(res) > 0:
                for vacancy_id, title, employer_id, salary_min, url in res:
                    color_word = title.replace(user_inputs, colorama.Fore.MAGENTA + user_inputs + colorama.Fore.RESET)
                    print(vacancy_id, color_word, employer_id, salary_min, url)
            else:
                print(colorama.Fore.RED + "Совпадений не найдено" + colorama.Fore.RESET)

        elif user_input == "exit":
            break


if __name__ == "__main__":
    main()
