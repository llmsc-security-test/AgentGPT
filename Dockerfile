FROM node:19-alpine

ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV
ENV PORT=11230

RUN apk add --no-cache netcat-openbsd git python3 make g++

WORKDIR /app

COPY next/package*.json ./
RUN npm install --legacy-peer-deps --ignore-scripts

COPY next/wait-for-db.sh /usr/local/bin/wait-for-db.sh
RUN chmod +x /usr/local/bin/wait-for-db.sh

COPY next/ ./

# Create entrypoint inline - use HOSTNAME instead of host flag
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'echo "Starting AgentGPT..."' >> /entrypoint.sh && \
    echo 'export HOSTNAME="0.0.0.0"' >> /entrypoint.sh && \
    echo 'cd /app && npm run dev' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

EXPOSE 11230

ENTRYPOINT ["/entrypoint.sh"]
