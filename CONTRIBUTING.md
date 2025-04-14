# Contributing 

We love community contributions! Help us expand this project with your configured collector templates.

Have an idea, but don't know where to start? Open an issue and we'll help you!

## Project Structure

Configurations must be stored in a logical structure:

```text
vendor-product/
  README.md
  manifest.yaml
  <base-platform-required-assets>.yaml(team, collection)
  resource type/ (dashboards, alerts, parsers, processors, collectors)
        <template_name>.json
        <asset_name>.yaml
          ...
  images/
        icon.svg
        dashboard-screenshot1.png
```

`<vendor>` is a normalized form of the vendor's name, for example: `Palo Alto Networks` to `panw`, or when there is no specific vendor use a descriptive like `linux` for linux os logs. 

`<product>` is a normalized form of the vendor's product name, for example: `Cortex XDR` to `cortex_xdr`. For an individual service or product provided by a vendor, the recommended structure would be for the top level template directory to reflect the service, for example `aws-s3`. 
`<template_name>` is a simple descriptive name for the collector template.

`<base-platform-required-assets>` are the base organizational structure required to import specific asset types like dashboards, monitors, data shaping rule and others. If a folder contains these asset types, the required asset yamls should be present within the vendor-product directory.

### Lua Script Examples

Lua script examples should all be stored in the following path: `processors/lua_examples/<lua_name>/template.json` using the same logical structure as other projects. 

`<lua_name>` is a descriptive name for the function of the lua script in question.

### Manifest Files:

The manifest file is a requirement within each vendor-product directory. It serves the purpose of a general inventory of what is included in that package as well as including any relevant links to outside documentation or dependencies. 

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

| Key                  | Parent               | Required / Optional | Description                                                                                                                                                                                | Input Type     | Example                                                |
|----------------------|----------------------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|--------------------------------------------------------|
| tech_type            | none                 | Required            | Identifies the specific technology associated with the assets and items within this directory                                                                                              | plain text     | kubernetes, aws, gcp                                   |
| icon                 | none                 | Optional            | Identifies which icon should be used in any UI tooling. The icon can be from the bootstrap library or a filepath to a resource in the images folder of the same vendor-product directory.  | plain text     | bi-amazon, bi-windows                                  |
| data_source_and_docs | none                 | Optional            | Identifies useful documentation for any setup required to get data to chronosphere.                                                                                                        | plain text     |                                                        |
| title                | data_source_and_docs | Required            | Title of the documentation or summary of it's use relating to this package. (required if adding docs)                                                                                      | plain text     | Ingest Google Cloud metrics                            |
| url                  | data_source_and_docs | Required            | URL to the appropriate documentation for the corresponding technology.                                                                                                                     | url / path     | https://docs.chronosphere.io/ingest/metrics-traces/gcp |
| asset_type           | none                 | Required            | Defines the type of asset being referenced.                                                                                                                                                | plain text     | Collection, Team, Dashboard, Monitor, Drop Rule        |
| name                 | asset item           | Required            | Defines the name of the asset as it will be displayed in public UI's.                                                                                                                      | plain text     |                                                        |
| slug                 | asset item           | Required            | Defines the slug that will be referenced internally.                                                                                                                                       | plain text     |                                                        |
| file                 | asset item           | Required            | Defines the file name containing the configuration of the asset.                                                                                                                           | filename       | manifest.yaml                                          |
| config_required      | asset item           | Required            | Boolean value defining whether or not the asset requires a configuration file.                                                                                                             | boolean string | "yes", "no"                                            |
| description          | asset item           | Required            | Describes the nature and utility of the asset.                                                                                                                                             | string         |                                                        |
| screenshot           | asset item           | Optional            | Screenshot of a dashboard included in the package.                                                                                                                                         |                |                                                        |
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