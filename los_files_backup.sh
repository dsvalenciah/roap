#!/bin/sh

export CONTAINER_NAME="roap_learning_object_collection_1"
export BACKUP_LOCATION="/home/ar4z/Projects"

docker exec -t ${CONTAINER_NAME} zip -r /tmp/los-files-backup.zip /run/files
docker cp ${CONTAINER_NAME}:/tmp/los-files-backup.zip ${BACKUP_LOCATION}
docker exec -t ${CONTAINER_NAME} rm /tmp/los-files-backup.zip