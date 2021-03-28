from bs4 import BeautifulSoup, Comment

class Parser():


    def __init__(self, text, content_area, tags_and_classes, host):
        self._text = text #Содержит ответ сервера  
        self._content_area = content_area #Область полезного конента
        self._tags_and_classes = tags_and_classes #теги и классы для разделения на абзацы
        self.list_texts = []
        self._host = host
        self._list_contents = []

    def _get_soup(self):
        try:
            self._soup = BeautifulSoup(self._text, 'html.parser')
        except:
            print("Парсер работает только с html-страницами")
            self._soup = BeautifulSoup()

    def _get_area_content(self):
        place = self._content_area.get('place', {})
        tag_view = place.get('tag', '')
        class_css =  place.get('class', '')
        self._view = self._soup.find_all(tag_view, class_=class_css)

    def _del_ignore_elements(self):
        ignore_classes = self._content_area.get('ignore_class', {})
        ignore_ids = self._content_area.get('ignore_id', {})
        for element in self._view:    
            if ignore_classes:
                for find_element in element.find_all(class_=ignore_classes):
                    find_element.decompose()
            if ignore_ids:
                for find_element in element.find_all(id=ignore_ids):
                    find_element.decompose()

    def _del_comments(self):
        for element in self._view:
            for comments in element.find_all(text=
                                             lambda text: 
                                             isinstance(text, Comment)):
                comments.extract()

    def _get_href(self):
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
        for element in self._list_contents:
                if hasattr(element, 'contents'):
                    text = element.get_text().strip()
                else:
                    text = str(element).strip()
                if text != '':
                    self.list_texts.append(text)
                   
    def parse(self):                
        if self._content_area:
            self._get_soup()
            self._get_area_content()
            self._del_ignore_elements()
            self._del_comments()
            self._get_href()
            self._get_paragraph_content()
            self._get_list_texts()