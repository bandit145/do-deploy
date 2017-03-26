from data import Data
import cloud_config
import requests
import json

class Droplet(Data):
	url = 'https://api.digitalocean.com/v2/droplets'
	def __init__(self, region, name, slug, image, headers):
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
		request = requests.post(url,data=json.dumps(self.data),headers=super.headers)
		response = request.json()
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
		request = requests.delete(url+'?tag_name={tag}'.format(tag=tag))
		if request.response_code == 204:
			print('Droplets of tag: {tag} '.format(tag=tag))
			print('Droplets deleted:')
			for droplet in droplets:
				print('Name: '+droplet['name']+' ID: '+ droplet['id'])
		else:
			print('Deletion not completed...')
			print('Dumping response code...')
			print('Response code: {code}'.format(code=requests.status_code))
			sys.exit()


	def remove_droplet(self, name):
		try:
			droplets = get_droplet_id(name)
			request = requests.delete(url+'/{id}'.format(id=droplets['name']),headers=super.headers)
			response = requests.json()
			if request.status_code == 204:
				print('Machine {machine} deleted'.format())
				sys.exit()
			else:
				print('Deletion not completed...')
				print('Dumping response code...')
				print('Response code: {code}'.format(code=requests.status_code))
				sys.exit()
		except KeyError:
			print('No machines with that name')
			sys.exit()

	#returns dict of droplets with name:id pairs
	def get_droplet_id(self, name):
		droplets = {}
		response = get_droplets()
		for droplet in response['droplets']:
			droplets[droplet['name']] = droplet['id']
		return droplets
		
	def get_droplets(self):
		try:
			request = requests.get(url, headers=super.headers)
			response = request.json()
			return response['droplets']
		except KeyError:
			print('Unexpected response... Dumping response')
			print(request.text)
			sys.exit()	