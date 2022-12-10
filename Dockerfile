# docker file (blueprint for building images)
# image (template for running container)
# container (running process with container in it)
# used version of python
FROM python:3.9
# add server.py into the container, will be added to the base folder of the container
ADD server.py .
ADD modules_dao.py .
ADD enums.py .
# install 3rd party libs
RUN pip install pika
# an environment variable so that python sends print and log statements directly to stdout
ENV PYTHONUNBUFFERED=1
# expose ip address port to docker container
EXPOSE 60000
# command used to run container in docker
CMD ["python","./server.py"]