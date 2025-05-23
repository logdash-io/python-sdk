FROM python:3.9-alpine

WORKDIR /app

RUN pip install logdash

COPY check-deployed-package/demo.py /app/

RUN chmod +x /app/demo.py

CMD ["python", "./check.py"] 