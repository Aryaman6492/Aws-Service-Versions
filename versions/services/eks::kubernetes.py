#!/usr/bin/python3
from versions import register
from versions.parser import MarkdownDoc, HtmlDoc
import re

@register
def versions():
	title = 'Amazon EKS Kubernetes versions'
	url = 'https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html'
	doc = HtmlDoc(url)
	versions = {'supported' : [], 'deprecated': []}
	header = doc.find(id='available-versions')
	section = header.find_next_sibling('div',class_='itemizedlist')
	for version in section.find_all('li'):
		versions['supported'].append(version.get_text(strip=True))

	return {
		'code' : __name__+'.versions',
		'title' : title,
		'version' : versions
	}

