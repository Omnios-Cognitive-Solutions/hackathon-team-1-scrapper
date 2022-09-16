```bash
--+-> .devcontainer                     # [Dir] Configuration to work with VScode & Docker
  |-> .vscode                           # [Dir] Vscode Debuging configuration
  |-> data                              # [Dir] Configuration files with static non-sensitive content
  |-> src                               # [Dir] Code resources folder
  |   L-> __init__.py                   # [File] Logging configuration
  |   |-> config                        # [Dir] Environment variable loader/manager
  |   |   L-> __init__.py               # [File] Mandatory file to load .env files
  |   |   L-> aws.py                    # [File] File to load the module environment variables
  |   |   L-> dynamodb.py               # [File] File to load the module environment variables
  |   |   L-> rds.py                    # [File] File to load the module environment variables
  |   |-> integrations                  # [Dir] Contains the integrations of modules/libraries with our project
  |   |   L-> [integration_name].py     # [File] Contains the code to integrate a module with our project, "the code here is specific to the project"
  |   |-> utils                         # [Dir] Contains utilities for the rest of the code
  |   |   L-> exception.py              # [File] File containing exception generic class for error handling
  |   |   L-> toolbox.py                # [File] File containing the most common utility functions used by the code
  |   |-> wrappers                      # [Dir] Contains wrappers to ease the utilization of modules in our code
  |   |   |-> aws                       # [Dir] Contain all code related to AWS integration
  |   |   |   L-> connect.py            # [File] Init session with AWS
  |   |   |   L-> dynamodb.py           # [File] Code related to DynamoDB services
  |   |   |   L-> s3.py                 # [File] Code related to S3 services
  |   |   |   L-> exception.py          # [File] Contains Exception module specific for DB handling
  |   |   |-> db                        # [Dir] Contain all code related to RDS integration
  |   |   |   |-> controllers           # [Dir] Folder that contain all the logic usable from integrations module
  |   |   |   |   L-> logic1.py         # [File] First logic module, splited by theme
  |   |   |   |-> entities              # [Dir] Folder that contain descrption of the tables
  |   |   |   |   L-> base_entities.py  # [File] Base module to setup tables
  |   |   |   |   L-> entity_first.py   # [File] Description of the first table
  |   |   |   L-> connection.py         # [File] Establish connection with relational Database
  |   |   |   L-> exception.py          # [File] Contains Exception module specific for DB handling
  |   |   |-> [wrapper_name]            # [Dir] Contains all the wrappers for a certain module
  |   |       L> [wrapper_file].py      # [File] Code to ease a certain module utilization in our code, "the code here is project independent"
  |-> tests                             # [Dir] Contains files to perform testing
  |-> toolbox                           # [Dir] All module related to DevOps strategy
  |   L-> bitbucket-pipelines.yml       # [File] Bitbucket pipelines definition
  |   L-> Dockerfile                    # [File] Docker image build instructions
  L-> .dockerignore                 # [File] List of file to ignore wile building the Docker Image
  L-> .gitignore                        # [File] Gitignore file
  L-> main.py                           # [File] Main file to be executed (lambda handler)
  L-> requirements.txt                  # [File] Pip requirements file
```


# SetUp

We use .env to store environment variable. Because it is in the .gitignore, it will not appear in this template. Therefor, the first things to do are:
```bash
$ touch .env
$ python -m pytest tests/test_config.py
```


# Logging

We do not use print(). Instead, use:

```python
import logging
logger = logging.getLogger("module_name")
logger.info("This is an info")
logger.warning("This is a warning")
logger.error("This is an error")
```

The logging configuration is in src/__ini\__.py <br/>
The logs will appear in the console as well as in CloudWatch (AWS).

# WRAPPERS/DB

1- This wrapper aim to connect to any relational database. It needs configuration variable from src/config/rds.py<br/>

2- Your code in integration/ will use db/controllers/* . From outside wrappers/db/, you will never call any modules exception the one from controllers/. <br/>

3- The structure is the following:
```bash
-> db
| |-> controllers/ # contain your own logic
| |-> entities/ # describe the tables
| |-> connect/ # establish the connection
| L-> exception.py #handle the errors
```

