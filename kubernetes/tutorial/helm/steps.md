- Create a kubernetes cluster using Kind

`kind create cluster --name helm --image=kindest/node:v1.21.1`

`kubectl get nodes`


- Run a `apline linux` container where we can install and play with helm
`docker run -it --rm -v ${HOME}:/root/ -v ${PWD}:/work -w /work --net host alpine sh`

**install curl & kubectl**
```
apk add --no-cache curl nano
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x ./kubectl
mv ./kubectl /usr/local/bin/kubectl
export KUBE_EDITOR="nano"
```

** test cluster access:**
`kubectl get nodes`

**Install Helm CLI**
```
curl -LO https://get.helm.sh/helm-v3.4.0-linux-amd64.tar.gz
tar -C /tmp/ -zxvf helm-v3.4.0-linux-amd64.tar.gz
rm helm-v3.4.0-linux-amd64.tar.gz
mv /tmp/linux-amd64/helm /usr/local/bin/helm
chmod +x /usr/local/bin/helm
```

**Create first helm chart**

`cd kubernetes/tutorial/helm`

`mkdir temp && cd temp`

`helm create example-app`

**Clean up the templace**

We can delete unwanted files:
- delete everything under `/templates/`, keeping only `_helpers.tpl`
- delete `tests` folder under `templates`

- clean up `values.yaml`

we can simply take our existing yaml as we have and paste to the templates folder


**testing**
`helm template example-app example-app`
name of chart and name of chart folder

**installing our chart**
`helm install example-app example-app`
name of our chart and chart folder

`helm list`

`kubectl get all`
`kubectl get cm`
`kubectl get secret`

**Value injection for our chart**
we may want to inject an image tag as a build number

add fields to `values.yaml`

```
deployment:
  image: "aimvector/python"
  tag: "1.0.4"
```

go to `deployment.yaml` and add syntax:

`image: {{ .Values.deployment.image }}:{{ .Values.deployment.tag }}`

now we upgrade

`helm upgrade example-app example-app --values ./example-app/values.yaml`

we could also do

`helm upgrade example-app example-app --set deployment.tag=1.0.4`


we can make our chart more generic

replace `example-deploy` and `example-app` to ingect : `"{{ .Values.name }}"` in

- deployments.yaml
- services.yaml
- secret.yaml
- configmap.yaml


we can create multiple instances using the generic yaml files now

create 

`example-app-02.values.yaml` and give it a different value for the `name`


`helm install example-app-02 example-app --values ./example-app/example-app-02.values.yaml`

`helm list`

`kubectl get deploy`