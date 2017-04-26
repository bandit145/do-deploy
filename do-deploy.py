#!/usr/bin/env python3
import DigitalOcean
import argparse
parser = argparse.ArgumentParser(description='deploy digital ocean servers')
#droplet stuff
subparsers = parser.add_subparsers(help='Help to be created...')
parser_image = subparsers.add_parser('image-list', help='List images')
parser_image_delete = subparsers.add_parser('image-delete', help='Delete images')
parser_droplet_create = subparsers.add_parser('droplet-create',help='Create a droplet')
#create
parser_droplet_create.set_defaults(cmd='droplet-create')
parser_droplet_create.add_argument('-n','--name',help='name of a droplet',type=str,required=True)
parser_droplet_create.add_argument('-os','--operating_system',help='DO image',type=str,required=True)
parser_droplet_create.add_argument('-r','--region',help='Server region',type=str , required=True)
parser_droplet_create.add_argument('-cf','--cloud_config',type=str ,help='Cloud config file to use')
parser_droplet_create.add_argument('-pn','--private_networking',help='Private networking (switch)', action='store_true')
parser_droplet_create.add_argument('-s','--slug', help='Unique ram size slug', type=str, required=True)
parser_droplet_create.add_argument('-b','--backups', help='Enable backups (switch)',action='store_true')
parser_droplet_create.add_argument('-t','--tags', help='tags in tag,tag format', type=str)
parser_droplet_create.add_argument('-v','--vars',help='Variables for cloud_init scripts in "var=data,var=data" format',type=str)
parser_droplet_create.add_argument('-m','--monitoring',help='Enables DO monitoring',action='store_true')
#parser_droplet_create.add_argument()
#droplet delete
parser_droplet_delete = subparsers.add_parser('droplet-delete',help='Delete a droplet')
parser_droplet_delete.set_defaults(cmd='droplet-delete')
parser_droplet_delete.add_argument('-n','--name',
		help='name of droplet (This will only delete the first droplet it finds with the matching name)', type=str)
parser_droplet_delete.add_argument('-i','--id',help='Delete droplet by provided id',type=str)
parser_droplet_delete.add_argument('-t','--tag',help='Deletes all droplet with tag',type=str)
#droplet list
parser_droplet_list = subparsers.add_parser('droplet-list',help='List droplets')
parser_droplet_list.set_defaults(cmd='droplet-list')
#images
#only on allowed at a time(Except delete image by name/id)
parser_image.set_defaults(cmd='image-list')
parser_image.add_argument('-a','--all',help='list all images',action='store_true')
parser_image.add_argument('-ap','--app',help='list application images',action='store_true')
parser_image.add_argument('-d','--dist',help='list dist images',action='store_true')
parser_image.add_argument('-i','--id',help='get image with id',type=str)
parser_image.add_argument('-u','--user',help='gets all users images',action='store_true')
parser_image.add_argument('-n','--name',help='get image by name',type=str)
#delete
parser_image_delete.add_argument('-i','--id',help='delete by id',type=str)
parser_image_delete.add_argument('-n','--name',help='delete by name',type=str)
#parse args
#parser_image_delete = parser_image_delete.parse_args()
#parser_image = parser_image.parse_args()
#parser_droplet_delete = parser_droplet_delete.parse_args()
#parser_droplet_create = parser_droplet_create.parse_args()
#parser_droplet_list = parser_droplet_list.parse_args() 
args = parser.parse_args()

def main():
	#try:
		#check for droplet args
		#droplet-create
		if args.cmd == 'droplet-create' :
			create_droplet()
			
		elif args.cmd == 'droplet-delete':
			delete_droplet()

		elif args.cmd == 'droplet-list':
			list_droplet()
		elif args.cmd == 'image-list':
			list_image()

		elif args.cmd == 'image-delete':
			delete_image()
	#except AttributeError:
	#	print(parser.print_usage())

def create_droplet():
	if ',' in str(args.tags):
		tags = slug.tags.split(',')
	droplet = DigitalOcean.Droplet(args.name)
	droplet.set_size(args.slug)
	droplet.set_image(args.operating_system)
	droplet.set_region(args.region)
	if args.private_networking:
		droplet.private_networking()
	if args.tags:
		droplet.set_tags(args.tags)
	if args.cloud_config and args.vars:
		cloud_config = DigitalOcean.CloudConfig(args.cloud_config,True)
		cloud_config.set_variables(args.vars)
		cloud_data = cloud_config.get_cloud_config()
		droplet.set_cloud_config(cloud_data)
	elif args.cloud_config:
		cloud_config = DigitalOcean.CloudConfig(args.cloud_config,True)
		cloud_data = cloud_config.get_cloud_config()
		droplet.set_cloud_config(cloud_data)
	if args.monitoring:
		droplet.set_monitoring()

	droplet.create_droplet()

def delete_droplet():
	droplet = DigitalOcean.Droplet(args.name)
	if args.name:
		#delete by name
		droplet.remove_droplet_by_name(args.name)
	elif args.id:
		droplet.remove_droplet(args.id)
	elif args.tag:
		droplet.remove_droplet_by_tag(args.tag)

def list_droplet():
	droplet = DigitalOcean.Droplet('nothing')
	#print('test')
	for drop in droplet.get_droplets():
		print('name: '+drop['name'])
		print('id: '+drop['id'])
		print('os: '+drop['image']['distribution']+''+drop['image']['name'])
		print('ip: '+drop['networks']['ip_address'])
		print('region: '+drop['region']['name'])
		print('----------------')

#terrible way to do this
def print_images(images):
	#print(images['distrubution'])
	#print(images.keys())
	if 'images' in  images.keys():
		for image in images['images']:
			#print(image)
			print('name: '+image['distribution']+' '+image['name'])
			print('slug: '+str(image['slug']))
			print('id: '+str(image['id']))
			print('----------------')
	else:
		images
		print('name: '+images['distribution']+' '+images['name'])
		print('slug: '+images['slug'])
		print('id: '+str(images['id']))
		print('----------------')

def list_image():
	image = DigitalOcean.Image()
	#print('test2')
	if args.all:
		print_images(image.get_all_images())
	elif args.app:
		print_images(image.get_application_images())
	elif args.dist:
		print_images(image.get_dist_images())
	elif args.id:
		print_images(image.get_image_by_id(args.id))
	elif args.user:
		print_images(image.get_all_user_images())
	elif args.name:
		print_images(image.get_image_by_name(args.name))

def delete_image():
	image = Image()
	if args.id:
		image.remove_image_by_id(args.id)
	elif args.name:
		image.remove_image_by_name(args.name)



#image stuff

if __name__ == '__main__':
	main()