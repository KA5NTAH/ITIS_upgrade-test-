"""
Создание базы данных на основе предоставленных логов
В БД одна таблица с колонками:
date TEXT - дата
time TEXT - время
user_ip TEXT - IP адрес пользователя
category TEXT - категория товара
item TEXT - продукт
payed TEXT - оповещение об успешной оплате

Если какой то из запросов не имеет указанной выше категории
то он помечается как 'NO'
"""
import sqlite3
connect = sqlite3.connect('ITIS_upgrade.db')
cursor = connect.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS logs(date TEXT, time TEXT, user_ip TEXT, category TEXT, "
               "item TEXT, payed TEXT)")

FORBIDDEN_WORDS = ["shop_api", "INFO:", "|", "", "https:", "\n", "all_to_the_bottom.com"]
with open("logs.txt", "r") as file:
    for line in file:
        # Первичная обработка разобьем строки по пробелам
        temp_row = line.split(" ")
        # Удалим заведомо лишние
        CurrentRow = []
        for word in temp_row:
            if word not in FORBIDDEN_WORDS:
                CurrentRow.append(word)
        # Будет уместно разбить ссылку на отдельные части
        temp_link = (CurrentRow[-1]).split("/")
        # Опять же удалим из сслыки заведомо лишние части (Поскольку мы работаем только с 1 сайтом
        # его название можно опустить)
        link = []
        for word in temp_link:
            if word not in FORBIDDEN_WORDS:
                link.append(word)
        # Теперь нужно понять какие собственно части ссылки мы имеем чтобы
        # окончательно привести CurrentRow к виду в котором его можно добавить в БД
        # В итоге из ссылки мы должны получить лист заполненный по образцу
        # [категория (category), продукт (item), успешная оплата (payed)]
        # Если какой то из пунктов остуствеут помечаем его как "NO"
        link_len = len(link)
        if link_len == 0:
            final_link = ["NO"] * 3
        elif link_len == 1:
            if "pay?" in link[0] or "cart?" in link[0]:
                final_link = ["NO"] * 3
            elif "success" in link[0]:
                final_link = ["NO", "NO", link[0]]
            else:
                final_link = [link[0], "NO", "NO"]
        elif link_len == 2:
            final_link = link + ["NO"]

        # Приводим current_row к финальному виду данные типа [NTKOP0S4] хранить не будем
        # потому что для ответа на выбранные мной запросы они не пригодятся

        CurrentRow = CurrentRow[:2] + CurrentRow[3:-1] + final_link
        cursor.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", tuple(CurrentRow))
        connect.commit()


