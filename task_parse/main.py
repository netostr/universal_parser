import requests
import json
import validators
from Parser import Parser
from Formatter import Formatter

#Функция валидации URL
def is_valid_url(URL):
    return validators.url(URL)

#Функция чтения config.json
def get_сonfig():
    try:
        with open("config.json", "r") as read_file:
            return json.load(read_file)
    except:
        return {}

#Функция получения данных из словаря
def get_param(dict_, param, default_):
    return dict_.get(param, default_)

if __name__ == "__main__":

    flag = True    
    config = get_сonfig()

    #Список тегов и классов для разделения на абзацы
    tags_and_classes = get_param(config, 'tags_and_classes', {})
    
    #Директория записи файла
    cur_dir = get_param(config, 'cur_dir', '')

    #Ширина строк в файле
    line_width = get_param(config, 'line_width', 80)

    #Словарь вебсайтов с шаблонами обработки страниц
    website = get_param(config, 'websites', {})
    
    while flag:
        url = input('Введите URL: ')

        #Проверяем является ли введеная страка URL.
        if is_valid_url(url):
            
            #Шаблоны обработки страниц
            content_area = get_param(website, url.split('/')[2], {})
            
            #Проверка на наличие шаблонов
            if not content_area:
                print("Пожалуйста добавьте шаблон обработки для сайта в config.json")
            else:
                r = requests.get(url)

                #По статусу get-запроса начинаем прасить и форматировать
                #или выводим код ошибки
                if r.status_code == 200:
                    host = '/'.join(url.split('/')[:3])
                    obj_parser = Parser(text=r.text, 
                                        content_area=content_area, 
                                        tags_and_classes=tags_and_classes, 
                                        host=host)
                    obj_parser.parse()
                    obj_formatter = Formatter(list_texts=obj_parser.list_texts, 
                                              url=url, 
                                              line_width=line_width, 
                                              cur_dir=cur_dir)
                    obj_formatter.formate()
                else:
                    print(f'Код ошибки {r.status_code}')
        else:
            print("Неверный URL-адрес")

        t = input('Желаете продолжить? (y/n) ').lower()
        flag = True if (t == 'y') else False #при либом вводе, кроме 'y', будет выходить из цикла

