from bs4 import BeautifulSoup
import requests
import markdown

class MarkdownDoc(BeautifulSoup):
	def __init__(self, url):
		self.markdown = requests.get(url).content
		self.raw_html = markdown.markdown(self.markdown)
		super().__init__(self.raw_html, 'html5lib')


class HtmlDoc(BeautifulSoup):
	def __init__(self, url):
		self.raw_html = requests.get(url).content
		super().__init__(self.raw_html, 'html5lib')
