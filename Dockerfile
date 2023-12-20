FROM alpine:latest
RUN apk add python3
RUN apk add py3-pip
RUN pip install -r requirements.txt
WORKDIR /project
ADD . /project
EXPOSE 10138
CMD ["python", "src/main.py"]
