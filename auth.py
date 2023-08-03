import os
import requests
import json
from dotenv import load_dotenv
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import IAMTokenManager
from datetime import datetime


####################
## Option-1: Requesting IAM token through Python SDK  
#################

def authenticate(apikey):
    authentiator = IAMAuthenticator(apikey)
    return authentiator

# print(authenticate(my_api_key))

def generate_access_token(apikey):
    iam_token_manager = IAMTokenManager(apikey=apikey)
    # token = iam_token_manager.get_token()
    token = iam_token_manager.request_token()
    # return token
    # os.environ['ACCESS_TOKEN'] = token['access_token']
    # os.environ['EXPIRATION'] = token['expiration']
    # file persist the token
    with open('access_token.json', 'w') as fp:
        json.dump(token, fp)
        print('Token renewed and persisted..')

# generate_access_token(my_api_key)

def get_access_token(apikey) -> str:
    # read token file
    with open('access_token.json', 'r') as tf:
        token = json.load(tf) 
    # validate if token expired?
    if datetime.now() > datetime.fromtimestamp(token['expiration']):
        print('..Token renewal required..')
        generate_access_token(apikey)
    with open('access_token.json', 'r') as tf:
        token = json.load(tf)
    # print(token['access_token'])
    # print(token['expiration'])
    return token['access_token']

# get_access_token(my_api_key)



####################
## Option-2: Requesting IAM token through REST API  
#################

def refresh_token(iam_url, api_key):
    data = {
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
        'apikey': api_key,
    }

    response = requests.post(url=iam_url, data=data)
    if response.status_code == 200:
        if datetime.now() > datetime.fromtimestamp(response.json()['expiration']):
            print('..Renew Token..')
            ## generate token
            token = ''
        else:
            token = response.json()['access_token']
            expiration = response.json()['expiration']
    else:
        token = ''
        print(f'Bad Response: {response}')
    return token

# print(refresh_token(iam_url, my_api_key))


if __name__ == '__main__':
    
    load_dotenv()

    ## my_api_key = <YOUR_API_KEY>
    my_api_key = os.getenv('API_KEY', None)
    iam_url = os.getenv('IAM_URL', None)

    # print(get_access_token(my_api_key))
    # print(refresh_token(iam_url, my_api_key))

    ## Refresh Token
    generate_access_token(my_api_key)
    
