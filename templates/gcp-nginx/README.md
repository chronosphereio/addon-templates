README
======

# GCP NGINX

HTTPS load balancer monitoring via GCP Cloud Monitoring (NGINX traffic analog).

## Documentation

- [Ingest Google Cloud Metrics with Chronosphere](https://docs.chronosphere.io/ingest/metrics-traces/gcp)
- [HTTPS load balancing metrics](https://cloud.google.com/load-balancing/docs/https/https-logging-monitoring)

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

## GCP HTTPS Load Balancer Overview (NGINX)

- Traffic
- Latency
- TCP Connections

## Deploy

```bash
cd templates/gcp-nginx
chronoctl apply -f gcp-nginx-team.yaml
chronoctl apply -f gcp-nginx-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
