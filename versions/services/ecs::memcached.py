#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc, clean_format
import re

@register
def node_generation():
	title = 'ElastiCache cluster latest node version ( memcached )'
	url = 'https://raw.githubusercontent.com/awsdocs/amazon-elasticache-docs/master/doc_source/memcache/CacheNodes.SupportedTypes.md'
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
				node[category].append(clean_format(sibling.get_text(strip=True)))
			else:
				continue

	return {
		'id' : __name__+'.node_generation',
		'title' : title,
		'node_generation' : node
	}



@register
def engine_versions():
	title = 'ElastiCache for Memcached versions'
	url = 'https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/supported-engine-versions.html'
	doc = HtmlDoc(url)
	engine = {'supported' : [], 'deprecated': []}
	header = doc.find(id='supported-engine-versions-mc')
	section = header.find_next_sibling(id='inline-topiclist')
	for version in section.find_all('li'):
		engine['supported'].append(clean_format(version.get_text(strip=True)))

	return {
		'id' : __name__+'.engine_version',
		'title' : title,
		'engine_version' : engine
	}
