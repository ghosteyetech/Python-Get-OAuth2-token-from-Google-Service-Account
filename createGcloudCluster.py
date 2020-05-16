

## Activate virtualenv: cloudk8s\Scripts\activate
## Run program: python .\getApiTokenOAuth2ServiceAcct.py

from google.auth.transport import requests
from google.oauth2 import service_account
from google.cloud.container_v1 import ClusterManagerClient
import requests as httpsRequests
import json

CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
CREDENTIALS_KEY_PATH = '<service_account_json_file_path>'

project_id = "<project_id>"
zone = "<zone>"
cluster_id = "<cluster_id>"
apiKeyK8s = "<apiKeyK8s>"

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
