# Python-Get-OAuth2-token-from-Google-Service-Account

## Activate virtualenv: 
```
    $ <virtual-env-name>\Scripts\activate
```

## Run program: 
```
    $ python .\getApiTokenOAuth2ServiceAcct.py
```

## Create a ClusterRole named "pod-reader" that allows user to perform "get", "watch" and "list" on pods
```
  $ kubectl create clusterrole pod-reader --verb=get,list,watch --resource=pods
```

## Create cluster role binding
```
    $ kubectl create clusterrolebinding pod-reader-binding --clusterrole=pod-reader --user=kubernetes-api-account@wn-cloud-275704.iam.gserviceaccount.com
```

## 
```
$ gcloud iam service-accounts add-iam-policy-binding kubernetes-api-account@wn-cloud-275704.iam.gserviceaccount.com --member=user:user --role=roles/container.clusterAdmin

$ gcloud iam service-accounts add-iam-policy-binding kubernetes-api-account@wn-cloud-275704.iam.gserviceaccount.com  --member=user:user  --role=roles/container.admin

```

## 
```
    $ kubectl auth can-i create deployments --namespace=dev --as=jane
    $ kubectl auth can-i create deployments --as=kubernetes-api-account@wn-cloud-275704.iam.gserviceaccount.com
    $ kubectl auth can-i list deployments.apps --as=kubernetes-api-account@wn-cloud-275704.iam.gserviceaccount.com
    $ kubectl auth can-i get pods --as=kubernetes-api-account@wn-cloud-275704.iam.gserviceaccount.com
```