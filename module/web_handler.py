#define a class represent a webpage
from readability import Document
from bs4 import BeautifulSoup
import requests


class Website:
    url : str
    title : str
    text : str

    def __init__(self, url):
        self.url = url
        response = requests.get(url)    
        doc = Document(response.text)
        doc = doc.summary()
        filtered = doc

        soup = BeautifulSoup(filtered, 'html.parser')
        for irrelevant in soup(["script", "style", "img", "input"]):
            irrelevant.decompose()

        self.title = doc.title()
        self.text = soup.body.get_text(separator = "\n", strip = True)