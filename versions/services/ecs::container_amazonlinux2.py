#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc
import re

@register
def agent_version():
	title = 'Fargate Linux Platform Version'
	url = 'https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-versions.html'
	doc = HtmlDoc(url)
	agent_versions = {'supported' : [], 'deprecated': []}

	header = doc.find(id='al2-optimized-ami-agent-versions')
	table = header.find_next_sibling(class_='table-container')
	headers = [header.get_text(strip=True) for header in table.find('thead').find_all('th')]
	agent_versions['supported'] = [{headers[i]: cell.get_text(strip=True).strip() for i, cell in enumerate(row.find_all('td'))}
		for row in table.find('tbody').find_all('tr')]

	section = header.find_next_sibling(class_="awsdocs-note awsdocs-important")
	note = section.find(string = re.compile(r'agent versions (.+) and later have deprecated'))
	if note:
		agent_versions['deprecated'].append(re.search(r'agent versions (\d+\.\d+\.?\d*) and later', str(note)).group(1))

	return {
		'id' : __name__+'.agent_version',
		'title' : title,
		'agent_version' : agent_versions
	}
