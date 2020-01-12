"""
Создание веб приложения которое визуализирует следующие отчеты:
1) Какая нагрузка (число запросов) на сайт за астрономический час?
2) В какое время суток чаще всего просматривают определенную категорию товаров?
3) Какое количество пользователей совершали повторные покупки за определенный период?
Веб приложение по адресу http://127.0.0.1:8050/
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import data_preparation

# Подготовка данных

# общие данные
dates = data_preparation.date_list()
categories = data_preparation.list_of_categories()
time_list = [i for i in range(24)]

# данные для первого графа
first_graph = data_preparation.prepare_data_for_first_request(dates)
first_marks_slider = {}
for i in range(len(dates)):
    first_marks_slider[i] = dates[i]

# данные для второго графа
second_graph = data_preparation.prepare_data_for_second_request(categories)
second_marks_slider = {}
for i in range(len(categories)):
    second_marks_slider[i] = categories[i]

# данные для третьего грфафа
third_graph = data_preparation.prepare_data_for_third_request(dates)

data2 = [0 for i in range(3)]

app = dash.Dash()

app.layout = html.Div([
    html.H1("ITIS Upgrade"),
    html.H2("Приложение создал студент ЮУрГУ Шилков Андрей"),
    html.H3("Используйте слайдер для отображения интересующей вас информации"),
    dcc.Graph(
        id="first_request_graph"
    ),

    dcc.Slider(
        id="fist_request_slider",
        min=0,
        max=len(dates) - 1,
        marks=first_marks_slider,
        value=0,
    ),

    dcc.Graph(
        id="second_request_graph"
    ),

    dcc.Slider(
        id="second_request_slider",
        min=0,
        max=len(categories) - 1,
        marks=second_marks_slider,
        value=0
    ),

    dcc.Graph(
        id="third_request_slider",
        figure={
            'data': [
                {'x': dates, 'y': third_graph, 'type':'bar', 'name': 'test'}
            ],
            'layout': {
                'title': 'Количество пользователей совершивших повторные покупки в каждый из дней'
            }
        },
    ),

])


@app.callback(
    dash.dependencies.Output('first_request_graph', 'figure'),
    [dash.dependencies.Input('fist_request_slider', 'value')])
def update_first_request(value):
    return {
        'data': [
            {'x': time_list, 'y': first_graph[value], 'type': 'bar', 'name': 'Количество запросов'}
        ],
        'layout': {
            'title': 'Количество запросов за час'
        }
    }


@app.callback(
    dash.dependencies.Output('second_request_graph', 'figure'),
    [dash.dependencies.Input('second_request_slider', 'value')])
def update_second_graph(value):
    return {
        'data': [
            {'x': ["Утро (6:00 - 12:00)", "День (12:00 - 18:00)", "Вечер (18:00 - 24:00)", "Ночь (00:00 - 6:00)"],
             'y': second_graph[value], 'type':'bar', 'name': 'test'}
        ],
        'layout': {
            'title': 'Популярность категори в зависимости от времени'
        }
    }


app.run_server(debug=True, host='0.0.0.0')

# Веб приложение по адресу http://127.0.0.1:8050/
