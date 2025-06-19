#!/bin/bash

# Ensure a command is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <bazel-command>"
    exit 1
fi

DOCKER_PATH="Docker/Bazel"
DOCKER_IMAGE="bazel"

# Build the Docker image if it doesn't exist
if ! docker image inspect "$DOCKER_IMAGE" > /dev/null 2>&1; then
    echo "Docker image '$DOCKER_IMAGE' not found. Building it..."
    docker build -t "$DOCKER_IMAGE" $DOCKER_PATH
fi

# Run the Bazel command inside the Docker container
docker run --rm -v "$(pwd)":/app "$DOCKER_IMAGE" "$@"