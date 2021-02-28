import requests
from bs4 import BeautifulSoup
import csv
import time


url = 'https://postel-deluxe.ru/shtori/by/ivanovo.html'
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}


def get_html(url, params=None):
    # Подключаемся к сайту.
    r = requests.get(url=url, params=params, headers=headers)
    return r


def get_pages(html):
    # В функции узнаем количество страниц нашлось по запросу.
    soup = BeautifulSoup(html, 'lxml')

    pagination = soup.find_all('a', {'class': 'last'})
    if pagination:
        return int(pagination[-1].text)
    else:
        return 1


def get_content(html):
    # Функция собирает нужную информацию с сайта.
    desired_object = []  # Создаем пустой список для добавленния объектов.

    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('li', {'class': 'item portrait'})
    # Через цикл собираем информация и добавляем с список.
    for div in divs:
        parameters = []  # Создаем список для информации о отваре.
        info = div.find_all('br')
        for i in info:
            # Инфо комплектуем в список.
            parameters.append(i.previous)

        try:
            desired_object.append({
                'name': div.find('h2', {'class': 'product-name'}).text.strip(),
                'meaning_price': div.find('span', {'class': 'price'}).text.strip(),
                'my_price': div.find('p', {'class': 'special-price'}).text.strip(),
                'manufacturer': parameters[0][1:],
                'brand_country': parameters[1][1:],
                'Material': parameters[2][1:],
                'Bracing': parameters[3][1:],
                'Appointment': parameters[4][1:],
                'Curtain_height': parameters[5][1:],
                'Width': parameters[6][1:]


            })

        except:
            pass
    return desired_object


def csv_file(items, hath):
    # в функцию передаем 2 параметра(1-инфо,2-путь )
    with open(hath, 'w', newline='')as file:  # Создаем файл для записи полученой информации
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Название  ", "Обычная цена", "Наша цена",
                         "Производитель", "Страна бренда", "Материал",
                         "Крепление", "Назначение", "Высота шторы",
                         "Ширина шторы"])  # Название колонок в таблице.

        for d in items:
            try:
                ind = 0
                while ind < len(d)+1:
                    # Записываем даные.
                    writer.writerow([d[ind]['name'], d[ind]['meaning_price'],
                                     d[ind]['my_price'], d[ind]['manufacturer'], d[ind]['brand_country'],
                                     d[ind]['Material'], d[ind]['Bracing'], d[ind]['Appointment'],
                                     d[ind]['Curtain_height'], d[ind]['Width']])
                    ind += 1
            except:
                pass


def parsing():
    html = get_html(url)
    if html.status_code == 200:
        print('Подключение к сайту прошло успешно.')
        pages = get_pages(html.text)
        cars = []

        for i in range(1, pages+1):
            print('Идет сбор информации странницы {0} из {1}.....'.format(i, pages))
            html = get_html(url, params={"page": i})
            time.sleep(1)  # Чтоббы незабанили ,мы даем 1 секунду заснуть скрипту.
            cars.append(get_content(html.text))

            csv_file(cars, 'info.csv')

        else:
            print('Сбор данных завершен!!')
    else:
        print('Eroor')


if __name__ == '__main__':
    parsing()