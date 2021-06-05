
import json

import requests
import msal


client_id = '<client_id>'
client_secret = '<client_secret>'
tenant_id = '<tenant_id>'
authority_url = f'https://login.microsoftonline.com/{tenant_id}'
scope = ["https://analysis.windows.net/powerbi/api/.default"]
#scope = [ "https://graph.microsoft.com/.default" ]
#endpoint = "https://graph.microsoft.com/v1.0/users"
endpoint =  'https://api.powerbi.com/v1.0/myorg/datasets'


# Create a preferably long-lived app instance which maintains a token cache.
app = msal.ConfidentialClientApplication(
    client_id, authority=authority_url,
    client_credential=client_secret
    )

# The pattern to acquire a token looks like this.
result = None

# Firstly, looks up a token from cache
# Since we are looking for token for the current app, NOT for an end user,
# notice we give account parameter as None.
result = app.acquire_token_silent(scope , account=None)


if not result:
    result = app.acquire_token_for_client(scopes=scope)

if "access_token" in result:
    # Calling graph using the access token
    response = requests.get(  # Use token to call downstream service
        endpoint,
        headers={'Authorization': 'Bearer ' + result['access_token']}, )
    
    print("Graph API call result: ")
    print(response.status_code)
    print(json.dumps(response.json(), indent=2))
    
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug