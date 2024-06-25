#!/bin/bash

# Build the Docker images
docker-compose build

# Run the Docker Compose to execute the tests
docker-compose up

