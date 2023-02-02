FROM python:3.10

ENV APP_HOME /usr/src/app

WORKDIR $APP_HOME

COPY . $APP_HOME

EXPOSE 3000

ENTRYPOINT ["python", "main.py"]
#  docker build . -t my_docker_tag
# docker run -p 3000:3000 -v ${PWD}/storage:/usr/src/app/storage/ my_docker_tag