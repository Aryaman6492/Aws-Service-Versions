#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc
import re

@register
def instances():
	title = 'EMR Latest generation of instances'
	url = 'https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-supported-instance-types.html'
	doc = HtmlDoc(url)
	instances = {'current' : [], 'previous': [], 'recommended_upgrade' : {}}
	table = doc.find(class_='table-contents')
	headers = [header.text for header in table.find('thead').find_all('th')]
	for row in table.find('tbody').find_all('tr'):
		row_previous = {}
		row_current = {}
		for i, cell in enumerate(row.find_all('td')):
			unwanted = cell.find(class_='awsdocs-note')
			if unwanted:
				unwanted.decompose()
			if i == 0:
				row_previous[headers[i]] = cell.get_text(strip=True)
				row_current[headers[i]]  = cell.get_text(strip=True)
			else:
				row_previous[headers[i]] = [_.extract().get_text(strip=True) 
						for _ in cell.find_all(class_="replaceable")]

				row_current[headers[i]] = list(map(str.strip, cell.get_text(strip=True).strip('|').split('|')))

		instances['previous'].append(row_previous)
		instances['current'].append(row_current)

	url = 'https://aws.amazon.com/ec2/previous-generation/'
	doc = HtmlDoc(url)

	section = doc.find(id ='Upgrade_paths').parent
	instances['recommended_upgrade'] = [_.get_text(strip=True) 
		for _ in section.find_all('a', class_='lb-accordion-trigger')]

	return {
		'id' : __name__+'.versions',
		'title' : title,
		'instances' : instances
	}
