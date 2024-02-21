# axiom

### Simple instance orchestration

axiom is developed to work with AWS and enables extremely fast and simple ec2 instance orchestration. 

The goal of axiom is to separate the logic of orchestration into a purpose built solution, then, a scanning solution such as swarm can be layered on top. 

Following the unix philosophy, do one thing good and do it well. axiom handles spinning up, spinning down, and building custom images effortlessly.

---

### Usage
```
➤ ./axiom.py --help                                                                                                                                                                                    git:main
usage: axiom.py [-h] [--build] [--instance-type INSTANCE_TYPE] [--profile PROFILE] [--init INIT] [-n N] [--images] [--image-id IMAGE_ID] [--snapshot SNAPSHOT] [--instances] [--ssh SSH] [--exec EXEC]
                [--rm RM [RM ...]]
                [instance_name]

axiom Instance Orchestration

positional arguments:
  instance_name         Name of the instance to perform an operation for

options:
  -h, --help            show this help message and exit
  --build               Build a new base AWS instance
  --instance-type INSTANCE_TYPE
                        Type of the instance (default: t3.micro)
  --profile PROFILE     Profile of the instance (default: work)
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
