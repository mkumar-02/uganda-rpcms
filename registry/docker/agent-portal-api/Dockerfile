# Uganda RPCMS Refugee Registry — Agent Portal API
# Build from registry/:  docker build -f docker/agent-portal-api/Dockerfile .
ARG RP_VERSION=0.0.0-develop.716
FROM openg2p/openg2p-registry-agent-portal-api:${RP_VERSION}

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_refugee_extension

COPY refugee-extension/ /app/refugee-extension/
RUN pip install --no-cache-dir /app/refugee-extension
