#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc, clean_format
import re


@register
def node_generation():
	title = 'Redshift clusters latest generation of nodes'
	url = 'https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html#working-with-clusters-overview'
	doc = HtmlDoc(url)
	node = {'current' : {}, 'previous': {}, 'recommended_upgrade' : {}}
	table_headers = doc.find_all(id=re.compile(r'rs-(.+)-nodes-table'))

	for header in table_headers:
		table = header.find_next_sibling(class_="table-container")
		headers = [header.text for header in table.find('thead').find_all('th')]
		for row in table.find('tbody').find_all('tr'):
			cells = row.find_all('td')
			if headers[0] not in node['current']:
				node['current'][headers[0]] = []
			node['current'][headers[0]].append(clean_format(cells[0].get_text(strip=True)))


	header = doc.find(id='rs-upgrading-to-ra3')
	table = header.find_next_sibling(class_="table-container")
	
	headers = [header.text for header in table.find('thead').find_all('th')]
	for row in table.find('tbody').find_all('tr'):
		cells = row.find_all('td')
		old = cells[0].get_text(strip=True)
		new = cells[2].get_text(strip=True)
		if old not in node['recommended_upgrade']:
			node['recommended_upgrade'][old] = []
		node['recommended_upgrade'][old].append({
			headers[1] : clean_format(cells[1].get_text(strip=True)),
			headers[2] : clean_format(new),
			headers[3] : clean_format(cells[3].get_text(strip=True))
		})

	return {
		'id' : __name__+'.node_generation',
		'title' : title,
		'node_generation' : node,
	}
