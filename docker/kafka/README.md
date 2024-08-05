- `Docker Compose` file contains:

1. `zookeper`: uses minimum configuraton and allows anonymous login
2. `kafka-[id]`:
   1. Each broker has unique ID (`KAFKA_CFG_BROKER_ID`) and shares the same Zookeper connect parameter (`KAFKA_CFG_ZOOKEEPER_CONNECT`). These are required to connect to the Zookeper node.
   2. Each node has two listeners - `INTERNAL` and `EXTERNAL`. The `INTERNAL` is accessed on port `9092` and it is used within the same Docker network. The `EXTERNAL` is mapped from port `29092` to `29094` and it can be used to connect from outside the network.
   3. Each can be accessed without authentication (`ALLOW_PLAINTEXT_LISTENER`)
3. `networks`: A network named `kafka-network` is created and used by all services. Having a custom network can be beneficial when services are launched by multiple Docker Compose files. This custom network can be referred by services in other compose files.
4. `volumes`: Each service has its own volume that will be mapped to the container’s data folder. We can check contents of the folder in the Docker volume path. More importantly data is preserved in the Docker volume unless it is deleted so that we don’t have to recreate data every time the Kafka cluster gets started.


Start the containers

`docker-compose -f compose-kafka.yml up -d`

Produce messages

1. Command utilities are available in `/opt/bitnami/kafka/bin/` directory
2. `docker exec -it kafka-0 bash`
3. create a topic with kafka-topics.sh by specifying the bootstrap server, topic name, number of partitions and replication factors - the last two are optional
`cd /opt/bitnami/kafka/bin/`

```
./kafka-topics.sh \
   --bootstrap-server localhost:9092 --create \
   --topic orders --partitions 3 --replication-factor 3
```

4. Produce messages with `kafka-console-producer.sh`

```
./kafka-console-producer.sh \
--bootstrap-server localhost:9092 --topic orders

>product: apples, quantity:5
>product: lemons, quantity:7
```

Consume messages

1. Use `kafka-console-consumer.sh` to consume messages

`cd /opt/bitnami/kafka/bin/`

```
./kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 --topic orders --from-beginning

```

### Note on Data Persistence
Sometimes we need to remove and recreate the Kafka containers, and it can be convenient if we can preserve data of the previous run. It is possible with the Docker volumes as data gets persisted in a later run as long as we keep using the same volumes. Note, by default, Docker Compose doesn’t remove volumes, and they remain even if we run docker-compose down. Therefore, if we recreate the containers later, data is persisted in the volumes.

To give additional details, below shows the volumes created by the Docker Compose file and data of one of the brokers.

`docker volume ls | grep data`

If you want to remove everything including the volumes, add -v flag as shown below.

`docker-compose -f compose-kafka.yml down -v`

For the UI

`docker-compose -f kafka-ui.yml up -d`

`python3 producer.py`