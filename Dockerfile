FROM python:3.7-alpine

MAINTAINER Oren Cohen "orenc@comm-it.co.il"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]