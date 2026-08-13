README
======

# GCP Rabbitmq

GCP Pub/Sub subscription metrics as a RabbitMQ queue monitoring analog.

## Documentation

- [Ingest Google Cloud Metrics with Chronosphere](https://docs.chronosphere.io/ingest/metrics-traces/gcp)
- [Pub/Sub monitoring](https://cloud.google.com/pubsub/docs/monitoring)

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
- Chronosphere Google Cloud integration enabled for the target project
- Cloud Monitoring metrics for the managed service ingested into Chronosphere

## GCP Pub/Sub Overview (RabbitMQ)

- Queue Depth
- Message Rates

## Deploy

```bash
cd templates/gcp-rabbitmq
chronoctl apply -f rabbitmq-team.yaml
chronoctl apply -f rabbitmq-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
