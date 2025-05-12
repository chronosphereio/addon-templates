# Contributing

We love community contributions! Help us grow this project by adding your configured collector templates.

Have an idea but not sure where to start? Open an issue and we'll help guide you.

## Prerequisites

To contribute to this project, you’ll need:

- Access to a Chronosphere instance for development
- Access to the [Chronoctl CLI](https://docs.chronosphere.io/tooling/chronoctl) with your organization name and API token
- A fork of this repository

## Start Here!

Want to contribute an asset to this library? Follow these steps:

1. Fork this repo
2. Clone your fork locally (or if you're into using the github UI you can certainly do that!) 
3. Follow the project structure below to create a service folder for your asset 
4. Make sure if you're creating a new service that your service has a manifest with all the needed information. There are detailed breakdowns of what should be in the manifest and how to retrieve your assets from Chronosphere to add to the template in this repo  
   - If you're adding an asset to an existing service make sure to add your asset to the manifest
5. Once you're work is ready to be pushed back to this repo, please create a pull request to merge your fork and branch with the `staging` branch of this repo

## Project Structure

Configurations should follow this logical structure:

```text
vendor-product/
  README.md
  manifest.yaml
  <base-platform-required-assets>.yaml(team, collection)
  resource type/ (dashboards, alerts, parsers, processors, collectors)
        <template_name>.json
        <asset_name>.yaml
          ...
  resources/
        icon.svg
        dashboard-screenshot1.png
```

`<vendor>` should be a normalized form of the vendor name, e.g., Palo Alto Networks → panw. If there's no vendor, use something descriptive like linux.

`<product>` should also be normalized, e.g., Cortex XDR → cortex_xdr. For vendor-specific services (like AWS S3), use aws-s3 as the top-level directory.

`<template_name>` should be a simple, descriptive name for the collector template.

`<base-platform-required-assets>` are foundational config files (e.g., teams, collections) required to support asset imports.

### Lua Script Examples

All Lua script examples must be stored under:

```processors/lua_examples/<lua_name>/template.json```

Use `<lua_name>` as a descriptive name for the function of the Lua script.


### Manifest Files:

Each vendor-product directory must contain a manifest.yaml, which serves as an inventory of the assets included in the package and any relevant external documentation.

#### Example and key:


```
tech_type: Kubernetes  # Name of the technology

data_source_and_docs:
  - title: Getting Started with Chronosphere Collector
    url: https://docs.chronosphere.io/ingest/metrics-traces/collector 
  - title: Setting up Prometheus for Kubernetes Monitoring
    url: https://prometheus.io/docs/prometheus/latest/installation/
  - title: Chronosphere Config Builder [internal]
    url: go/config

asset_list:
  - asset_type: Collection
    name: kubernetes-io
    slug: kubernetes-io
    file: k8s-collection.yaml
    config_required: no
    description: 'A chronosphere collection for storing assets in this library. These assets will include dashboards, alerts, and data shaping rules for monitoring Kubernetes clusters.'
```

#### Manifest Key:

| Key                  | Parent               | Required / Optional | Description                                                                                                                                                                                   | Input Type     | Example                                                |
|----------------------|----------------------|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|--------------------------------------------------------|
| tech_type            | none                 | Required            | Identifies the specific technology associated with the assets and items within this directory                                                                                                 | plain text     | kubernetes, aws, gcp                                   |
| icon                 | none                 | Optional            | Identifies which icon should be used in any UI tooling. The icon can be from the bootstrap library or a filepath to a resource in the resources folder of the same vendor-product directory.  | plain text     | bi-amazon, bi-windows                                  |
| data_source_and_docs | none                 | Optional            | Identifies useful documentation for any setup required to get data to chronosphere.                                                                                                           | plain text     |                                                        |
| title                | data_source_and_docs | Required            | Title of the documentation or summary of it's use relating to this package. (required if adding docs)                                                                                         | plain text     | Ingest Google Cloud metrics                            |
| url                  | data_source_and_docs | Required            | URL to the appropriate documentation for the corresponding technology.                                                                                                                        | url / path     | https://docs.chronosphere.io/ingest/metrics-traces/gcp |
| asset_type           | none                 | Required            | Defines the type of asset being referenced.                                                                                                                                                   | plain text     | Collection, Team, Dashboard, Monitor, Drop Rule        |
| name                 | asset item           | Required            | Defines the name of the asset as it will be displayed in public UI's.                                                                                                                         | plain text     |                                                        |
| slug                 | asset item           | Required            | Defines the slug that will be referenced internally.                                                                                                                                          | plain text     |                                                        |
| file                 | asset item           | Required            | Defines the file name containing the configuration of the asset.                                                                                                                              | filepath       | dashboards/dashboard-1.yaml                            |
| screenshot           | asset item           | optional            | Defines which screenshot from the resources folder should be used in the UI.  (limit 1 screenshot per asset)                                                                                  | filepath       | resources/dashboard-1.png                              |
| config_required      | asset item           | Required            | Boolean value defining whether or not the asset requires a configuration file.                                                                                                                | boolean string | "yes", "no"                                            |
| description          | asset item           | Required            | Describes the nature and utility of the asset.                                                                                                                                                | string         |                                                        |
| screenshot           | asset item           | Optional            | Screenshot of a dasbhoard included in the package.                                                                                                                                            |                |                                                        |
## Contributing Platform-Related Assets

To contribute platform-related assets such as Dashboards, Monitors, Rules, and other configurations, you must first create and test the asset within a Chronosphere instance. Once finalized, you can export the asset's configuration and add it to this repository in the required `chronoctl` format.

You have two ways to retrieve the asset configuration:

- **Chronosphere UI**: Create the asset (e.g., a dashboard) via the Chronosphere UI. Then, use the "View Code" option and select the `chronoctl` format to obtain the configuration

- **Chronoctl CLI**: After the asset has been created in a tenant, use the `chronoctl` CLI to export the configuration in the correct format. For example:

```bash 
  chronoctl dashboards read dashboard-slug > templates/service-name/dashboards/my-new-dashboard.yaml
 ```

## Standards

Each template directory must include a README file with a minimum set of details:

1. The author of the Template and any relevant contact information
2. A description of what the template does and the expected behavior and outcome of the template, including volume reduction percentage
3. Any changes required to the template to ensure it functions correctly

A sample of events that work in the processor is required for merge approval


## Sample Data

Any sample data included with the template must be placed into the `samples` directory, and have a descriptive name.

⚠️ Absolutely no sensitive data should be committed to this repo! You are responsible for ensure the complete sanitization of any submitted samples.

## Recommendations

It is recommended that you pretty print your JSON templates before opening your pull request. a great tool for this is [jsonformatter.org](jsonformatter.org).
