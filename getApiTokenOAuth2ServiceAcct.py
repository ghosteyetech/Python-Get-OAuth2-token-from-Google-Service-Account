

## Activate virtualenv: cloudk8s\Scripts\activate
## Run program: python .\getApiTokenOAuth2ServiceAcct.py

from google.auth.transport import requests
from google.oauth2 import service_account
from google.cloud.container_v1 import ClusterManagerClient

CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
CREDENTIALS_KEY_PATH = 'service-account-json.json'

project_id = "<project_id>"
zone = "<zone: eg: us-central1-c>"
cluster_id = "<cluster id>"

def get_service_account_token():
    credentials = service_account.Credentials.from_service_account_file(
          CREDENTIALS_KEY_PATH, scopes=CREDENTIAL_SCOPES)
    credentials.refresh(requests.Request())

    print("Token: ",credentials.token)

    test_gke(credentials)
    # return credentials.token


def test_gke(credentials):
    
    cluster_manager_client = ClusterManagerClient(credentials=credentials)
    cluster = cluster_manager_client.get_cluster(project_id, zone, cluster_id)

    configuration = client.Configuration()
    configuration.host = f"https://{cluster.endpoint}:443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + credentials.token}
    client.Configuration.set_default(configuration)

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    pods = v1.list_pod_for_all_namespaces(watch=False)
    for i in pods.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

get_service_account_token()