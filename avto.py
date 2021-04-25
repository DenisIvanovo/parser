"""
Получаем информацию с сайта  https://auto.ru по определеным параметрам.
Параметры запрашиваем у пользователя методом input()
Полученую информацию в файл формата .csv
Мы показываем пользователю, сколько объявлений было найдено и сколько времени это заняло.
"""

import requests
from bs4 import BeautifulSoup
import time
import csv

# Глобальный переменые.
result = []
cars = 0
lead_time = []


def execution_measurement(func):
    global lead_time
    # Вычисляем время выполнения сбора информации.
    def wrapper(*args):
        start = time.time()
        return_value = func(*args)
        end = time.time()
        lead_time.append(end - start)
        return return_value

    return wrapper


@execution_measurement
def get_pade(base_URL):
    # Выполняем запрос и вычисляем количество страниц.
    quantity = []
    try:
        pages = requests.get(base_URL)
        if pages.status_code == 200:
            s = BeautifulSoup(pages.content, 'lxml')
            page = s.find_all('span', class_='ControlGroup ControlGroup_'
                                             'responsive_no ControlGroup_size_'
                                             's ListingPagination-module__pages')
            if not len(page) == 0:
                for i in page:
                    button = i.find_all('span', class_='Button__text')
                for b in button:
                    quantity.append(b.get_text())  # Добавляем элементы в список.
                # Возвращаем последний элемент списка
                return int(quantity[-1])
            else:
                return 1
        else:
            print(pages.status_code)
            return None
    except requests.exceptions.ConnectionError as error:
        print('Ошибка', error)

@execution_measurement
def get_content(url, param):
    global result, cars
    # Получаем нужную информацию с сайта.
    con = requests.get(url, params=param)
    soup = BeautifulSoup(con.content, 'lxml')
    divs = soup.find_all('div', class_='ListingItem-module__main')

    for d in divs:
        specifications =[]  # Список для выборки характеристики.
        for i in d:
            elem = (i.find_all('div', class_='ListingItemTechSummaryDesktop__cell'))
            for e in elem:
                specifications.append(e.get_text())

        data = {'Марка и модель': d.find('a', class_='Link ListingItemTitle'
                                                     '-module__link').get_text(),
                'Характеристики': specifications[0].strip(),
                'кпп': specifications[1].strip(),
                'Корпус': specifications[2].strip(),
                'Привод': specifications[3].strip(),
                'Цвет': specifications[4].strip(),
                'Цена': d.find('span').text.strip(),
                'Год выпуска': d.find('div', class_='ListingItem-'
                                                    'module__year').get_text().strip(),
                'Пробег': d.find('div', class_='ListingItem-module__kmAge').get_text().strip()
                }
        result.append(data)
        # Подсчет количества объявлений по параметрам
        cars += 1  # Добавляем +1

@execution_measurement
def csv_file(items, hath):

    # в функцию передаем 2 параметра(1-инфо,2-путь )
    with open(hath, 'w', newline='', encoding='utf-8')as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Марка и модель", "Характеристики", "Тип КПП", "Корпус",
                         "Привод", "Цвет", "Цена", "Год выпуска", "Пробег"])

        for d in items:
            try:
                writer.writerow([d['Марка и модель'], d['Характеристики'], d['кпп'],
                                    d['Корпус'], d['Привод'], d['Цвет'],
                                    d['Цена'], d['Год выпуска'], d['Пробег']])
            except:
                pass


if __name__ == '__main__':
    # Запрашиваем парамерты для поиска обьявлений. 
    car_brand = input('car brand :')  # Марка авто.
    car_model = input('car model :')  # Модель авто.
    name_file = input('Введите имя файла "укажите формат .csv" :')
    # Состовляем базовый адрес для запроса.
    pages_names = f'cars/{car_brand}/{car_model}/used/'  # названия страниц
    base_url = 'https://auto.ru/ivanovo/{}'.format(pages_names)
    # Узнаём количество страниц для определенной категории машин.
    pages = get_pade(base_url)
    if not pages == None:
        for page in range(1, pages+1):
            param = {'page': page}
            get_content(base_url, param)
    else:
        print('Страница не существует')
    csv_file(result, f'{name_file}')

    print(f'Сбор информации закончен,мы нашли {cars} объявлений.'
          f'Информация сохранена в файле {name_file}\n'
          f'На запрос количества строниц ушло {lead_time[0]:.3f} секунд\n'
          f'На сбор информации объявлений ушло {lead_time[1]:.3f} секунд\n'
          f'На запись информации в файл ушло {lead_time[2]:.3f} секунд')





