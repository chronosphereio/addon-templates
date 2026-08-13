README
======

# NGINX

Comprehensive NGINX monitoring using nginx-prometheus-exporter stub_status metrics.

## Documentation

- [Getting Started with Chronosphere Collector](https://docs.chronosphere.io/ingest/metrics-traces/collector)
- [nginx-prometheus-exporter](https://github.com/nginx/nginx-prometheus-exporter)
- [NGINX stub_status](https://nginx.org/en/docs/http/ngx_http_stub_status_module.html)

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

## NGINX Overview

- Traffic
- Connection Pool
- Saturation Signals

## Deploy

```bash
cd templates/nginx
chronoctl apply -f nginx-team.yaml
chronoctl apply -f nginx-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
