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
				request = requests.get(url=url, headers=self.headers)
				return request.json()

			elif requesttype == 'post':
				request = requests.post(url=url, headers=self.headers, data=json.dumps(kwargs['data']))
				return request.json()

			elif request == 'delete':
				request = requests.delete(url=url, headers=self.headers)
				return request.response_code
			
			else:
				return "Error"
		except KeyError:
			return "No Data for post"	
