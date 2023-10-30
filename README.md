<center><h1>Parser HH vacancy</h1></center>

Данный проект представляет собой парсер, которой извлекает информацию о вакансиях и компаниях
с сайта [_hh.ru_](https://hh.ru/) и создает 2 таблицы (<font color="grey">работодатели </font>,<font color="grey">
вакансии</font>) ***postgreSQL***:

| № | <font color="red">employers </font> | <font color="red">vacancies </font> | 
|:-:|:-----------------------------------:|:-----------------------------------:|
| 1 |           **employer_id**           |           **vacancy_id**            |
| 2 |              **title**              |              **title**              |
| 3 |                                     |           **employer_id**           |
| 4 |                                     |           **salary_min**            |
| 5 |                                     |               **url**               |

---
![1.gif](..%2F..%2FDownloads%2F1.gif)
> [!NOTE]
> В **<font color="yellow">companies.json </font>** перечислены работодатели по которым будет осуществляться поиск
> вакансий:

``` json
{
  "Яндекс": 1740,
  "МТС": 3776,
  "Тинькофф": 78638,
  "Мегафон": 3127,
  "СБЕР": 3529,
  "OZON": 2180,
  "ПАО Газпром": 104628,
  "Skyeng": 1122462,
  "Пятёрочка": 1942330,
  "Магнит": 49357
}
```
---
Перед использование программы нужно:<br>

<h3>1. Установить заисимости из файла **<font color="yellow">requirements.txt</font>**<br> </h3>
Воспользоваться командой:  **pip install -r requirements.txt**

<h3>2. Что бы подключиться к базе данных нужно создать **<font color="yellow">database.ini</font>** и заполнить файл ↓:</h3>


```sql
[postgresql]
user=postgres
password=Указать свой пароль!!!
host=localhost
port=5432
dbname=cw5
```
---
