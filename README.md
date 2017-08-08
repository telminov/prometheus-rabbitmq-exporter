[![Build Status](https://travis-ci.org/telminov/prometheus-rabbitmq-exporter.svg?branch=master)](https://travis-ci.org/telminov/prometheus-rabbitmq-exporter)

# prometheus-rabbitmq-exporter
prometheus rabbitmq exporter

## docker
build image
```bash
docker build -t prometheus-rabbitmq-exporter .
```
or get image
```bash
docker pull telminov/prometheus-rabbitmq-exporter
```

run container interactive
```bash
docker run -it --rm -v .../config.yml:/opt/app/config.yml -p 9125:9125 telminov/prometheus-rabbitmq-exporter
```

run container detached
```bash
docker run -d --name rabbitmq_exporter -v .../config.yml:/opt/app/config.yml -p 9125:9125 telminov/prometheus-rabbitmq-exporter
```
