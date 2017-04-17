#Eventually for mapping DOs verbose ubtunu-ver-ver-ver naming scheme
#with something simpilar
import configparser
import sys
import requests
import json
class Data:

	def __init__(self):
		try:
			self.config = configparser.ConfigParser()
			self.config.read('config.ini')
		except IOError:
			print('config file not found...')
			sys.exit()
		#print(self.config.sections())
		self.headers = {'Content-Type':'application/json','Authorization':'Bearer {token}'.format(token=self.config['config']['dotoken'])}

	def request_data(self, url, requesttype,**kwargs):
		try:
			if requesttype == 'get':
				response = requests.get(url=url, headers=self.headers)
				return response.json()

			elif requesttype == 'post':
				response = requests.post(url=url, headers=self.headers, data=json.dumps(kwargs['data']))
				return response.json()

			elif requesttype == 'delete':
				response = requests.delete(url=url, headers=self.headers)
				return response.status_code
			
			else:
				return "Error"
		except KeyError:
			return "No Data for post"	
