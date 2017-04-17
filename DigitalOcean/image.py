from DigitalOcean.data import Data
import sys
class Image(Data):
	url = 'https://api.digitalocean.com/v2/images'
	def __init__(self):
		super().__init__()

	def get_all_images(self):
		response = super().request_data(Image.url,'get')
		print(response['images'][0])
		if type(response['images'][0]['id']) == int:
			return response
		else:
			print('Images request failed')
			sys.exit()



	def get_dist_images(self):
		response = super().request_data('{url}{suburl}'.format(url=Image.url,suburl='?type=distribution'),'get')
		if type(response['images'][0]['id']) == int:
			return response
		else:
			print('Distribution image request failed')
			sys.exit()

	def get_application_images(self):
		response = super().request_data('{url}{suburl}'.format(url=Image.url,suburl='?type=application'),'get')
		if type(response['images'][0]['id']) == int:
			return response
		else:
			print('Application image request failed')
			sys.exit()

	def get_image_by_id(self,iden):
		response = super().request_data('{url}/{id}'.format(url=Image.url, id=iden), 'get')
		if type(response['image']['id']) == int:
			return response['image']
		else:
			print('Image by id request failed')
			print(response)
			sys.exit()

	def get_all_user_images(self):
		response = super().request_data('{url}{suburl}'.format(url=Image.url,suburl='?private=true'), 'get')
		try:
			#print(response)
			if type(response['images'][0]['id']) == int:
				return response

			else:
				print('User image request failed')
				sys.exit()
		except KeyError:
			print('No user images exist')
			sys.exit()
		except IndexError:
			print('Image does not exist')
			sys.exit()
	
	def get_image_by_name(self, name):
		images = self.get_all_user_images()
		for image in images:
			if image['slug'] == name:
				return get_image_by_id(image['id'])
			else:
				print('No image by that name exists')
				sys.exit()

	def remove_image_by_id(self, iden):
		response = super().request_data('{url}/{suburl}'.format(url=Image.url,suburl=iden),'delete')
		if response == 204:
			print('Image {id} deleted successfully'.format(id=iden))
		else:
			print('Error deleting image')
			sys.exit()

	def remove_image_by_name(self,name):
		iden = self.get_image_by_name(name)
		iden = iden['image']['id']
		response = super().request_data('{url}/{suburl}'.format(url=Image.url,suburl=iden),'delete')
		if response == 204:
			print('Image {id} deleted successfully'.format(id=iden))
		else:
			print('Error deleting image')
			sys.exit()		
