README
======

# Postgres

Comprehensive PostgreSQL monitoring via postgres_exporter database and bgwriter statistics.

## Documentation

- [Getting Started with Chronosphere Collector](https://docs.chronosphere.io/ingest/metrics-traces/collector)
- [postgres_exporter](https://github.com/prometheus-community/postgres_exporter)
- [PostgreSQL monitoring](https://www.postgresql.org/docs/current/monitoring-stats.html)

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

## PostgreSQL Overview

- Connections
- Transactions & Conflicts
- Buffer Cache & I/o
- Tuple Activity
- Background Writer & Checkpoints
- Replication & Size

## Deploy

```bash
cd templates/postgres
chronoctl apply -f postgres-team.yaml
chronoctl apply -f postgres-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
