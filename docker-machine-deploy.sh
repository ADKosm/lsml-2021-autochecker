#!/bin/bash

set -e

eval $(docker-machine -s . env autochecker)

echo "Pull..."
docker-compose -f docker-compose.yaml pull

echo "Preparing to stop services..."
docker-compose -f docker-compose.yaml ps
docker-compose -f docker-compose.yaml stop -t 60

echo "Starting services..."
docker-compose -f docker-compose.yaml up --build -d
docker-compose -f docker-compose.yaml ps
