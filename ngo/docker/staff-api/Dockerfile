# Build context = ngo/
FROM python:3.12-alpine

ARG FASTAPI_COMMON_REF=develop

RUN apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers make \
 && apk add --no-cache bash git gettext libpq-dev libffi-dev openssl-dev

WORKDIR /app

RUN pip install --no-cache-dir \
    "git+https://github.com/openg2p/openg2p-fastapi-common.git@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-common"

COPY backend /src/backend
RUN pip install --no-cache-dir /src/backend

RUN apk del --no-network .build-deps

ENV PYTHONUNBUFFERED=1
ENV RPCMS_NGO_HOST=0.0.0.0
ENV RPCMS_NGO_PORT=8000
ENV RPCMS_NGO_NO_OF_WORKERS=2
ENV RPCMS_NGO_WORKER_TYPE=gunicorn

CMD python3 -m openg2p_rpcms_ngo_api.main migrate && \
    gunicorn "openg2p_rpcms_ngo_api.main:app" \
      --workers ${RPCMS_NGO_NO_OF_WORKERS} \
      --worker-class uvicorn.workers.UvicornWorker \
      --bind ${RPCMS_NGO_HOST}:${RPCMS_NGO_PORT} \
      --log-level info
