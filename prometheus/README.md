Monitoring and Alerting with Prometheus
=======================================

Prometheus is a cloud-native monitoring and alerting tool that's easy
to implement and use.

## Demo

The demo below expects to be run on a Linux/Unix machine such as Linux or a Mac.

To get started you'll need to install [Docker](https://docs.docker.com/install/) and
[Docker Compose](https://docs.docker.com/compose/install/). Switch in to the
`prometheus/demo` directory, and run `./start.sh` (creates an insecure folder for
persistence and starts things).

After everything starts you'll be able to access [Grafana](http://localhost:3000),
[Prometheus](http://localhost:9090), [Alertmanager](http://localhost:9093), and
[Node Exporter](http://localhost:9100) on your local machine.

Prometheus will start scraping itself, the node exporter, and Grafana for metrics to look
at.

Once things are up, try running the query `prometheus_tsdb_head_series` to see how many
metrics you're capturing, then start to experiment (if you break something just ctrl-c
out of Docker, delete `demo/data/`, and start over fresh)

The components that require persistent data will keep everything in `prometheus/demo/data`.