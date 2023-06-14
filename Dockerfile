FROM python:3.11-slim

RUN useradd -m app

ADD risk-accept.py requirements.txt /home/app/

RUN pip3 install -r /home/app/requirements.txt

WORKDIR /home/app
USER app

ENTRYPOINT ["python3","/home/app/risk-accept.py"]
