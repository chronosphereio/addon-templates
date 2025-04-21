# Apache Cassandra 
Apache Cassandra is a highly scalable, distributed NoSQL database designed to handle large amounts of data across many servers, providing high availability with no single point of failure.

## Available Assets
| Asset Type | Status       | Quantity |
| ---------- | ------------ | -------- |
| Collection | ✅ Available | 1        |
| Dashboards | ✅ Available | 1        |
| Team       | ✅ Available | 1        |


# Requirements
- A Team to own the Collection (Either included or custom team)
- A Collection to own the asset (Either included or custom collection)
- A Collector to provide data
- Chronosphere Tenant

# Installation:

1. Download the .yaml file for the asset you want to add to your tenant.

    - If you haven't installed Chronoctl please refer to our [installation guide](https://docs.chronosphere.io/tooling/chronoctl/install).

2. Use the [chronoctl auth command](https://docs.chronosphere.io/tooling/chronoctl#auth) to login to your tenant.

3. Ensure that you have a team and a collection to assign the asset to. If you do not have one you may use the included team or collection .yaml files.

4.  For adding each asset, the [chronoctl apply command](https://docs.chronosphere.io/tooling/chronoctl#apply) needs to be used in the following order.
    - Apply the team file
    - Apply the collection file
    - Apply any assets for your chosen service

# Dashboards 
## Cassandra JMX Exporter Dashboard 
This dashboard provides real-time insights into the health, performance, and internal behavior of Apache Cassandra nodes through metrics exposed by the JMX Exporter.


Data Source: Prometheus, scraping metrics via the Cassandra JMX Exporter.

### Panels
- Uptime
- Containers
- Load
- Persistent Volume Usage
- 
