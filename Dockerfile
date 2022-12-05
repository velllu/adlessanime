FROM alpine:latest
RUN apk add python3
RUN apk add py3-pip
RUN pip install bs4 flask requests
WORKDIR /project
ADD . /project
EXPOSE 10138
CMD ["python", "app.py"]