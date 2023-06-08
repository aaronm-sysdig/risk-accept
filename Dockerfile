FROM python:3.11-slim

ADD risk-accept.py requirements.txt /

RUN useradd -m app
RUN pip3 install -r /requirements.txt
RUN apt update && apt -y install wget

WORKDIR /home/app
USER app

ENTRYPOINT ["python3","/risk-accept.py"]
