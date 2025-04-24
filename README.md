# addon-templates
This repository is a library of addons for Chronosphere products to enable rapid value out of the box. these templates can include dashboards, alerts, parsers, processors, and API collectors.

- [Dashboards](https://docs.chronosphere.io/observe/dashboards): Pre-built visualizations to monitor key metrics and gain insights into system performance
- [Alerts](https://docs.chronosphere.io/investigate/alerts): Proactive notifications to identify potential issues and take corrective action
- [Parsers](https://docs.chronosphere.io/pipeline-data/parsers): Ability to transform telemetry data into predictable, structured format.
- [Processors](https://docs.chronosphere.io/pipeline-data/processing-rules):
- [API Collectors](https://docs.chronosphere.io/pipeline-data/plugins/source-plugins/http-api-collector): The HTTP API Collector source plugin lets you retrieve data from your HTTP endpoints and ingest it into Chronosphere Telemetry Pipeline
- [Data Shaping and control Rules](https://docs.chronosphere.io/control/shaping): Streamline your data storage and reduce costs by aggregating metrics at scale
- Documentation: Prescriptive, clear and concise guidance on how to best take advantage of each tech type, send the data to Chronosphere and use each package effectively.


## How to navigate
The general format for this repository is laid out `templates/<vendor>-<product>/resource-type/file` with readme files and sample data. Lua script examples are the only exception to rule currently, and can be found at this path: `processors/lua_examples/<lua_name>/template.json`.

## Contributing
Contributions are open to anyone, please read the [contribution guide](https://github.com/chronosphereio/processing-templates/blob/main/CONTRIBUTING.md) for standards.

## License
the contents of this project are released under the [APACHE 2.0 License](https://github.com/chronosphereio/processing-templates/blob/main/LICENSE)
