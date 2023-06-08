FROM python:3.11-alpine

ADD risk-accept.py requirements.txt /

RUN pip3 install -r requirements.txt

RUN adduser -D app

WORKDIR /home/app

USER app

ENTRYPOINT ["python3", "/risk-accept.py"]
