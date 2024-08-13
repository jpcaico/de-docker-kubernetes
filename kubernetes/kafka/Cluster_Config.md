### Strimzi

Strimzi is a tool designed to help run Apache Kafka in Kubernetes. Running Kafka by itself can have a lot of moving parts (brokers, zookeepers, etc). Strinzi makes it easier to run Kafka on Kubernetes by managing all complex details for you.

**Operator**
Strimzi uses an `Operator`, which knows how Kafka should run, takes care of setting Kafka up, fix if something goes wrong and upgrades when needed.

**Custom Resources Definitions (CRDs)**
In Kubernetes, you usually describe what you want your system to look like using YAML files. Strimzi introduces special types of resources that let you define Kafka clusters, topcis, and users directly in these files. This means you can manage kafka the same way you manage the rest of your applications in kubernetes.

**Scaling**
Strimzi lets you add more Kafka brokers (the parts of Kafka that handle data) easily. Just update your configuration, and Strimzi will do the rest.

**Security and Monitoring**
Strimzi also helps with securing your Kafka setup (e.g., using encryption) and integrating with monitoring tools like Prometheus and Grafana so you can keep an eye on how your Kafka cluster is doing.

### Kafka Cluster

We deploy the Kafka Cluster using the Strimzi Operator on a Minikube cluster.

**Minikube**
Minikube is a tool that allows you to run Kubernetes on your local machine. It's a personal, lightweight version of Kubernetes that you can use to test and experiment without needing a big server setup. Before you can run Kafka on Kubernetes, you need to set up a Kubernetes environment. Since you’re working on your local machine, you use Minikube for this purpose.


`minikube start --cpus='max' --memory=10240 --addons=metrics-server --kubernetes-version=v1.27.0`

### Deploy Strimzi Operator


**Manifest File**
In kubernetes, manifest files is like a blueprint that describes the resources you want to create in your cluster. These files are written in yaml format and tell kubernetes how to set up things like applications, services and other infrastructure components.

**Namespace**
In Kubernetes, a namespace is like a folder where your resources live. By default, the downloaded manifest assumes you want to deploy everything in a namespace called "myproject." However, in this tutorial, you’re using the default namespace (which is where resources go if you don’t specify a namespace).

Then, you use the kubectl create command to tell Kubernetes to create all the resources described in the file. This command essentially hands over the blueprint to Kubernetes and says, "Build this for me."


```
## download and update strimzi oeprator manifest

STRIMZI_VERSION="0.39.0"

DOWNLOAD_URL=https://github.com/strimzi/strimzi-kafka-operator/releases/download/$STRIMZI_VERSION/strimzi-cluster-operator-$STRIMZI_VERSION.yaml
 
curl -L -o kafka/manifests/strimzi-cluster-operator-$STRIMZI_VERSION.yaml ${DOWNLOAD_URL}



# update namespace from myproject to default

sed -i 's/namespace: .*/namespace: default/' manifests/strimzi-cluster-operator-$STRIMZI_VERSION.yaml (for Unix)
sed -i '' 's/namespace: .*/namespace: default/' manifests/strimzi-cluster-operator-$STRIMZI_VERSION.yaml (for MacOS)


## deploy strimzi cluster operator
kubectl create -f manifests/strimzi-cluster-operator-$STRIMZI_VERSION.yaml

### check deployments
kubectl get deploy,rs,po

```

By this point we have set:

1 **Minikube Cluster**: lighweight local version of kubernetes
2. **Strimzi Operator**: Deployed the Strimzi Operator on our kubernetes cluster. This deployment includes over 20 resources necessary to manage kafka on Kubernetes

### Deploy Kafka Cluster

**Kafka Cluster**
Kafka Cluster is essentially a group of Kafka brokers working together to manage and distribute data. Brokers are the componentes in the Kafka that store, manage and distribute messages. The Zookeeper node is a separate service that helps manage and coordinate the kafka brokers, keeping track of things like which broker is responsible for which data.


- Deploy a Kafka cluster with two brokers and one Zookeeper node. It has both internal and external listeners on port 9092 and 29092 respectively.
- The external listener is configured as the nodeport type so that the associating service can be accessed from the host machine.
- Cluster is configured to allow automatic creation of topics (auto.create.topics.enable: “true”) and the default number of partition is set to 3 (num.partitions: 3).

