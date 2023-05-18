#!/usr/bin/python3
from datetime import datetime

import os
import json
import requests
import pandas as pd

def main():
	data = requests.get('https://api.regional-table.region-services.aws.a2z.com/index.json', timeout = 10).json()
	js = {'index_by_region': {}, 'index_by_service' : {}}

	cjs = load_cache('AwsServiceRegions.json', jsonstr = True)

	for service in data['prices']:
		region_name = service['attributes']['aws:region']
		service_name = service['attributes']['aws:serviceName']

		if not js['index_by_region'].get(region_name):
			js['index_by_region'][region_name] = []

		js['index_by_region'][region_name].append(service_name)


		if not js['index_by_service'].get(service_name):
			js['index_by_service'][service_name] = []

		js['index_by_service'][service_name].append(region_name)

	df = pd.DataFrame(index=js['index_by_service'].keys(), columns=js['index_by_region'].keys())

	for service in data['prices']:
		region_name = service['attributes']['aws:region']
		service_name = service['attributes']['aws:serviceName']

		df.at[service_name,region_name] = 'YES'

	styler = df.style.applymap(lambda x: "background-color: #23C552" if x == 'YES' else "background-color: #F84F31")

	# Cache our data in json and xlsx
	save_cache('AwsServiceRegions.json', jsonstr = True, data = js)
	save_cache('AwsServiceRegions.xlsx', jsonstr = False, data = styler)

	# Compare new and old data and send changes notification
	send_notification(compare(js, cjs))

def compare(new, old):
	"""Compares old and new json and checks for new or discarded regions and services."""
	default = 'No changes were made.'
	region_added = ', '.join( set(new['index_by_region'].keys()) - set(old['index_by_region'].keys()) )
	region_removed = ', '.join( set(old['index_by_region'].keys()) - set(new['index_by_region'].keys()) )
	service_added = ', '.join( set(new['index_by_service'].keys()) - set(old['index_by_service'].keys()) )
	service_removed = ', '.join( set(old['index_by_service'].keys()) - set(new['index_by_service'].keys()) )

	return (f'*New Regions :*\n{region_added or default}\n\n' 
			f'*Discarded Regions :*\n{region_removed or default}\n\n' 
			f'*New Services :*\n{service_added or default}\n\n' 
			f'*Discarded Services :*\n{service_removed or default}\n\n'
		)


def load_cache(file_name, jsonstr = True):
	"""Load the service regions data either from a json or xlxs."""

	try:
		with open(file_name) as f:
			if jsonstr:
				return json.load(f)

	except (FileNotFoundError, json.decoder.JSONDecodeError):
		return {}

def save_cache(file_name, jsonstr = True, data = None):
	"""Save the service regions data either to a json or xlxs."""
	if jsonstr:
		with open(file_name, 'w+') as f:
			f.write(json.dumps(data))
	else:
		data.to_excel(file_name)

def send_notification(message):
    """Hangouts Chat incoming webhook quickstart."""

    url = os.environ['NOTIFICATION_URL']
    bot_message = {'text': f'Notification {datetime.now()}\n\n{message}'}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    response = requests.post(
        url,
        headers=message_headers,
        json=bot_message,
		timeout=10
    )
    return response


if __name__ == '__main__':
	main()
	#print(json.dumps(js))
