#!/usr/bin/env python
from datetime import  datetime

# address: server address e.g. localhost and bangkok.ischool.syr.edu
# auth: True if MongoDB authentication is enabled. If True, username and password must be given
MONGO_ACCOUNT = {'address': 'localhost',
                 'auth': True,
                 'username': 'xxx',
                 'password': 'xxx'}


DB_NAME = 'DB_NAME'
COL_NAME = 'COL_NAME'

AUTH = {
    'consumer_key': 'xxx',
    'consumer_secret': 'xxx',
    'access_token': 'xxx',
    'access_token_secret': 'xxx'
}

INPUT_FILENAME = './input.csv'
OUTPUT_FILENAME = './output.json'

