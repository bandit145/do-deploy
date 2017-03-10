#!/usr/bin/env python3
import configparser
import argparse
import requests
import sys
import json
parser = argparse.ArgumentParser(description='deploy digital ocean servers')
parser.add_argument('-n','--name',help='Server name', required=True)
parser.add_argument('-os','--operating_system',help='DO image', required=True)
parser.add_argument('-r','--region',help='Server region', required=True)
parser.add_argument('-cf','--cloud_config',help='Cloud config file to use')
parser.add_argument('-pn','--private_networking',help='Private networking (switch)', action='store_true')
parser.add_argument('-s','--slug', help='Unique ram size slug', required=True)
parser.add_argument('-b','--backups', help='Enable backups (switch)',action='store_true')
parser.add_argument('-t','--tags', help='tags in tag,tag format')
parser.parse_args()
config = configparser.ConfigParser()
try:
	config.read('config.ini')

except IOError:
	print('Config file not found')
	sys.exit()

def main():
	#break this and see what error it produces and handle it
	if parser.tags:
		tags = parser.tags.split(',')
	if cloud_config:
		user_data = cloud_config()
		create_droplet(user_data)
	else:
		create_droplet()


def create_droplet(**kwargs):
	headers = {'Content-Type':'application/json','Authorization':config['config']['dotoken']}
	data = {'name':parser.name,'region':parser.region,'size':parser.slug,'image':parser.os}
	if parser.cf:
		data['user_data'] = kwargs['user_data']
	if parser.pn:
		data['private_networking'] = True
	if parser.backups:
		data['backups'] = True
	if parser.tags:
		data['tags'] = kwargs['tags']
	request = requests.post('https://digitalocean.com/v2/droplets',data=data,headers=headers)
	response = json.loads(request.json())
	if len(response.id) >= 1:
		print('Server deployed')
	else:
		print('Server not deployed successfully... Dumping response')
		print(request.text())


#Read cloud config file into var
def cloud_config():
	try:
		with open(config['cloudconfig']+'/'+parser.cloud_config) as file:
			user_data = file.read()
	except IOError:
		print('Could not open cloud config file')
		sys.exit()

main()