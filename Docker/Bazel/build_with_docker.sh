#!/bin/bash
# other option
# docker run  -v "$PWD":/app -v "$PWD"/output:/app/output bazel run //lib/CameraModels:omnidirectional_main

# using a permanent container
# docker build -t bazelimage -f Docker/Bazel/Dockerfile .

docker run -d \
  --name mybazel \
  --entrypoint /bin/bash \
  -u "$(id -u):$(id -g)" \
  -e HOME=/tmp \
  -e USER="$(whoami)" \
  -v "$(pwd)":/app \
  -v "$PWD/.bazelcache":/bazel-cache \
  -v "/Users/julessimon/Downloads/FB-SSEM_dataset":/app/Data \
  -v "$(pwd)/output":/output \
  bazelimage \
  -c "sleep infinity"

# Then, to run commands inside the container, use:
# docker exec -w /app mybazel bazel run //lib/CameraModels:omnidirectional_main

# Afterwards, delete the container with:
# docker rm -f mybazel