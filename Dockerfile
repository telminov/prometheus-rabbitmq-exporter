FROM python:3.6

COPY . /opt/app
WORKDIR /opt/app
RUN pip3 install -r requirements.txt


EXPOSE 9125
ENV PYTHONUNBUFFERED 1

ENTRYPOINT python3.6 server.py
