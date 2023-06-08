FROM python:3.11-alpine

ADD risk-accept.py requirements.txt /
ADD startup.sh /home/app

RUN pip3 install -r requirements.txt

RUN adduser -D app

WORKDIR /home/app

USER app

ENTRYPOINT ["sh", "-c", "/home/app/startup.sh"]
