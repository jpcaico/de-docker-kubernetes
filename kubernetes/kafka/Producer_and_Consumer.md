We assume that a Kafka cluster and management app are deployed on Minikube

The external listener of the Kafka bootstrap server is exposed by a service named demo-cluster-kafka-external-bootstrap. We can use the minikube service command to obtain the Kubernetes URL for the service.

`minikube service demo-cluster-kafka-external-bootstrap --url`

We can execute the Kafka client apps by replacing the bootstrap server address with the URL obtained in the previous step. Note that the apps should run in separate terminals.

`BOOTSTRAP_SERVERS=127.0.0.1:60901 python3 clients/producer.py`

`BOOTSTRAP_SERVERS=127.0.0.1:60901 python3 clients/consumer.py`

`minikube service kafka-ui --url`