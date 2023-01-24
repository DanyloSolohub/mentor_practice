FROM python:3.10

COPY . .

ENTRYPOINT ["python", "main.py"]
