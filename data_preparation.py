"""
Подготовка данных для создания следующих отчетов
1) Какая нагрузка (число запросов) на сайт за астрономический час?
2) В какое время суток чаще всего просматривают определенную категорию товаров?
3) Какое количество пользователей совершали повторные покупки за определенный период?
"""
import sqlite3


def date_list():
    # Небольшая вспомогательная функция которая возвращает список дат с 2018-08-01 - 2018-08-14
    dates = []
    YYYY_MM = "2018-08-"
    for day in range(1, 15, 1):
        day = str(day)
        if len(day) == 1:
            dates.append(YYYY_MM + "0" + day)
        else:
            dates.append(YYYY_MM + day)
    return dates


def prepare_data_for_first_request(dates):
    """
    Подгтовка данных для первого отчета
    Какая нагрузка (число запросов) на сайт за астрономический час?
    В веб приложении можно будет посмотреть граф который показывает нагрузку на сайт
    в любой из дней
    :return:
    """
    connect = sqlite3.connect("ITIS_upgrade.db")
    cursor = connect.cursor()
    first_result = []

    for current_date in dates:
        # Выбираем из базы данных все запросы которые были совершенны в текущий день
        current_load = [0 for i in range(24)]
        cursor.execute("SELECT * FROM logs WHERE date= ?", (current_date,))
        fetched_rows = cursor.fetchall()
        for log in fetched_rows:
            # Лист с данными для текущей даты (current_load) будет выглядеть так
            # что индексу i соответствует количество запросов во время с [i:00:00 - (i + 1):00:00)
            hour = int((log[1])[:2])
            current_load[hour] += 1
        first_result.append(current_load)
    return first_result


def list_of_categories():
    # Небольшая вспомогательная функция которая возвращает список категорий
    connect = sqlite3.connect("ITIS_upgrade.db")
    cursor = connect.cursor()
    # Для начала составим список категорий
    categories = []
    cursor.execute("SELECT * FROM logs")
    fetched_rows = cursor.fetchall()
    for log in fetched_rows:
        if log[3] not in categories and log[3] != "NO":
            categories.append(log[3])
    return categories


def prepare_data_for_second_request(categories):
    """
    Подготовка данных для второго отчета
    В какое время суток чаще всего просматривают определенную категорию товаров?
    Будем считать что:
    утро  [6:00 - 12:00)
    день [12:00 - 18:00)
    вечер [18:00 - 00:00)
    ночь [00:00 - 6:00)
    :return:
    """
    connect = sqlite3.connect("ITIS_upgrade.db")
    cursor = connect.cursor()
    second_result = []
    for categ in categories:
        cursor.execute("SELECT * FROM logs WHERE category = ?", (categ,))
        categ_rows = cursor.fetchall()
        categ_popularity = [0 for i in range(4)]
        for log in categ_rows:
            # Теперь осталось только понять к какому времени суток
            # Согласно нашему распределению относится текущий лог
            # Для каждой категории заведем лист вида
            # [КЗ утром, КЗ днем, КЗ вечером, КЗ ночью] (КЗ - количество запросов)
            hour = int((log[1])[:2])
            if hour < 6:
                categ_popularity[3] += 1  # Ночь
            elif hour < 12:
                categ_popularity[0] += 2  # Утро
            elif hour < 18:
                categ_popularity[1] += 2  # День
            else:
                categ_popularity[2] += 1  # Вечер
        second_result.append(categ_popularity)
    return second_result


def prepare_data_for_third_request(dates):
    """
    Подготовка данных для третьего отчета
    Какое количество пользователей совершали повторные покупки за определенный период?
    Подготовим лист в котором для каждого дня обозначи количество таких пользователей

    Пользователь соверштил повторную покупку в день X
    если он совершал покупку в любой день до этого
    :return:
    """
    connect = sqlite3.connect("ITIS_upgrade.db")
    cursor = connect.cursor()
    third_result = [0 for i in range(len(dates))]
    regular_customers = []
    for (i, date) in enumerate(dates):
        cursor.execute("SELECT * FROM logs WHERE date = ?", (date,))
        fetched_rows = cursor.fetchall()
        for log in fetched_rows:
            if "success" in log[5]:
                if log[2] in regular_customers:
                    third_result[i] += 1
                else:
                    regular_customers.append(log[2])
    return third_result
