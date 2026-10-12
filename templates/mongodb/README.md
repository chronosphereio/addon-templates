README
======

# Mongodb

Comprehensive MongoDB monitoring via Percona/mongodb_exporter serverStatus metrics.

## Documentation

- [Getting Started with Chronosphere Collector](https://docs.chronosphere.io/ingest/metrics-traces/collector)
- [mongodb_exporter](https://github.com/percona/mongodb_exporter)
- [MongoDB serverStatus](https://www.mongodb.com/docs/manual/reference/command/serverStatus/)

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

## MongoDB Overview

- Connections
- Operations
- Memory & Cache
- Query & Asserts
- Replication

## Deploy

```bash
cd templates/mongodb
chronoctl apply -f mongodb-team.yaml
chronoctl apply -f mongodb-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
