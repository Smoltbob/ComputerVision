#!/bin/bash
# other option
# docker run  -v "$PWD":/app -v "$PWD"/output:/app/output bazel run //lib/CameraModels:omnidirectional_main

# using a permanent container
# docker build -t bazel .

docker run -d \
  --name mybazel \
  --entrypoint /bin/bash \
  -u "$(id -u):$(id -g)" \
  -e HOME=/tmp \
  -e USER="$(whoami)" \
  -v "$(pwd)":/app \
  -v "$PWD/.bazelcache":/bazel-cache \
  -v "$(pwd)/output":/output \
  bazel \
  -c "sleep infinity"

# Then, to run commands inside the container, use:
# docker exec -w /app mybazel bazel run //lib/CameraModels:omnidirectional_main

# Afterwards, delete the container with:
# docker rm -f mybazel