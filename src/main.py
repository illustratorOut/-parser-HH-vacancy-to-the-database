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
exit - Завершить работу\n""")

        if user_input == "1":
            vacancies = db_manager.get_vacancies()
            for vacancy in vacancies:
                print(vacancy)
        if user_input == "2":
            res = db_manager.get_avg_salary()
            res = round(res, 2)
            print(res)
        elif user_input == "exit":
            break


if __name__ == "__main__":
    main()
