#!/bin/bash

# Start Kafka and Zookeeper
docker-compose up -d

# Initialize MySQL database
docker exec -i mysql mysql -u root -pmyrootpass < mysql-init/init.sql