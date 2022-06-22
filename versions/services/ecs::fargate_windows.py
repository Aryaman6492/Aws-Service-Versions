#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc, clean_format
import re

@register
def platform_version():
	title = 'Fargate Windows Platform Version'
	url = 'https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform-windows-fargate.html'
	doc = HtmlDoc(url)
	platform_versions = {'supported' : [], 'deprecated': []}
	for version in doc.find_all(['h2', 'h1', 'h3'], id=re.compile(r'^platform-version-w\d+-\d+')):
		platform_versions['supported'].append(clean_format(version.get_text(strip=True)))

	return {
		'id' : __name__+'.platform_version',
		'title' : title,
		'platform_version' : platform_versions
	}
