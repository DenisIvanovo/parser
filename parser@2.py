import requests
from bs4 import BeautifulSoup
import csv
import time


url = 'https://www.biopodushka.ru/catalog/1622/'
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}


def get_html(url, params=None):
    # Подключаемся к сайту.
    r = requests.get(url=url, params=params, headers=headers)
    return r


def get_pages(html):
    # В функции узнаем количество страниц нашлось по запросу.
    soup = BeautifulSoup(html, 'lxml')

    pagination = soup.find_all('div', {'class': 'ep'})
    if pagination:
        return int(pagination[-1].text)
    else:
        return 1


def get_content(html):
    # Функция собирает нужную информацию с сайта.
    desired_object = []  # Создаем пустой список для добавленния объектов.

    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', {'class': 'tilec'})
    # Через цикл собираем информация и добавляем с список.
    for div in divs:

        parameters = []  # Создаем список для информации о отваре.
        info = div.find_all('div', {'class': 'ldr1'})
        for i in info:
            # Инфо комплектуем в список.
            parameters.append(i.text.expandtabs(tabsize=0).strip().splitlines())
        try:
            desired_object.append({
                'name': div.find('h2', {'class': 'title1'}).text.strip(),
                'old price': div.find('div', {'class': 'preo chu'}).text.strip(),
                'new price': div.find('div', {'class': 'pre red'}).text.strip(),
                'delivery': div.find('div', {'class': 'ave'}).text.strip(),
                'Brand': parameters[0][2],
                'Material': parameters[1][2],
                'Fabric composition': parameters[2][2],
                'Filler': parameters[3][2],


            })

        except:
            pass
    return desired_object


def csv_file(items, hath):
    # в функцию передаем 2 параметра(1-инфо,2-путь )
    with open(hath, 'w', newline='')as file:  # Создаем файл для записи полученой информации
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Название  ", "Обычная цена", "Наша цена",
                         "Доставка", "Производитель", "Материал",
                         "Состав ткани", "Наполнитель"])  # Название колонок в таблице.

        for d in items:
            try:
                ind = 0
                while ind < len(d)+1:
                    # Записываем даные.
                    writer.writerow([d[ind]['name'], d[ind]['old price'],
                                     d[ind]['new price'], d[ind]['delivery'], d[ind]['Brand'],
                                     d[ind]['Material'], d[ind]['Fabric composition'], d[ind]['Filler']])
                    ind += 1
            except:
                pass


def parsing():
    html = get_html(url)
    if html.status_code == 200:
        print('Подклю чение к сайту прошло успешно.')
        pages = get_pages(html.text)
        cars = []

        for i in range(1, pages+1):
            print('Идет сбор информации странницы {0} из {1}.....'.format(i, pages))
            html = get_html(url, params={"PAGEN_1": i})
            time.sleep(1)  # Чтоббы незабанили ,мы даем 1 секунду заснуть скрипту.
            cars.append(get_content(html.text))

            csv_file(cars, 'info2.csv')

        else:
            print('Сбор данных завершен!!')
    else:
        print('Eroor')


if __name__ == '__main__':
    parsing()