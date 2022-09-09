FROM python:3-slim

WORKDIR /usr/src/app

RUN pip install bs4 flask requests

COPY . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=1046" ]
