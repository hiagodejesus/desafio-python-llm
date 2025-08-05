#!/bin/bash

docker stop $(docker ps -aq) 2>/dev/null

docker rm $(docker ps -aq) 2>/dev/null

docker rmi -f $(docker images -q) 2>/dev/null

docker volume rm $(docker volume ls -q) 2>/dev/null

docker network prune -f

echo "Limpeza completa!"
