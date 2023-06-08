FROM python:3.11-slim
RUN useradd -m app

ADD startup.sh /home/app
RUN chmod +x /home/app/startup.sh
ADD risk-accept.py requirements.txt /

RUN pip3 install -r /requirements.txt
RUN apt update && apt -y install wget

WORKDIR /home/app
USER app

ENTRYPOINT ["sh", "-c", "/home/app/startup.sh"]
