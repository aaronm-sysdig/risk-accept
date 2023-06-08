FROM python:3.11-alpine
RUN adduser -D app
WORKDIR /home/app
USER app

ADD startup.sh /home/app
ADD risk-accept.py requirements.txt /
RUN pip3 install -r requirements.txt

ENTRYPOINT ["sh", "-c", "/home/app/startup.sh"]
