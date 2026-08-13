README
======

# GCP Memcached

GCP Memorystore Memcached monitoring via Cloud Monitoring collector metrics.

## Documentation

- [Ingest Google Cloud Metrics with Chronosphere](https://docs.chronosphere.io/ingest/metrics-traces/gcp)
- [Memorystore for Memcached metrics](https://cloud.google.com/memorystore/docs/memcached/supported-monitoring-metrics)

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

## GCP Memorystore Memcached Overview

- Connections
- Memory
- Network

## Deploy

```bash
cd templates/gcp-memcached
chronoctl apply -f memcached-team.yaml
chronoctl apply -f memcached-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
