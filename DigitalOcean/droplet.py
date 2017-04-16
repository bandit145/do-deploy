from DigitalOcean.data import Data
import DigitalOcean.cloud_config
import requests
import json

class Droplet(Data):
	url = 'https://api.digitalocean.com/v2/droplets'
	def __init__(self, name):
		super().__init__()
		self.name = name
		self.data = {'name':name}
	#interfaces for adding things for creating droplets
	def set_size(self, slug):
		self.data['size'] = slug

	def set_image(self, image):
		data['image'] = image

	def set_private_networking(self):
		self.data['private_networking'] = True

	def set_ssh_keys(self,keys):
		self.data['ssh_keys'] = keys

	def set_backups(self):
		self.data['backups'] = True

	def set_ipv6(self):
		self.data['ipv6'] = True

	def set_user_data(self,filename):
		cloud = cloud_config.CloudConfig(filename)
		self.data['user_data'] = cloud.get_cloud_config()

	def set_monitoring(self):
		self.data['monitoring'] = True

	def set_volumes(self, volumes):
		self.data['volumes'] = volumes

	#tags array
	def set_tags(self, tags):
		self.data['tags'] = tags

	def create_droplet(self):
		response = super.request_data(Droplet.url,'post',self.data)
		try:
			if type(response['droplet']['id']) == int:
				print('Server deployed')
				#print(kwargs['user_data'])
				print(response['droplet']['name'] +' '+str(response['droplet']['id']))
				sys.exit()
			else:
				print('Server not deployed successfully... Dumping response')
				print(request.text)
				sys.exit()
		except KeyError:
			print('Unexpected response... Dumping response')
			print(request.text)
			sys.exit()

	def remove_droplet_by_tag(self, tag):
		droplets = get_droplets()
		response = super.request_data(Droplet.url+'?tag_name={tag}'.format(tag=tag),'delete')
		if response == 204:
			print('Droplets of tag: {tag} '.format(tag=tag))
			print('Droplets deleted:')
			for droplet in droplets:
				print('Name: '+droplet['name']+' ID: '+ droplet['id'])
		else:
			print('Deletion not completed...')
			print('Dumping response code...')
			print('Response code: {code}'.format(code=response))
			sys.exit()


	def remove_droplet_by_name(self, name):
		try:
			droplet_id = get_droplet_id(name)
			response = super.request_data(Droplet.url+'/{id}'.format(id=droplet_id),'delete')
			response = requests.json()
			if response == 204:
				print('Machine {machine} deleted'.format())
				sys.exit()
			else:
				print('Deletion not completed...')
				print('Dumping response code...')
				print('Response code: {code}'.format(code=response))
				sys.exit()
		except KeyError:
			print('No machines with that name')
			sys.exit()

	def remove_droplet(self,id)
		response = super.request_data(Droplet.url+'/{id}'.format(id=id),'delete')
		response = requests.json()
		if response == 204:
			print('Machine {machine} deleted'.format())
			sys.exit()
		else:
			print('Deletion not completed...')
			print('Dumping response code...')
			print('Response code: {code}'.format(code=response))
			sys.exit()

	#returns dict of droplets with name:id pairs
	def get_droplet_id(self, name):
		droplets = {}
		response = get_droplets()
		for droplet in response['droplets']:
			droplets[droplet['name']] = droplet['id']
		droplet_id = droplets[name]
		return droplet_id
		
	def get_droplets(self):
		try:
			response = self.request_data(Droplet.url, 'get')
			#print(self.headers)
			return response['droplets']
		except KeyError:
			print('Unexpected response... Dumping response')
			print(request.text)
			sys.exit()	