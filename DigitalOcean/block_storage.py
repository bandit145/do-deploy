#TODO: replace all this repetitve error handling with super function
from DigitalOcean.data import Data
from DigitalOcean.droplet import Droplet
import sys
class BlockStorage(Data):
	url = 'https://api.digitalocean.com/v2/volumes'
	def __init__(self):
		super().__init__()
		self.data = {}

	def set_name(self,name):
		self.data['name'] = name

	def set_size(self, size):
		self.data['size'] = size

	def set_region(self, region):
		self.data['region'] = region

	def set_description(self, description):
		self.data['description'] = description

	def set_attach(self, droplet_id):
		self.data['type'] = 'attach'
		self.data['droplet_id'] = droplet_id

	def set_detach(self, droplet_id):
		self.data['type'] = 'detach'
		self.data['droplet_id'] = droplet_id

	def get_volumes(self):
		try:
			droplet = Droplet('none')
			response = super().request_data(BlockStorage.url+'?region={region}'.format(region=self.data['region']),'get')
			for volume in response['volumes']:
				print('name: {name}'.format(name=volume['name']))
				print('id: {id}'.format(id=volume['id']))
				print('gbs: {gbs}'.format(gbs=volume['size_']))
				print('region: {region}'.format(region=volume['region']['slug']))
				print('attached droplets:')
				for droplet in volume['droplet_ids']:
					info = droplet.get_droplet_by_id(droplet)
					print('droplet_name: {name}'.format(name=info['name']))
					print('droplet_id: {id}'.format(id=info['id']))
				print('----------------')
		except KeyError:
			super().error_handle(response)

	#probably dont need this self.data if I'm doing this in the create section
	def new_volume(self):
		try:
			response = super().request_data(BlockStorage.url,'post',data=self.data)
			if type(response['size_gigabytes']) == int:
				print('Block storage created')
				print('name: '+response['name'])
				print('region: '+response['region'])
			else:
				super().error_handle(response)

		except KeyError:
			super().error_handle(response)

	def get_volume_by_id(self,iden):
		try:
			response = super().request_data(BlockStorage.url+'/{iden}'.format(iden=iden,'get'))
			return response['volume']
		except KeyError:
			super().error_handle(response)

	def get_volume_by_name(self):
		try:
			response = super.request_data(BlockStorage.url+'?name={name}&region={region}'.format(name=self.data['name'],region=self.data['region']),'get')
			return response['volumes']
		except KeyError:
			super().error_handle(response)

	#gets returns all volume snapshots in a regions matching the name
	def get_volume_snapshots_name(self):
		volume = self.get_volume_by_name()
		return self.get_volume_snapshots_id(volume['id'])

	def get_volume_snapshots_id(self,iden):
		try:
			response = super().request_data(BlockStorage.url+'/{iden}/snapshots'.format(iden=iden),'get')
			if response
		except KeyError:
			super().error_handle(response)

	#might have it print that it created it in here
	def create_snapshot_by_id(self,iden,name):
		try:
			response = super().request_data(BlockStorage.url+'/{iden}/snapshots'.format(iden=iden),'post')
			if type(response['snapshot']['id'] == int):
				print('snapshot created')
				print('name: {name}'.format(name=name))
				print('id: {id}'.format(id=str(response['snapshot']['id'])))
				print('regions: ')
				for region in response['snapshot']['regions']:
					print(region)
			else:
				super().error_handle(response)

		except KeyError:
			super().error_handle(response)

	def remove_volume_by_id(self,iden)
		response = super().request_data(BlockStorage.url+'/{iden}'.format(iden=iden),'delete')
		if response == 204:
			print('volume deleted')
			print('id: {id}'.format(id=iden))
		else:
			super().error_handle(response)

	def remove_volume_by_name(self):
		response = super().request_data(BlockStorage.url+'/name={name}&region={region}'.format(name=self.data['name'],region=self.data['region']),'delete')
		if response == 204:
			print('volume deleted')
			print('name: {name}'.format(name=self.data['name']))
			print('region: {region}'.format(region=self.data['region']))
		else:
			super().error_handle(response)

	def attach_volume(self, volume_name):
		try:
			droplet = Droplet('none')
			droplet_info = droplet.get_droplet_by_id(self.data['droplet_id'])
			response = super().request_data(BlockStorage.url+'/{volume_name}/actions'.format(volume_name=volume_name),'post',data=self.data)
			if type(response['action']['status']) == 'completed':
				print('volume attached')
				print('droplet:')
				print('name: {name}'.format(name=droplet_info['name']))
				print('id: {id}'.format(id=str(droplet_info['id'])))
				print('volume:')
				print('id: {id}'.format(id=response['action']['id']))
				print('region: {region}'.format(region=response['action']['region']['slug']))
			else:
				super().error_handle(response)
		except KeyError:
			super().error_handle(response)

	def remove_volume(self, volume_name):
		try:
			droplet = Droplet('none')
			droplet_info = droplet.get_droplet_by_id(self.data['droplet_id'])
			response = super().request_data(BlockStorage.url+'/volumes/actions','post',data=self.data)
			if type(response['action']['status']) == 'completed':
				print('volume attached')
				print('droplet:')
				print('name: {name}'.format(name=droplet_info['name']))
				print('id: {id}'.format(id=str(droplet_info['id'])))
				print('volume:')
				print('id: {id}'.format(id=response['action']['id']))
				print('region: {region}'.format(region=response['action']['region']['slug']))
			else:
				super().error_handle(response)
		except KeyError:
			super().error_handle(response)
