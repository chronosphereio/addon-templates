README
======

# GCP Mongodb

Firestore document metrics as a MongoDB-style database monitoring analog on GCP.

## Documentation

- [Ingest Google Cloud Metrics with Chronosphere](https://docs.chronosphere.io/ingest/metrics-traces/gcp)
- [Firestore monitoring](https://cloud.google.com/firestore/docs/monitor-metrics)

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

## GCP Firestore Overview (MongoDB)

- Operations
- Document Counts

## Deploy

```bash
cd templates/gcp-mongodb
chronoctl apply -f mongodb-team.yaml
chronoctl apply -f mongodb-collection.yaml
chronoctl apply -f dashboards/overview.yaml
```
