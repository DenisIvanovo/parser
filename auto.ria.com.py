import requests
from bs4 import BeautifulSoup
import csv
import openpyxl
from openpyxl.styles import Font
import time

"""
В этом модуле мы парсим сайт 'avto.ria.com'.
Получаем информацию по продаже поддержаных автомабилях,
неиспользуем дополнительный параметров.
Информацию выгружаем в файл формата 'csv'

Потом эту информацию можно использовать для анализа.

"""

url = 'https://auto.ria.com/newauto/marka-audi/'
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}


def get_html(url, params=None):
    # Подключаемся к сайту.
    r = requests.get(url=url, params=params, headers=headers)
    return r


def get_pages(html):
    # В функции узнаем количество страниц нашлось по запросу.
    soup = BeautifulSoup(html, 'lxml')

    pagination = soup.find_all('span', {'class': 'page-item mhide'})
    if pagination:
        return int(pagination[-1].text)
    else:
        return 1


def get_content(html):
    # Функция собирает нужную информацию с сайта.
    desired_object = []  # Создаем пустой список для добавленния объектов.

    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', {'class': 'proposition'})

    for div in divs:
        try:
            desired_object.append({
                'title': div.find('h3', {'class': 'proposition_name'}).text,
                'title_': div.find('div', {'class': 'proposition_equip size13 mt-5'}).text,
                'infocarb': div.find_all('span', {'class': 'size13'})[0].text,
                'infocark': div.find_all('span', {'class': 'size13'})[1].text,
                'infocarp': div.find_all('span', {'class': 'size13'})[2].text,
                'remains': div.find('div', {'class': 'proposition_badges'}).text[:11],
                'credit': div.find('span', {'class': 'badge badge--dark'}).text,
                'price': div.find('span', {'class': 'size18'}).text + ' или ' +
                              div.find('span', {'class': 'grey size13'}).text

            })

        except:
            pass

    return desired_object


def csv_file(items,hath):
    # в функцию передаем 2 параметра(1-инфо,2-путь )
    with open(hath, 'w', newline='')as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Марка", "Серия", "Двигатель", "Тип КП", "Трансмиссия"
                            , "Статус", "Кредит", "Цена"])

        for d in items:
            try:
                ind = 0
                while ind < len(d)+1:
                    writer.writerow([d[ind]['title'], d[ind]['title_'], d[ind]['infocarb'],
                                    d[ind]['infocark'], d[ind]['infocarp'], d[ind]['remains'],
                                    d[ind]['credit'], d[ind]['price']])
                    ind+=1
            except:
                pass


def xlsx_file(items,pades):
    # Создаем файл формата xlsx и выгружаем информацию в файл.
    # создаем новый excel-файл
    wb = openpyxl.Workbook()
    # добавляем новый лист
    wb.create_sheet(title='Первый лист3333', index=0)

    # получаем лист, с которым будем работать
    sheet = wb['Первый лист3333']

    font = Font(name='Arial', size=16, italic=True, color='FF0000')
    sheet['A1'].font = font
    sheet.column_dimensions['A'].width = 20
    sheet['A1'] = 'Марка'
    sheet.column_dimensions['B'].width = 40
    sheet['B1'] = 'Серия'
    sheet.column_dimensions['C'].width = 20
    sheet['C1'] = 'Двигатель'
    sheet.column_dimensions['D'].width = 20
    sheet['D1'] = 'Коробка передач'
    sheet.column_dimensions['E'].width = 20
    sheet['E1'] = 'Трансмиссия'
    sheet.column_dimensions['F'].width = 20
    sheet['F1'] = 'Статус'
    sheet.column_dimensions['G'].width = 25
    sheet['G1'] = 'Кредит'
    sheet.column_dimensions['H'].width = 30
    sheet['H1'] = 'Цена в "usd" и грин'

    for d in items:
        try:
            ind = 0
            while ind < len(d) + 1:
                sheet.append([d[ind]['title'], d[ind]['title_'], d[ind]['infocarb'],
                                 d[ind]['infocark'], d[ind]['infocarp'], d[ind]['remains'],
                                 d[ind]['credit'], d[ind]['price']])
                ind += 1
        except:
            pass
    wb.save('example.xlsx')


def parsing():
    html = get_html(url)
    if html.status_code == 200:
        print('Подключение к сайту прошло успешно.')
        pages = get_pages(html.text)
        cars = []

        for i in range(1,pages+1):
            print('Идет сбор информации странницы {0} из {1}.....'.format(i, pages))
            html = get_html(url,params={"page":i})
            time.sleep(1)  # Чтоббы незабанили ,мы даем 1 секунду заснуть скрипту.
            cars.append(get_content(html.text))

            csv_file(cars, 'den.csv')
            xlsx_file(cars, pages)

        else:
            print('Сбор данных завершен!!')
    else:
        print('Eroor')


if __name__ == '__main__':
    parsing()