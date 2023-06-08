FROM python:3.11-slim
RUN adduser -D app

ADD startup.sh /home/app
RUN chmod +x /home/app/startup.sh
ADD risk-accept.py requirements.txt /
RUN pip3 install -r /requirements.txt

WORKDIR /home/app
USER app

ENTRYPOINT ["sh", "-c", "/home/app/startup.sh"]
