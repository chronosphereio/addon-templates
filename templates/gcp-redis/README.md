README
======

# GCP Redis

GCP Memorystore for Redis monitoring via Cloud Monitoring collector metrics.

## Documentation

- [Ingest Google Cloud Metrics with Chronosphere](https://docs.chronosphere.io/ingest/metrics-traces/gcp)
- [Memorystore for Redis metrics](https://cloud.google.com/memorystore/docs/redis/supported-monitoring-metrics)

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

## GCP Memorystore Redis Overview

- Performance Metrics
- Memory Metrics
- Base Activity Metrics
- Key Metrics
- Replication & Persistence

## Deploy

```bash
cd templates/gcp-redis
chronoctl apply -f gcp-redis-team.yaml
chronoctl apply -f gcp-redis-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