> **Internal Listener (port: 9092)**: This is used for communication within the Kubernetes cluster, where different parts of your system can talk to Kafka.
> **External Listener (port: 29092)**: This is set up as a NodePort, which allows your Kafka cluster to be accessed from outside the Kubernetes cluster (like from your laptop or another machine). This is useful when you need to send or receive data from Kafka while working on your local machine.


Run
`kubectl create -f manifests/kafka-cluster.yaml`

When the Kafka and Zookeeper nodes are deployed, Kubernetes uses something called StatefulSets. Here’s why:

StatefulSets ensure that each Kafka broker and Zookeeper node has a unique identifier and maintains that identity, even if it restarts. This is important for Kafka because it relies on the uniqueness of each broker to manage data correctly.
The deployment also creates services, which are like communication gateways:

Internal Services: Allow components inside Kubernetes to communicate with Kafka (e.g., demo-cluster-kafka-bootstrap).
External Services: Allow communication from outside Kubernetes (e.g., demo-cluster-kafka-external-bootstrap).

`kubectl get all -l app.kubernetes.io/instance=demo-cluster`

```
communication within Kubernetes cluster

demo-cluster-kafka-bootstrap - to access Kafka brokers from the client and management apps
demo-cluster-zookeeper-client - to access Zookeeper node from the management app

communication from host
demo-cluster-kafka-external-bootstrap - to access Kafka brokers from the client apps
```

### Deploy Kafka UI

UI for Apache Kafka (kafka-ui) is a free and open-source Kafka management application, and it is deployed as a Kubernetes Deployment. The Deployment is configured to have a single instance, and the Kafka cluster access details are specified as environment variables. The app is associated by a service of the NodePort type for external access.

`kubectl create -f manifests/kafka-ui.yaml`

`kubectl get all -l app=kafka-ui`

We can use the minikube service command to obtain the Kubernetes URL for the kafka-ui service.

`minikube service kafka-ui --url`


### Delete Resources
The Kubernetes resources and Minikube cluster can be removed by the kubectl delete and minikube delete commands respectively.


`kubectl delete -f manifests/kafka-cluster.yaml`
`kubectl delete -f manifests/kafka-ui.yaml`
`kubectl delete -f manifests/strimzi-cluster-operator-$STRIMZI_VERSION.yaml`
`minikube delete`


_____

Running a Kafka producer within a Kubernetes cluster using kubectl:

**kubectl run kafka-producer:**
This creates a new pod in the Kubernetes cluster. The pod is named kafka-producer.

**--image=quay.io/strimzi/kafka:0.27.1-kafka-2.8.1:**
Specifies the Docker image to use for this pod. The image quay.io/strimzi/kafka:0.27.1-kafka-2.8.1 is a Kafka image provided by Strimzi, which includes Kafka version 2.8.1.

**--rm:**
Automatically removes the pod once the command completes. This ensures that the pod does not remain in the cluster after it has finished running.

**-it:**
Runs the command in an interactive mode (-i stands for interactive and -t allocates a pseudo-TTY). This allows you to interact with the Kafka producer from the command line.

**--restart=Never:**
Specifies that the pod should not be restarted automatically if it exits. This is useful for running one-off tasks like this one.

**--:**
The double hyphen -- indicates the end of the kubectl command arguments. Everything after this is passed to the container within the pod.

**bin/kafka-console-producer.sh:**
This is the command that runs inside the pod. It's a script that starts a Kafka producer, which can send messages to a Kafka topic.

**--bootstrap-server demo-cluster-kafka-bootstrap:9092:**
The --bootstrap-server argument specifies the Kafka broker to connect to. Here, demo-cluster-kafka-bootstrap:9092 refers to the Kafka bootstrap service in the Kubernetes cluster, which runs on port 9092.

**--topic demo-topic:**
Specifies the Kafka topic where the producer will send messages. In this case, the topic is named demo-topic.

```
kubectl run kafka-producer --image=quay.io/strimzi/kafka:0.27.1-kafka-2.8.1 --rm -it --restart=Never \
  -- bin/kafka-console-producer.sh --bootstrap-server demo-cluster-kafka-bootstrap:9092 --topic demo-topic
  ```


```
kubectl run kafka-consumer --image=quay.io/strimzi/kafka:0.27.1-kafka-2.8.1 --rm -it --restart=Never \
-- bin/kafka-console-consumer.sh --bootstrap-server demo-cluster-kafka-bootstrap:9092 --topic demo-topic --from-beginning
```