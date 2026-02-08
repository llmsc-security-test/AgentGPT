#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t reworkd-platform:latest -f Dockerfile .

# Run the container with port mapping
echo "Starting container..."
docker run -d \
    --name platform \
    -p 11230:8000 \
    -e REWORKD_PLATFORM_HOST=0.0.0.0 \
    -e REWORKD_PLATFORM_DB_HOST=host.docker.internal \
    -e REWORKD_PLATFORM_DB_PORT=3308 \
    -e REWORKD_PLATFORM_DB_USER=reworkd_platform \
    -e REWORKD_PLATFORM_DB_PASS=reworkd_platform \
    -e REWORKD_PLATFORM_DB_BASE=reworkd_platform \
    -e OPENAI_API_KEY="${OPENAI_API_KEY:-}" \
    --add-host host.docker.internal:host-gateway \
    reworkd-platform:latest

echo "Platform service started on port 11230"
echo "API docs available at: http://localhost:11230/api/docs"
