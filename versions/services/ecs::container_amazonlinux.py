#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc, clean_format
import re

def agent_version():
	title = 'Amazon Linux 2 and 2023 AMI container agent versions'
	url = 'https://github.com/aws/amazon-ecs-agent/tags'
	doc = HtmlDoc(url)
	agent_versions = {'supported' : [], 'deprecated': []}

	header = doc.find(id='al2-optimized-ami-agent-versions')
	table = header.find_next_sibling(class_='table-container')
	headers = [header.get_text(strip=True) for header in table.find('thead').find_all('th')]
	for row in table.find('tbody').find_all('tr'):
		for i, cell in enumerate(row.find_all('td')):
			if 'agent version' in headers[i]:
				value = clean_format(cell.get_text(strip=True))
				if value not in agent_versions['supported']:
					agent_versions['supported'].append(value)

	section = header.find_next_sibling(class_="awsdocs-note awsdocs-important")
	note = section.find(string = re.compile(r'agent versions (.+) and later have deprecated'))
	if note:
		agent_versions['deprecated'].append(re.search(r'agent versions (\d+\.\d+\.?\d*) and later', str(note)).group(1))

	return {
		'id' : __name__+'.agent_version',
		'title' : title,
		'agent_version' : agent_versions
	}
