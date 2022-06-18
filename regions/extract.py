#!/usr/bin/python3
import json
import requests
import pandas as pd

data = requests.get('https://api.regional-table.region-services.aws.a2z.com/index.json').json()
js = {'index_by_region': {}, 'index_by_service' : {}}


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
print(df)
styler.to_excel('Regional Services.xlsx')

#print(json.dumps(js))
