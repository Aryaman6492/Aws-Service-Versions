#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc
import re


@register
def instances():
	title = 'ElastiCache for Redis versions'
	url = 'https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-emr-supported-instance-types.html'
	doc = HtmlDoc(url)
	instances = {'current' : [], 'previous': []}
	header = doc.find(id='dp-emr-supported-instance-types')
	table = header.parent.find(class_='table-contents')

	headers = [header.text for header in table.find('thead').find_all('th')]
	for row in table.find('tbody').find_all('tr'):
		row_current = {}
		for i, cell in enumerate(row.find_all('td')):
			unwanted = cell.find(class_='awsdocs-note')
			if unwanted:
				unwanted.decompose()
			if i == 0:
				row_current[headers[i]]  = cell.get_text(strip=True)
			else:
				row_current[headers[i]] = list(map(str.strip, cell.get_text(strip=True).strip('|').split('|')))

		instances['current'].append(row_current)

	return {
		'id' : __name__+'.instances',
		'title' : title,
		'instances' : instances
	}
