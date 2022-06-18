#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc
import re

@register
def node_generations():
	title = 'ElastiCache cluster latest node version ( redis )'
	url = 'https://raw.githubusercontent.com/awsdocs/amazon-elasticache-docs/master/doc_source/redis/CacheNodes.SupportedTypes.md'
	doc = MarkdownDoc(url)
	node = {'current' : [], 'previous': []}
	categories = doc.find_all(string = re.compile(r"\+\s*(Current|Previous) generation:", re.IGNORECASE))
	for section in categories:
		if 'current' in section.lower():
			category = 'current'
		else:
			category = 'previous'

		for sibling in section.next_siblings:
			if sibling in categories:
				break
			elif sibling.name == 'code':
				node[category].append(sibling.get_text())
			else:
				continue

	return {
		'code' : __name__+'.node_generations',
		'title' : title,
		'node_version' : node
	}


@register
def engine_versions():
	title = 'ElastiCache for Redis versions'
	url = 'https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/supported-engine-versions.html'
	doc = HtmlDoc(url)
	engine = {'supported' : [], 'deprecated': []}
	header = doc.find(id='supported-engine-versions')
	section = header.find_next_sibling(id='inline-topiclist')
	for version in section.find_all('li'):
		engine['supported'].append(version.get_text())

	url = 'https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/deprecated-engine-versions.html'
	doc = HtmlDoc(url)
	table = doc.find(class_='table-contents')
	#print(table)
	headers = [header.text for header in table.find('thead').find_all('th')]
	engine['deprecated'] = [{headers[i]: cell.get_text(strip=True).strip() for i, cell in enumerate(row.find_all('td'))}
		for row in table.find('tbody').find_all('tr')]

	return {
		'code' : __name__+'.engine_versions',
		'title' : title,
		'engine_version' : engine
	}
