FROM python:3.10

COPY . /usr/src/app

WORKDIR /usr/src/app

ENTRYPOINT ["python", "main.py"]
