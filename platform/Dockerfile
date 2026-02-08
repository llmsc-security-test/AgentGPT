# Dockerfile for Reworkd Platform
FROM python:3.11-slim-buster

# Install build dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    openjdk-11-jdk \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.4.2
RUN poetry config virtualenvs.create false

# Set working directory
WORKDIR /app/src

# Copy and install requirements
COPY pyproject.toml .
RUN poetry install --only main

# Copy application code
COPY . .

# Expose port
EXPOSE 11230

# Set entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
