FROM python:3.9-alpine

WORKDIR /app

# The version to check, the latest when empty; PyPI can take a few minutes to serve one just published
ARG LOGDASH_VERSION
RUN for _ in $(seq 30); do pip install --no-cache-dir "logdash${LOGDASH_VERSION:+==$LOGDASH_VERSION}" && exit 0; sleep 10; done; exit 1

COPY check-deployed-package/check.py /app/

RUN chmod +x /app/check.py

CMD ["python", "./check.py"] 