README
======

# KAFKA

Comprehensive Kafka broker monitoring — JMX exporter metrics (kafka_server_*) and kafka_exporter lag metrics.

## Documentation

- [Getting Started with Chronosphere Collector](https://docs.chronosphere.io/ingest/metrics-traces/collector)
- [Kafka JMX metrics](https://kafka.apache.org/documentation/#monitoring)
- [kafka_exporter](https://github.com/danielqsj/kafka_exporter)

## Available Assets

| Asset Type | Status | Count |
| :---: | :---: | :---: |
| collection | ✅ Available | 1 |
| dashboard | ✅ Available | 1 |
| team | ✅ Available | 1 |

## Requirements

- A Team to own the Collection (either included or a custom team)
- A Collection to own the asset (either included or a custom collection)
- A Collector to provide data
- Chronosphere tenant
- Prometheus-compatible metrics from the technology exporter (see Documentation)
- Chronosphere Collector or Prometheus scrape configuration targeting the exporter `/metrics` endpoint

## Kafka Overview

- Throughput
- Replication
- Request Latency
- Consumer Lag (kafka_exporter)

## Deploy

```bash
cd templates/kafka
chronoctl apply -f kafka-team.yaml
chronoctl apply -f kafka-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
