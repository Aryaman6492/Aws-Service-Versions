#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc, clean_format
import re

@register
def platform_version():
	title = 'Fargate Linux Platform Version'
	url = 'https://docs.aws.amazon.com/AmazonECS/latest/userguide/platform-linux-fargate.html'
	doc = HtmlDoc(url)
	platform_versions = {'supported' : [], 'deprecated': []}
	for version in doc.find_all(['h2', 'h1', 'h3'], id=re.compile(r'^platform-version-\d+-\d+')):
		platform_versions['supported'].append(clean_format(version.get_text(strip=True)))
	
	url = 'https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform-versions-retired.html'
	doc = HtmlDoc(url)
	header = doc.find(id='platform-versions-retired')
	table = header.parent.find(class_='table-contents')
	headers = [header.text for header in table.find('thead').find_all('th')]
	platform_versions['deprecated'] = [{headers[i]: clean_format(cell.get_text(strip=True)) for i, cell in enumerate(row.find_all('td'))}
		for row in table.find('tbody').find_all('tr')]

	return {
		'id' : __name__+'.platform_version',
		'title' : title,
		'platform_version' : platform_versions
	}
