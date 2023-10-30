import json


def get_employers(filename='../companies.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        employers = json.load(file)
    return employers
