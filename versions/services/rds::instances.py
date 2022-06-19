#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc
import re


@register
def classes():
	title = 'RDS Instances latest generation of instance classes'
	url = 'https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html'
	doc = HtmlDoc(url)
	classes = {'current' : [], 'previous': [], 'recommended_upgrade' : {}}
	header = doc.find(id="rds-db-instance-classes-engine-support")
	table = header.find_next_sibling(class_='table-container')

	headers = [header.text for header in table.find('thead').find_all('th')]
	for row in table.find('tbody').find_all('tr'):
		for i, cell in enumerate(row.find_all('td')):
			unwanted = cell.find(class_='awsdocs-note')
			if unwanted:
				unwanted.decompose()
			if i == 0:
				classes['current'].append(cell.get_text(strip=True))


	url = 'https://aws.amazon.com/rds/previous-generation/'
	doc = HtmlDoc(url)

	section = doc.find(id ='Upgrade_paths').parent
	classes['recommended_upgrade'] = [_.get_text(strip=True) 
		for _ in section.find_all('a', class_='lb-accordion-trigger')]

	return {
		'id' : __name__+'.classes',
		'title' : title,
		'classes' : classes
	}
