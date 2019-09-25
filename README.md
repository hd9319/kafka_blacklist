# kafka_blacklist
Blacklist Feature using Kafka. 

# Dependencies
* kafka-python
* pyodbc
* flask
* Start Zookeeper and Kafka Servers

# How it works
Each HTTP request is sent by a KafkaProducer to a message queue. KafkaConsumers poll from the queue and monitor subsequent requests made by each unique client. If too many requests are made by a single client within a defined period of time, their ip address is then added to a blacklist file. Each request validates that the client has not been blacklisted before sending an appropriate response.

