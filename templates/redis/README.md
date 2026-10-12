README
======

# Redis

Redis monitoring via redis_exporter Prometheus metrics.

## Documentation

- [Getting Started with Chronosphere Collector](https://docs.chronosphere.io/ingest/metrics-traces/collector)
- [redis_exporter](https://github.com/oliver006/redis_exporter)
- [Datadog redisdb dashboard (layout reference)](https://github.com/DataDog/integrations-core/tree/master/redisdb/assets/dashboards)

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

## Redis Overview

- Performance Metrics
- Memory Metrics
- Base Activity Metrics
- Key Metrics
- Replication & Persistence

## Deploy

```bash
cd templates/redis
chronoctl apply -f redis-team.yaml
chronoctl apply -f redis-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
