#!/bin/sh

mkdir -p data/prometheus
mkdir -p data/grafana
mkdir -p data/alertmanager
sudo chmod -R 0777 data/
sleep 1
docker-compose up