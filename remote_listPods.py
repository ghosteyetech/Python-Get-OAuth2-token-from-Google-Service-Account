import base64
import google.auth.transport.requests
from google.oauth2 import service_account
from google.cloud.container_v1 import ClusterManagerClient
from kubernetes import client
from python_hosts.hosts import Hosts, HostsEntry


def test_gke():
    project_id = "wn-cloud-275704"
    zone = "us-central1-c"
    cluster_id = "wn-cloud-portal-qa"

    # Use a service account configured in GCP console,
    # authenticating with a JSON key
    credentials = service_account.Credentials \
        .from_service_account_file('wn-cloud-275704-24c84de6f442.json')

    print('Authentication done------------------------------>')        

    # Get cluster details
    cluster_manager_client = ClusterManagerClient(credentials=credentials)
    cluster = cluster_manager_client.get_cluster(
            project_id=project_id, zone=zone,
            cluster_id=cluster_id)
    print('cluster info received------------------------------>')        

    # Save cluster certificate for SSL verification
    cert = base64.b64decode(cluster.master_auth.cluster_ca_certificate)
    cert_filename = 'cluster_ca_cert'
    cert_file = open(cert_filename, 'w')
    cert_file.write(cert)
    cert_file.close()

    # Configure hostname for SSL verification
    hosts = Hosts()
    hosts.add([HostsEntry(
            entry_type='ipv4',
            address=cluster.endpoint, names=['kubernetes'])])
    hosts.write()

    # Get a token with the scopes required by GKE
    kubeconfig_creds = credentials.with_scopes(
            ['https://www.googleapis.com/auth/cloud-platform',
             'https://www.googleapis.com/auth/userinfo.email'])
    auth_req = google.auth.transport.requests.Request()
    kubeconfig_creds.refresh(auth_req)

    configuration = client.Configuration()
    configuration.host = "https://kubernetes"
    configuration.ssl_ca_cert = cert_filename
    kubeconfig_creds.apply(configuration.api_key)
    client.Configuration.set_default(configuration)

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    pods = v1.list_pod_for_all_namespaces(watch=False)
    for i in pods.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

test_gke()