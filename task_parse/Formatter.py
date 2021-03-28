from urllib.parse import urlparse
import os

class Formatter():
    """Класс для форматироания и сохранения текста."""
    
    def __init__(self, list_texts, url, line_width, cur_dir):
        self._list_texts = list_texts   #Список текстов по абзацам
        self._url = url                 #URL-адрес для формирования названия файла
        self._list_texts_format = []    #Список текстов по абзацам и форматированых по ширине строки
        self._line_width = line_width   #Ширина строк в файле
        self._cur_dir = cur_dir         #Директория записи файлов
        self._dir = cur_dir             #Директори записи файла
        self._file_name = ''            #Название файла с директорией записи

    def _split_by_width(self):
        '''Метод форматирования текста по ширине строки.'''
        for text in self._list_texts:
            counter = 0
            text_format = ''
            for word in text.split():
                counter += len(word)
                if counter >= self._line_width:
                    counter = len(word)
                    text_format = text_format.strip() + '\n'
                text_format += word
                counter += 1
                if counter >= self._line_width:
                    counter = 0
                    text_format += '\n'
                else:           
                    text_format += ' '                    
            self._list_texts_format.append(text_format.strip())

    def _get_dir_and_filename(self):
        '''Метод получения названия файла и директории.'''
        url_parse = urlparse(self._url)
        p = url_parse.path.split('/')
        if p[-1] == '':
            p = p[:-1]
        self._dir = os.path.join(self._cur_dir, url_parse.netloc, *p[:-1]) 
        self._file_name = os.path.join(self._cur_dir, url_parse.netloc, *p)  
        self._file_name = self._file_name.replace('.html', '')
        self._file_name += '.txt'


    def _save_to_file(self):
        '''Метод сохранения текста в файл.'''
        if not os.path.isdir(self._dir):
            os.makedirs(self._dir)
        try:            
            with open(self._file_name, 'w') as f:
                text = '\n\n'.join(self._list_texts_format)
                f.write(text)
        except:
            print('Не удалось создать файл')

    def formate(self):
        '''Метод форматирования и сохранения текста.'''
        self._split_by_width()
        self._get_dir_and_filename()
        self._save_to_file()
