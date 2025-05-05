import yaml
import os
import json
import converters
def parse_manifest(manifest_file_path: str):

    split_path = manifest_file_path.split("/")
    name = split_path[len(split_path)-2]
    name = converters.convert_kebab_to_title(name)

    readme_folder_path = manifest_file_path.removesuffix("manifest.yaml")
    
    manifest_data={
        "name":name,
        "description":"",
        "docs":{},
        "asset_table":["Asset Type", "Status", "Count"],
        "dashboards":[],
        "monitors":[],
        "parsers":[],
        "collectors":[],
        "processors":[],
        "filepath":readme_folder_path
    }
    counts={}

    with open(manifest_file_path, "r") as file:
        manifest: dict = yaml.safe_load(file)
    # print("manifest", manifest)
    asset_list = manifest["asset_list"]
    if "description" in manifest:
        manifest_data["description"] = manifest["description"]

    if "data_source_and_docs" in manifest and len(manifest["data_source_and_docs"]) > 0:
        for source in manifest["data_source_and_docs"]:
            title = source["title"]
            url = source["url"]
            manifest_docs = manifest_data["docs"]
            if title not in manifest_docs:
                manifest_docs[title] = url

    for asset in asset_list:
        asset_type = asset["asset_type"].lower()
        asset_name = asset["name"]
        if asset_type not in counts:
            counts[asset_type] = 1
        else:
            counts[asset_type] += 1

        if asset_type == "monitor":
            manifest_data["monitors"].append(asset_name)
        
        if asset_type == "processor":
            manifest_data["processors"].append(asset_name)

        if asset_type == "collector":
            manifest_data["collectors"].append(asset_name)

        if asset_type == "parser":
            manifest_data["parsers"].append(asset_name)
            

    for asset in counts:
        manifest_data["asset_table"].extend([asset,"✅ Available",counts[asset]])

    if "dashboard" in counts and counts["dashboard"] >= 1:
        dashboard_dir_path = manifest_file_path.replace("manifest.yaml","dashboards/")
        for dirpath, _, filenames in os.walk(dashboard_dir_path):
            for filename in filenames:
                dashboard_filepath = os.path.join(dirpath, filename)
                manifest_data['dashboards'].append(parse_dashboard_yaml(dashboard_filepath))

    return manifest_data

def parse_dashboard_yaml(dashboard_filepath):
    

    with open(dashboard_filepath, "r") as file:
        dashboard_yaml_converted: dict = yaml.safe_load(file)

        dashboard_data = {
            "name":dashboard_yaml_converted["spec"]["name"],
            "panel_groups":[]
                          }
        dashboard_json = json.loads(dashboard_yaml_converted["spec"]["dashboard_json"])
        layout_list = dashboard_json["spec"]["layouts"]

        for layout in layout_list:
            if "display" not in layout ["spec"]:
                panel_group_title = "no_group"
            else:
                panel_group_title =  layout["spec"]["display"]["title"]

            if panel_group_title not in dashboard_data["panel_groups"]:
                dashboard_data["panel_groups"] = []

            kind = layout["kind"]
            if kind == "Grid":
                panels = layout["spec"]["items"]
                for panel in panels:
                    panel_name = converters.convert_path_to_title(panel["content"]["$ref"])
                    dashboard_data["panel_groups"].append(panel_name)

    return dashboard_data