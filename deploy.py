import configparser
import argparse
parser = argparse.ArgumentParser(description='deploy digital ocean servers')
parser.add_argument('-n','--name',help='Server name', required=True)
parser.add_argument('-r','--region',help='Server region', required=True)
parser.add_argument('-cf','--cloud_config',help='Cloud config file to use')
parser.add_argument('-pn','--private_networking',help='private networking')
config = configparser.ConfigParser()
config.read('config.ini')