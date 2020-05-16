

## Activate virtualenv: cloudk8s\Scripts\activate
## Run program: python .\getApiTokenOAuth2ServiceAcct.py

from google.auth.transport import requests
from google.oauth2 import service_account
from google.cloud.container_v1 import ClusterManagerClient
import requests as httpsRequests
from kubernetes import client, config
from os import path

import yaml

CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
CREDENTIALS_KEY_PATH = 'wn-cloud-275704-52dd099c2945.json' #NEW wncp

project_id = "wn-cloud-275704"
zone = "us-central1-c"
cluster_id = "wn-cloud-portal-qa"

def get_service_account_token():
    credentials = service_account.Credentials.from_service_account_file(
          CREDENTIALS_KEY_PATH, scopes=CREDENTIAL_SCOPES)
    credentials.refresh(requests.Request())

    print("Token: ",credentials.token)

    # getClusterNodes(credentials.token)
    # test_gke(credentials)
    createDeployment(credentials)
    # return credentials.token

def getClusterNodes(token):
    apiKeyK8s = "AIzaSyB4sDvn8CGxVh1z8fLd8wn3E9J2GXhjJ5I"
    # endpoint = "https://container.googleapis.com/v1/projects/{projectId}/zones/{zone}/clusters/{clusterId}?key={apiKey}".format(projectId = project_id, zone = zone, clusterId = cluster_id, apiKey = apiKeyK8s)
    endpoint = "https://container.googleapis.com/v1/projects/{projectId}/zones/{zone}/clusters?key={apiKey}".format(projectId = project_id, zone = zone, apiKey = apiKeyK8s)

    print("endpoint: ", endpoint)

    data = {}
    headers = {"Authorization": "Bearer "+token,  "Accept": "application/json"}

    print(httpsRequests.get(endpoint, data=data, headers=headers).json())


def createDeployment(credentials):
    
    cluster_manager_client = ClusterManagerClient(credentials=credentials)
    cluster = cluster_manager_client.get_cluster(project_id, zone, cluster_id)

    print("CLUSTER END POINT: ", cluster.endpoint)

    configuration = client.Configuration()
    configuration.host = f"https://{cluster.endpoint}:443"
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + credentials.token}
    client.Configuration.set_default(configuration)

    with open(path.join(path.dirname(__file__), "nginx-deployment.yaml")) as f:
        dep = yaml.safe_load(f)
        k8s_apps_v1 = client.AppsV1Api()
        resp = k8s_apps_v1.create_namespaced_deployment(
            body=dep, namespace="default")
        print("Deployment created. status='%s'" % resp.metadata.name)

def test_gke(credentials):
    
    cluster_manager_client = ClusterManagerClient(credentials=credentials)
    cluster = cluster_manager_client.get_cluster(project_id, zone, cluster_id)

    print("CLUSTER END POINT: ", cluster.endpoint)

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