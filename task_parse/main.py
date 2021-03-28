import requests
import json
import validators
from Parser import Parser

def is_valid_url(URL):
    return validators.url(URL)

def get_сonfig():
    try:
        with open("config.json", "r") as read_file:
            return json.load(read_file)
    except:
        return {}

def get_content_area(config, url):
    website = url.split('/')[2]
    websites = config.get("websites", {})
    return websites.get(website, {})

def get_tags(config):
    return config.get("tags", {})


if __name__ == "__main__":

    flag = True    
    config = get_сonfig()
    tags = get_tags(config)
    
    while flag:
        url = input('Введите URL: ')

        #проверяем является ли введеная страка URL. По статусу get-запроса начинаем прасить или выводим код ошибки
        if is_valid_url(url):            
            content_area = get_content_area(config, url)            
            if not content_area:
                print("Пожалуйста добавьте шаблон обработки для сайта в config.json")
            else:
                r = requests.get(url)
                if r.status_code == 200:
                    host = '/'.join(url.split('/')[:3])
                    obj_parser = Parser(text=r.text, content_area=content_area, tags=tags, host=host)
                    obj_parser.parse()
                    print(obj_parser.list_texts)
                else:
                    print(f'Код ошибки {r.status_code}')

        t = input('Желаете продолжить? (y/n) ').lower()
        flag = True if (t == 'y') else False #при либом вводе, кроме 'y', будет выходить из цикла

