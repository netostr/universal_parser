from bs4 import BeautifulSoup, Comment

class Parser():
    '''Парсер html-страниц по заданному шаблону.'''

    def __init__(self, content, patterns, tags_and_classes, host):
        self._content = content                     #Содержит ответ сервера  
        self._patterns = patterns                   #Шаблоны обработки страниц
        self._tags_and_classes = tags_and_classes   #Список тегов и классов для разделения на абзацы
        self.list_texts = []                        #Список текстов по абзацам
        self._host = host                           #Адрес хоста сайта для дополнения ссылок
        self._list_contents = []                    #Список элементов разделенных по абзацам

    def _get_soup(self):
        '''Метод для получения объекта BeautifulSoup.'''
        try:
            self._soup = BeautifulSoup(self._content, 'html.parser')
        except:
            print("Парсер работает только с html-страницами")
            self._soup = BeautifulSoup()

    def _get_area_content(self):
        '''Метод получения части текста с необходимой информацией.'''
        place = self._patterns.get('place', {})
        tag_view = place.get('tag', '')
        class_css =  place.get('class', '')
        self._view = self._soup.find_all(tag_view, class_=class_css)

    def _del_ignore_elements(self):
        '''Метод удаления ненужных элементов.'''
        ignore_classes = self._patterns.get('ignore_class', {})
        ignore_ids = self._patterns.get('ignore_id', {})
        for element in self._view:    
            if ignore_classes:
                for find_element in element.find_all(class_=ignore_classes):
                    find_element.decompose()
            if ignore_ids:
                for find_element in element.find_all(id=ignore_ids):
                    find_element.decompose()

    def _del_comments(self):
        '''Метод удаления комментариев.'''
        for element in self._view:
            for comments in element.find_all(text=
                                             lambda text: 
                                             isinstance(text, Comment)):
                comments.extract()

    def _get_href(self):
        '''Метод добавления ссылок в текст.'''
        for element in self._view:                
            for element_href in element.find_all(href=True):
                href = element_href.get('href')
                if "http" not in href:
                    href = self._host + href
                try:
                    element_href.string += f" [{href}]"
                except:
                    pass

    def _get_paragraph_content(self):
        '''
        Метод разделения на абзацы. Вызывает рекурсионную функцию, 
        которая проходит по элементам DOM-дерева и записывает в список элементы,
        отнесенные к абзацным.
        '''
        def recursion(DOM_elements):        
            for element in DOM_elements:
                if hasattr(element,"contents"):
                    if (element.name in self._tags_and_classes 
                            or element.class_ in self._tags_and_classes):
                        self._list_contents.append(element)
                    else:
                        if (element.find(self._tags_and_classes)
                                or element.find(class_=self._tags_and_classes)):                        
                            recursion(element.children)
                        else:
                            self._list_contents.append(element)
                else:
                        self._list_contents.append(element)

        recursion(self._view)

    def _get_list_texts(self):
        '''Метод получения текста.'''
        for element in self._list_contents:
                if hasattr(element, 'contents'):
                    text = element.get_text().strip()
                else:
                    text = str(element).strip()
                if text != '':
                    self.list_texts.append(text)
                   
    def parse(self): 
        '''Метод парсинга сайтов.'''
        self._get_soup()
        self._get_area_content()
        self._del_ignore_elements()
        self._del_comments()
        self._get_href()
        self._get_paragraph_content()
        self._get_list_texts()