#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc, clean_format
import re

@register
def runtime():
	title = 'Lambda latest runtime for all environments'
	url = 'https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html'
	doc = HtmlDoc(url)
	runtimes = {'supported' : [], 'deprecated': []}
	header = doc.find(id="runtime-support-policy")
	table = header.find_next_sibling(class_='table-container')

	headers = [header.text for header in table.find('thead').find_all('th')][1:] # Cause extra table head
	runtimes['deprecated'] = [{headers[i]: clean_format(cell.get_text(strip=True)) for i, cell in enumerate(row.find_all('td'))}
		for row in table.find('tbody').find_all('tr')]

	return {
		'id' : __name__+'.runtime',
		'title' : title,
		'runtime' : runtimes
	}
