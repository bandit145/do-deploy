from jinja2 import Environment, FileSystemLoader, meta
from DigitalOcean.data import Data
import sys
class CloudConfig(Data):

	def __init__(self,filename):
		self.filename = filename
		super().__init__()

	def get_cloud_config(self):
		try:
			env = Environment(loader=FileSystemLoader(self.config['config']['cf_templates']))	
			data = {}
			source = env.loader.get_source(env, self.filename)[0]
			parsed = env.parse(source)
			for var in meta.find_undeclared_variables(parsed):
				if args.vars:
					try:
						data[var] = kwargs['cloud_var'][var]
					except KeyError:
						print('All vars for template not entered...')
						print('Printing required variables...')
						print(meta.find_undeclared_variables(parsed))
				else:
					data[var] = input('Enter data for {var}: '.format(var=var))
			user_data = env.get_template(args.cloud_config+'.yml')
			user_data = user_data.render(data)
			#print(user_data)
			return user_data

		except IOError:
			#print(e)
			print('Could not open cloud config file')
			sys.exit()