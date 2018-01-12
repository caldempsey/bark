#!/usr/bin/env bash

# Stop all containers (if causes error then usually successful [if it is not passed any arguments then nothing to delete, see logs])
docker stop $(docker ps -a -q)
# Delete all containers (if causes error then usually successful [if it is not passed any arguments then nothing to delete, see logs])
docker rm $(docker ps -a -q)
# Delete all images the containers were instances from (if causes error then usually successful [if it is not passed any arguments then nothing to delete, see logs])
docker rmi -f $(docker images -q)
# Delete any subsequent volumes which were being used by containers.
docker volume prune -f
