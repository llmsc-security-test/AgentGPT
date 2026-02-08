#!/usr/bin/env sh

# Wait for database to be available
host="${REWORKD_PLATFORM_DB_HOST:-localhost}"
port="${REWORKD_PLATFORM_DB_PORT:-3307}"

echo "Waiting for database at $host:$port..."
while ! echo "SELECT 1;" | nc "$host" "$port" > /dev/null 2>&1; do
  sleep 2
done

echo "Database is available! Starting platform service..."

# Start the platform service
exec python -m reworkd_platform
