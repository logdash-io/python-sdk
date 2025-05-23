FROM python:3.9-alpine

WORKDIR /app

RUN pip install logdash

COPY check-deployed-package/check.py /app/

RUN chmod +x /app/check.py

CMD ["python", "./check.py"] 