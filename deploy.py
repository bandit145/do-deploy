#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader, meta
import configparser
import argparse
import requests
import sys
import json
parser = argparse.ArgumentParser(description='deploy digital ocean servers')
parser.add_argument('-n','--name',help='Server name',type=str , required=True)
parser.add_argument('-os','--operating_system',help='DO image',type=str , required=True)
parser.add_argument('-r','--region',help='Server region',type=str , required=True)
parser.add_argument('-cf','--cloud_config',type=str ,help='Cloud config file to use')
parser.add_argument('-pn','--private_networking',help='Private networking (switch)', action='store_true')
parser.add_argument('-s','--slug', help='Unique ram size slug', type=str, required=True)
parser.add_argument('-b','--backups', help='Enable backups (switch)',action='store_true')
parser.add_argument('-t','--tags', help='tags in tag,tag format', type=str)
config = configparser.ConfigParser()
args = parser.parse_args()
try:
	config.read('config.ini')

except IOError:
	print('Config file not found')
	sys.exit()
env = Environment(loader=FileSystemLoader(config['config']['cf_templates']))

def main():
	#break this and see what error it produces and handle it
	if len(args.tags) > 1:
		try:
			args.tags = args.tags.split(',')
		except ValueError:
			print('Tags formatted incorrectly, must use "tag,tag"' )

	if args.cloud_config:
		user_data = cloud_config()
		create_droplet(args, user_data = user_data)
	else:
		create_droplet(args)


def create_droplet(args,**kwargs):
	headers = {'Content-Type':'application/json','Authorization':'Bearer '+config['config']['dotoken']}
	data = {'name':args.name,'region':args.region,'size':args.slug,'image':args.operating_system}
	if args.cloud_config:
		data['user_data'] = kwargs['user_data']
	if args.private_networking:
		data['private_networking'] = True
	if args.backups:
		data['backups'] = True
	if args.tags:
		data['tags'] = args.tags
	request = requests.post('https://api.digitalocean.com/v2/droplets',data=json.dumps(data),headers=headers)
	response = request.json()
	try:
		if type(response['droplet']['id']) == int:
			print('Server deployed')
			#print(kwargs['user_data'])
			print(response['droplet']['name'] +' '+str(response['droplet']['id']))
		else:
			print('Server not deployed successfully... Dumping response')
			print(request.text)
	except KeyError:
		print('Unexpected Response... Dumping response')
		print(request.text)


#Read cloud config file into var
def cloud_config():
	try:	
			data = {}
			source = env.loader.get_source(env, args.cloud_config+'.yml')[0]
			parsed = env.parse(source)
			for var in meta.find_undeclared_variables(parsed):
				data[var] = input('Enter data for {var}: '.format(var=var))
			user_data = env.get_template(args.cloud_config+'.yml')
			user_data = user_data.render(data)
			return user_data

	except IOError:
		print('Could not open cloud config file')
		sys.exit()

main()