#Eventually for mapping DOs verbose ubtunu-ver-ver-ver naming scheme
#with something simpilar
import configparser
import sys
class Data:
	
	def __init__(self):
		try:
			self.config = configparser.ConfigParser('../config.ini')
		except IOError:
			print('config file not found...')
			sys.exit()
		headers = {'Content-Type':'application/json','Authorization':'Bearer {token}'.format(token=config['config']['dotoken'])}