
import json
from configparser import ConfigParser

import requests
import msal


config = ConfigParser()

config.read("./config/config.init")

CLIENT_ID = config.get('power_bi_api','client_id')
CLIENT_SECRET = config.get('power_bi_api','client_secret')
TENANT_ID = config.get('power_bi_api','tenant_id')
AUTHORITY_URL = f"{config.get('power_bi_api','authority_url')}{TENANT_ID}"
SCOPE = list()
SCOPE.append(config.get('power_bi_api','scope'))


API_ENDPOINT = 'https://api.powerbi.com/v1.0/myorg/groups'


def get_token(client_id, client_secret, tenant_id, authority_url, scope):
    app = msal.ConfidentialClientApplication(
    client_id, authority=authority_url,
    client_credential=client_secret
    )
    result = None

    result = app.acquire_token_silent(scope , account=None)    

    if not result:
        result = app.acquire_token_for_client(scopes=scope)

    return result.get('access_token')

def get_header(token):
    return {'Authorization': f'Bearer {token}',
            'Content-type': 'application/json'} 


def call_API(end_point, headers):
    response = requests.get(
        end_point,
        headers=headers )
    return response.json()

try:
    token = get_token(CLIENT_ID, CLIENT_SECRET, TENANT_ID, AUTHORITY_URL, SCOPE)
    headers = get_header(token)
    api_response = call_API(API_ENDPOINT, headers)
    print(json.dumps(api_response, indent=2))
except Exception as err:
    print(err)

