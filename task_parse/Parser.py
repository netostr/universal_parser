from bs4 import BeautifulSoup

class Parser():


    def __init__(self, text, content_area, tags, host):
        self._text = text #Содержит ответ сервера  
        self._content_area = content_area #Область полезного конента
        self._tags = tags
        self.list_texts = []
        self._host = host

    def _get_soup(self):
        try:
            self._soup = BeautifulSoup(self._text, 'html.parser')
        except:
            print("Парсер работает только с html-страницами")
            self._soup = BeautifulSoup()

    def _get_area_content(self):
        _place = self._content_area.get('place', {})
        _tag_view = _place.get('tag', '')
        _class_css =  _place.get('class', '')
        self._view = self._soup.find_all(_tag_view, class_=_class_css)

    def _del_ignore_elements(self):
        _ignore_classes = self._content_area.get('ignore_class', {})
        _ignore_ids = self._content_area.get('ignore_id', {})
        for _element in self._view:
            for _ignore_class in _ignore_classes:
                for _find_element in _element.find_all(class_=_ignore_class):
                    _find_element.decompose()
            for _ignore_id in _ignore_ids:
                for _find_element in _element.find_all(id=_ignore_id):
                    _find_element.decompose()


    def _get_href(self):
        for _i in range(len(self._view)):                
            for _element in self._view[_i].find_all(href=True):
                _href = _element.get('href')
                if "http" not in _href:
                    _href = self._host + _href
                try:
                    _element.string += f" [{_href}]"
                except:
                    pass

    def _get_content(self):

        def recursion(_DOM_elements):        
            for _element in _DOM_elements:
                if hasattr(_element,"contents"):
                    if _element.name in self._tags or _element.class_ in self._tags:
                        self._list_contents.append(_element)
                    else:       
                    
                        if _element.find(self._tags) or _element.find(class_=self._tags):                        
                            recursion(_element.contents)
                        else:
                            self._list_contents.append(_element)
                else:
                        self._list_contents.append(_element)

        self._list_contents = []
        recursion(self._view)
                   
    def parse(self):
                
        if self._content_area:
            self._get_soup()
            self._get_area_content()
            self._del_ignore_elements()
            self._get_href()
            self._get_content()
            
            for _element in self._list_contents:
                if hasattr(_element, 'contents'):
                    _text = _element.get_text().strip()
                else:
                    _text = str(_element).strip()
                if _text != '':
                    self.list_texts.append(_text)