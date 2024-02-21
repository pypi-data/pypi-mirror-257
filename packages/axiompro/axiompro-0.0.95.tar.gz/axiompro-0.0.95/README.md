# axiompro
[![Python package](https://github.com/swarmsecurity/axiompro/actions/workflows/python-package.yml/badge.svg)](https://github.com/swarmsecurity/axiompro/actions/workflows/python-package.yml)

### Simple instance orchestration

axiom is developed to work with AWS and enables extremely fast and simple ec2 instance orchestration. 

The goal of axiom is to separate the logic of orchestration into a purpose built solution, then, a scanning solution such as swarm can be layered on top. 

Following the unix philosophy, do one thing good and do it well. axiom handles spinning up, spinning down, and building custom images effortlessly.

---

### Installation
```
pip3 install axiompro
```

### Setup
First, if an AWS session isn't already configured, configure one with the `--configure` option, then, use `--build` to build a base image.
```
axiompro --configure
axiompro --build
```

### Usage
```
➤ axiompro --help

 ▄▄▄      ▒██   ██▒ ██▓ ▒█████   ███▄ ▄███▓    ██▓███   ██▀███   ▒█████  
▒████▄    ▒▒ █ █ ▒░▓██▒▒██▒  ██▒▓██▒▀█▀ ██▒   ▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒
▒██  ▀█▄  ░░  █   ░▒██▒▒██░  ██▒▓██    ▓██░   ▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒
░██▄▄▄▄██  ░ █ █ ▒ ░██░▒██   ██░▒██    ▒██    ▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░
 ▓█   ▓██▒▒██▒ ▒██▒░██░░ ████▓▒░▒██▒   ░██▒   ▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░
 ▒▒   ▓▒█░▒▒ ░ ░▓ ░░▓  ░ ▒░▒░▒░ ░ ▒░   ░  ░   ▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░ 
  ▒   ▒▒ ░░░   ░▒ ░ ▒ ░  ░ ▒ ▒░ ░  ░      ░   ░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░ 
  ░   ▒    ░    ░   ▒ ░░ ░ ░ ▒  ░      ░      ░░         ░░   ░ ░ ░ ░ ▒  
      ░  ░ ░    ░   ░      ░ ░         ░                  ░         ░ ░  
                                                                         
    author: pry0cc

    
usage: axiompro [-h] [--build] [--build-script BUILD_SCRIPT] [--instance-type INSTANCE_TYPE] [--profile PROFILE] [--prefix PREFIX] [--init INIT] [-n N] [--images] [--image-id IMAGE_ID]
                [--snapshot SNAPSHOT] [--instances] [--ssh SSH] [--exec EXEC] [--rm RM [RM ...]]
                [instance_name]

axiom Instance Orchestration

positional arguments:
  instance_name         Name of the instance to perform an operation for

options:
  -h, --help            show this help message and exit
  --build               Build a new base AWS instance
  --build-script BUILD_SCRIPT
                        Optional bash script to supply with --build, will append to the default build process
  --instance-type INSTANCE_TYPE
                        Type of the instance (default: t3.micro)
  --profile PROFILE     Profile of the instance (default: axiom)
  --prefix PREFIX       Prefix of the fleet
  --init INIT           Initialize a new fleet of instances
  -n N                  Number of nodes to initialize (default: 1)
  --images              Print a table of images
  --image-id IMAGE_ID   Image ID to use as the base image
  --snapshot SNAPSHOT   Snapshot an instance by name to create an iamge
  --instances           Print a table of instance information
  --ssh SSH             Interactively SSH into an instance
  --exec EXEC           Execute a single command over SSH
  --rm RM [RM ...]      List of instance names to delete
```
### Building
```
axiompro --build
axiompro --build-script install.sh
``` 

### Orchestration
```
## List Images
axiompro --images

## Initialize a fleet with 10 instances
axiompro --init myfleet -n 10

## List instances
axiompro --instances

## Connect to an instance
axiompro --ssh myfleet0

## Build a base image from an existing instance
axiompro --snapshot myfleet06

## Execute a single command across a fleet
axiompro --exec "ifconfig" --prefix myfleet

## Delete a fleet with the prefix 'myfleet'
axiompro --rm myfleet --prefix myfleet

```


