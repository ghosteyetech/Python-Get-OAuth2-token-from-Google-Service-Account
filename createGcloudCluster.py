

## Activate virtualenv: cloudk8s\Scripts\activate
## Run program: python .\getApiTokenOAuth2ServiceAcct.py

from google.auth.transport import requests
from google.oauth2 import service_account
from google.cloud.container_v1 import ClusterManagerClient
import requests as httpsRequests
import json

CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
CREDENTIALS_KEY_PATH = 'wn-cloud-275704-52dd099c2945.json'

project_id = "wn-cloud-275704"
zone = "us-central1-c"
cluster_id = "wn-cloud-portal-qa"
apiKeyK8s = "AIzaSyB4sDvn8CGxVh1z8fLd8wn3E9J2GXhjJ5I"

def get_service_account_token():
    credentials = service_account.Credentials.from_service_account_file(
          CREDENTIALS_KEY_PATH, scopes=CREDENTIAL_SCOPES)
    credentials.refresh(requests.Request())

    print("Token: ",credentials.token)

    createCluster(credentials.token)

def createCluster(token):
    
    endpoint = "https://container.googleapis.com/v1beta1/projects/{projectId}/zones/{zone}/clusters?key={apiKey}".format(projectId = project_id, zone = zone, apiKey = apiKeyK8s)

    print("endpoint: ", endpoint)

    data = {
        "cluster": {
            "name": "test-rest-clust-1",
            "initialNodeCount": 1
        }
    }

    headers = {"Authorization": "Bearer "+token,  "Accept": "application/json"}

    print(httpsRequests.post(endpoint, data=json.dumps(data), headers=headers).json())

get_service_account_token()