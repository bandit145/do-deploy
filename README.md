# do-deploy

### Usage
  #### Setup 
   Generate a DO token with write permission and place that in the config file.

  Deploy a 512mb DO droplet with Ubuntu 16.04:
 
`./deploy.py -n test -r nyc2  -os ubuntu-16-04-x86 -s 512mb `

  Deploy the same with a cloud-config file:
  
  `./deploy.py -n test -r nyc2  -os ubuntu-16-04-x86 -s 512mb -cf test -v content=ytho,wat=bcuz`




### Command Line Syntax

 `usage: deploy.py [-h] -n NAME -os OPERATING_SYSTEM -r REGION`
`                 [-cf CLOUD_CONFIG] [-pn] -s SLUG [-b] [-t TAGS] [-v VARS]`

`deploy digital ocean servers`

`optional arguments:`
`  -h, --help            show this help message and exit`

`  -n NAME, --name NAME  Server name`

`  -os OPERATING_SYSTEM, --operating_system OPERATING_SYSTEM`
`                        DO image`

`  -r REGION, --region REGION`
`                        Server region`

`  -cf CLOUD_CONFIG, --cloud_config CLOUD_CONFIG`
`                        Cloud config file to use`

`  -pn, --private_networking`
`                        Private networking (switch)`

`  -s SLUG, --slug SLUG  Unique ram size slug`

`  -b, --backups         Enable backups (switch)`

`   -t TAGS, --tags TAGS  tags in tag,tag format`

`  -v VARS, --vars VARS  Variables for cloud_init scripts in`
`                        "var=data,var=data" format`
