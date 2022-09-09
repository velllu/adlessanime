FROM ubuntu:latest

WORKDIR /usr/src/app

RUN apt-get update

# DEPENDENCIES
RUN apt-get -qq -y install python3
RUN apt-get -qq -y install python3-pip

RUN pip install flask bs4 requests

# RUNNING APP
COPY . .

CMD export FLASK_APP=app.py
CMD flask run --host=0.0.0.0 --port 4567