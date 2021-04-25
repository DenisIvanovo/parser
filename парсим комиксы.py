""""
Парсим комиксы
"""

import requests
import img2pdf
import os


class Comics:
    def __init__(self):
        self.images_list = []  # Собираем все сктраницы в список для склеивания в один файл.
        self.name_dir = input('название каталога для комикса :')  # Запрашиваем имя папки.
        self.name_file = input('Имя файла формата .pdf :')
        # Проверяе существует папка или нет.
        dir = os.path.exists(f'images/{self.name_dir}')
        if not dir:
            # Если папка нет,создаем её
            os.mkdir(f'images/{self.name_dir}/')

        self.collecting_information()

    def collecting_information(self):
        """
        Собираем все картинки и имя файла записываем с список.
        """
        for i in range(0, 93):
            if i < 10:
                page = f'00{i}'
            else:
                page = f'0{i}'

            image = requests.get(f'http://img.drawnstories.ru/img/Marvel-'
                                 f'Comics/Fantastic-Four/fantastic-four-v6/fantastic-'
                                 f'four-v6-006/{page}.jpg')
            # Проверяем код ответа.
            if image.status_code == 200:  # КОД 200 ВСЕ ХОРОШО.
                response = image.content  # Получаем картинку.
                # Загружаем полученую картинку в папку
                with open(f'images/{self.name_dir}/image{i}.jpg', 'wb')as file:
                    file.write(response)
                print(f'[*] Удачное скачивание {i} страницы комикса.')

                self.images_list.append(f'images/{self.name_dir}/image{i}.jpg')

            else:
                print(image.status_code)

        self.writing_a_file()

    def writing_a_file(self):
        """Записываем информацию в один файл формата PDF"""
        print('#' * 50)

        with open(f'{self.name_file}', 'wb')as f:
            f.write(img2pdf.convert(self.images_list))

        print(f'Комикс скачан и сохранен, файл находиться по пути '
              f'/{self.name_dir}')


if __name__ == '__main__':
    Comics()
