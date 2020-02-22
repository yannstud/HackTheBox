import requests
import json
import jwt
import pprint

# This should include the tenant name/id
AUTHORITY_URL = 'https://login.microsoftonline.com/ericsengines.onmicrosoft.com'
TOKEN_ENDPOINT = '/recon/TokenCache.dat'

data = {'client_id':'372efea9-7bc4-4b76-8839-984b45edfb98',
        'resource':'https://graph.microsoft.com',
        'client_secret':'redactedpassword',
        'grant_type':'client_credentials'}

r = requests.post(AUTHORITY_URL + TOKEN_ENDPOINT, data=data)

data2 = r.json()

try:
    jwtdata = jwt.decode(data2['access_token'], verify=False)
    pprint.pprint(jwtdata)
except KeyError:
    pass

