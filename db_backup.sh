#!/bin/sh

export CONTAINER_NAME="roap_db_1"
export DATABASE_NAME="roap"
export BACKUP_LOCATION="/home/ar4z/Projects"

docker exec -t ${CONTAINER_NAME} mongodump --out /data/${DATABASE_NAME}-backup --db ${DATABASE_NAME}
docker cp ${CONTAINER_NAME}:/data/${DATABASE_NAME}-backup ${BACKUP_LOCATION}
docker exec -t ${CONTAINER_NAME} rm -r /data/${DATABASE_NAME}-backup