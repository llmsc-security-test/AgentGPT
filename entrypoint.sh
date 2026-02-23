#!/bin/bash
set -e

echo "Starting reworkd--AgentGPT..."
echo "Current time: $(date)"

# Start the Next.js app with custom port 11230
exec npm run dev -- --host 0.0.0.0 --port 11230