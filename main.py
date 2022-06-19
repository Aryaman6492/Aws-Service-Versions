import versions
import regions

if __name__ == '__main__':
	versions_data = versions.update()
	with open('AwsServiceVersions.json', 'w') as file:
		file.write(versions_data)

	#regions.update('AwsRegionalServices.json')
