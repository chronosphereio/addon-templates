README
======

# Memcached

Comprehensive Memcached monitoring via prometheus memcached_exporter.

## Documentation

- [Getting Started with Chronosphere Collector](https://docs.chronosphere.io/ingest/metrics-traces/collector)
- [memcached_exporter](https://github.com/prometheus/memcached_exporter)
- [Memcached stats](https://docs.memcached.org/features/statistics/)

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

## Memcached Overview

- Connections & Commands
- Memory & Items
- Cache Efficiency
- Network

## Deploy

```bash
cd templates/memcached
chronoctl apply -f memcached-team.yaml
chronoctl apply -f memcached-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
