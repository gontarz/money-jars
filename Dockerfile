# pull official base image
FROM python:3.8.0

# set work directory
WORKDIR /usr/src/code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev  -y

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/code/requirements.txt
RUN pip install -r requirements.txt

# copy project
#COPY . /usr/src/code/
