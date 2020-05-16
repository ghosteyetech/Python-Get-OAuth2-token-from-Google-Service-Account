from google.cloud import container_v1

client = container_v1.ClusterManagerClient()

project_id = 'wn-cloud-275704'
zone = 'us-central1-c'

response = client.list_clusters(project_id, zone)

print(response)