README
======

# GCP KAFKA

GCP Managed Kafka monitoring via Cloud Monitoring collector metrics.

## Documentation

- [Ingest Google Cloud Metrics with Chronosphere](https://docs.chronosphere.io/ingest/metrics-traces/gcp)
- [Managed Service for Apache Kafka metrics](https://cloud.google.com/managed-service-for-apache-kafka/docs/monitor-cluster)

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

## GCP Managed Kafka Overview

- Throughput
- Request Latency
- Consumer Groups & Errors
- CPU

## Deploy

```bash
cd templates/gcp-kafka
chronoctl apply -f kafka-team.yaml
chronoctl apply -f kafka-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
