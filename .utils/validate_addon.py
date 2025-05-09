'''
Script to validate changed files for a commit/pull request to main/staging branches of the
chronosphereio/add-on-templates repo targeting the templates directory.
'''

import sys
import yaml
import re
from collections import defaultdict
import os
import json

ALL_ASSET_TYPES = {
    "dashboards": (".yaml", ".yml"),
    "monitors": (".yaml", ".yml"),
    "notification-policies": (".yaml", ".yml"),
    "collectors": (".yaml", ".yml"),
    "processors": (".json",),
    "parsers": (".conf",),
}

PLATFORM_ASSET_TYPES = ["dashboards", "monitors", "notification-policies"]

TEAM_EXPECTED_STRUCTURE = {
    "api_version": "v1/config",
    "kind": "Team",
    "spec": {
        "slug": str,
        "name": str,
    }
}

COLLECTION_EXPECTED_STRUCTURE = {
    "api_version": "v1/config",
    "kind": "Collection",
    "spec": {
        "slug": str,
        "name": str,
        "team_slug": str,
    },
}

DASHBOARD_EXPECTED_STRUCTURE = {
    "api_version": "v1/config",
    "kind": "Dashboard",
    "spec": {
        "slug": str,
        "name": str,
        "collection_slug": str,
        "dashboard_json": str,
    },
}

MONITOR_EXPECTED_STRUCTURE = {
    "api_version": "v1/config",
    "kind": "Monitor",
    "spec": {
        "slug": str,
        "name": str,
        "collection_slug": str,
        "notification_policy_slug": str,
        "prometheus_query": str,
    }
}

NOTIFICATION_POLICY_EXPECTED_STRUCTURE = {
    "api_version": "v1/config",
    "kind": "NotificationPolicy",
    "spec": {
        "slug": str,
        "name": str,
        "team_slug": str,
        "routes": {
            "defaults": dict,
        }
    }
}

def main():
    if len(sys.argv) < 2:
        print("Correct Usage: python validate_addon.py <list of changed files>")
        sys.exit(1)
    
    # Step 1: List of changed_files (input from GitHub Actions workflow)
    changed_files = sys.argv[1:]
    print(changed_files)

    # Step 2: Group by vendor-product
    changed_by_dir = defaultdict(list)
    for changed_file in changed_files:
        if changed_file.startswith("templates/"):
            parts = changed_file.split("/")
            if len(parts) >= 3:
                vendor_product = parts[1]
                changed_by_dir[vendor_product].append(changed_file)
    
    # Step 3: Directory-level, file-level & cross-file validation 
    for vendor_product, files in changed_by_dir.items():
        print(f"\nValidating templates/{vendor_product}")
        
        existing_asset_dirs = validate_vendor_product_dir(vendor_product, files)
        validate_cross_file_references(vendor_product, files, existing_asset_dirs)
        
        print(f"templates/{vendor_product} passed validation")

# Validation functions------------------------------------------------------------

# Directory-level validation
def validate_vendor_product_dir(vendor_product, files):
    validate_files_parseable(vendor_product, files)
    check_readme_file(vendor_product, files)
    check_manifest_file(vendor_product, files)

    existing_asset_dirs = check_existing_asset_dirs(vendor_product, files)

    check_asset_dir_dependencies(vendor_product, existing_asset_dirs)
    check_required_files_in_assets(vendor_product, files, existing_asset_dirs)
    check_platform_asset_files(vendor_product, files, existing_asset_dirs)

    return existing_asset_dirs

# Cross-file validation
def validate_cross_file_references(vendor_product, files, existing_asset_dirs):
    if existing_asset_dirs.intersection(PLATFORM_ASSET_TYPES):
        team_slug = get_team_slug_from_collection(vendor_product, files)
        print("team slug", team_slug)
        collection_slug = validate_team_slug_for_collection(vendor_product, files, team_slug)
        validate_collection_slug_for_platform_assets(vendor_product, files, collection_slug)
        validate_team_slug_for_notif_policy(vendor_product, files, team_slug)

# Directory-level validation functions-------------------------------------------------------------------------------------------------------

def validate_files_parseable(vendor_product, files):
    for file in files:
        if file.endswith((".yaml", ".yml")):
            try:
                with open(file, "r") as f:
                    yaml.safe_load(f)
            except Exception:
                raise ValueError(f"{vendor_product}: The YAML file '{file}' could not be parsed.")
        elif file.endswith(".json"):
            try:
                with open(file, "r") as f:
                    json.load(f)
            except Exception:
                raise ValueError(f"{vendor_product}: The JSON file '{file}' could not be parsed.")

def check_readme_file(vendor_product, files):
    readme_file = f"templates/{vendor_product}/README.md"
    if not any(f == readme_file for f in files):
        raise ValueError(f"{vendor_product}: Missing README.md in the commit/PR.")

def check_manifest_file(vendor_product, files):
    manifest_file = next(
        (f for f in files if re.fullmatch(rf"templates/{vendor_product}/manifest\.ya?ml", f)),
        None
    )
    if not manifest_file:
        raise ValueError(f"{vendor_product}: Missing manifest YAML file in the commit/PR.")
    
    validate_manifest_file(manifest_file)

def check_existing_asset_dirs(vendor_product, files):
    existing_asset_dirs = set()
    for asset_type in ALL_ASSET_TYPES:
        if any(f.startswith(f"templates/{vendor_product}/{asset_type}/") for f in files):
            existing_asset_dirs.add(asset_type)
    if not existing_asset_dirs:
        raise ValueError(
            f"templates/{vendor_product}: Must contain at least one asset directory: dashboards, monitors, "
            "notification-policies, collectors, parsers, processors."
        )
    return existing_asset_dirs

def check_asset_dir_dependencies(vendor_product, existing_asset_dirs):
    has_monitors = "monitors" in existing_asset_dirs
    has_notification_policies = "notification-policies" in existing_asset_dirs
    if has_monitors and not has_notification_policies:
        raise ValueError(
            f"{vendor_product}: The monitors directory requires a notification-policies directory to be present as well."
        )
    if has_notification_policies and not has_monitors:
        raise ValueError(
            f"{vendor_product}: The notification-policies directory requires a monitors directory to be present as well."
        )

def check_required_files_in_assets(vendor_product, files, existing_asset_dirs):
    missing_assets = []
    invalid_files = []

    for asset_type in existing_asset_dirs:
        expected_extensions = ALL_ASSET_TYPES[asset_type]

        matching_files = [
            f for f in files
            if f.startswith(f"templates/{vendor_product}/{asset_type}/")
        ]

        if not matching_files:
            expected_ext_str = ', '.join(expected_extensions)
            missing_assets.append(
                f"The {asset_type} directory is missing a file of type {expected_ext_str}."
            )
        else:
            for file in matching_files:
                if not file.endswith(expected_extensions):
                    invalid_files.append(
                        f"{file} is not a valid {asset_type} file (expected: {', '.join(expected_extensions)})."
                    )

            if asset_type == "dashboards":
                for dashboard_file in matching_files:
                    if dashboard_file.endswith(expected_extensions):
                        try:
                            validate_dashboard_file(dashboard_file)
                        except Exception as e:
                            invalid_files.append(
                                f"Validation failed for {dashboard_file}: {e}"
                            )
            elif asset_type == "monitors":
                for monitor_file in matching_files:
                    if monitor_file.endswith(expected_extensions):
                        try:
                            validate_monitor_file(monitor_file)
                        except Exception as e:
                            invalid_files.append(
                                f"Validation failed for {monitor_file}: {e}"
                            )
            elif asset_type == "notification-policies":
                for notif_policy_file in matching_files:
                        if notif_policy_file.endswith(expected_extensions):
                            try:
                                validate_notif_policy_file(notif_policy_file)
                            except Exception as e:
                                invalid_files.append(
                                    f"Validation failed for {notif_policy_file}: {e}"
                                )

    if missing_assets:
        raise ValueError(
            f"{vendor_product}: " + ' '.join(missing_assets)
        )
    if invalid_files:
        raise ValueError(
            f"{vendor_product}: Invalid files found: " + ' | '.join(invalid_files)
        )

# Check platform assets have team & collection YAMLs
def check_platform_asset_files(vendor_product, files, existing_asset_dirs):
    has_platform_assets = any(asset_type in existing_asset_dirs for asset_type in PLATFORM_ASSET_TYPES)
    team_file = None
    collection_file = None
    
    if has_platform_assets:
        collection_files = [
            f for f in files
            if f.startswith(f"templates/{vendor_product}/") and re.search(r"collection\.ya?ml$", f)
        ]

        if len(collection_files) != 1:
            raise ValueError(f"{vendor_product}: Expected 1 *collection YAML file, found {len(collection_files)}.")
        
        collection_file = collection_files[0]
        validate_collection_file(collection_file)

        team_files = [
            f for f in files
            if f.startswith(f"templates/{vendor_product}/") and re.search(r"team\.ya?ml$", f)
        ]

        if len(team_files) != 1:
            raise ValueError(f"{vendor_product}: Expected 1 *team YAML file, found {len(team_files)}.")

        team_file = team_files[0]
        validate_team_file(team_file)

# File-level validation functions----------------------------------------------------------------------------------

def validate_manifest_file(manifest_file):
    with open(manifest_file, "r") as f:
        manifest = yaml.safe_load(f)
        
    required_top_level_keys = ["tech_type", "asset_list"]
    for key in required_top_level_keys:
        if key not in manifest:
            raise ValueError(f"Manifest file {manifest_file} is missing required key: {key}")

    if "data_source_and_docs" in manifest:
        data_source_list = manifest["data_source_and_docs"]
        if not isinstance(data_source_list, list):
            raise ValueError(
                f"Manifest file {manifest_file}: 'data_source_and_docs' should be a list."
            )

        data_source_keys = ["title", "url"]
        for i, data_source in enumerate(data_source_list):
            for key in data_source_keys:
                if key not in data_source:
                    raise ValueError(
                        f"Manifest file {manifest_file}: 'data_source_and_docs[{i}]' is missing required key: {key}"
                    )

    asset_list = manifest["asset_list"]
    if not isinstance(asset_list, list):
        raise ValueError(f"Manifest file {manifest_file} 'asset_list' should be a list.")

    asset_required_keys = ["asset_type", "name", "slug", "file", "config_required", "description"]
    for i, asset in enumerate(asset_list):
        for key in asset_required_keys:
            if key not in asset:
                raise ValueError(
                    f"Manifest file {manifest_file}: 'asset_list[{i}]' is missing required key: {key}"
                )

def validate_team_file(team_file):
    with open(team_file, 'r') as f:
        data = yaml.safe_load(f)
    check_structure(data, TEAM_EXPECTED_STRUCTURE, team_file)
    
def validate_collection_file(collection_file):
    with open(collection_file, 'r') as f:
        data = yaml.safe_load(f)
    check_structure(data, COLLECTION_EXPECTED_STRUCTURE, collection_file)

def validate_dashboard_file(dashboard_file):
    with open(dashboard_file, 'r') as f:
        data = yaml.safe_load(f)
    check_structure(data, DASHBOARD_EXPECTED_STRUCTURE, dashboard_file)

    dashboard_json_str = data['spec']['dashboard_json']
    if isinstance(dashboard_json_str, dict):
        return
    
    try:
        json.loads(dashboard_json_str)
    except Exception as e:
        raise ValueError(f"{dashboard_file}: 'dashboard_json' contains invalid JSON: {e}")

def validate_monitor_file(monitor_file):
    with open(monitor_file, 'r') as f:
        data = yaml.safe_load(f)
    check_structure(data, MONITOR_EXPECTED_STRUCTURE, monitor_file)

def validate_notif_policy_file(notif_policy_file):
    with open(notif_policy_file, 'r') as f:
        data = yaml.safe_load(f)
    check_structure(data, NOTIFICATION_POLICY_EXPECTED_STRUCTURE, notif_policy_file)

def check_structure(data, expected, file_path, parent=""):
    for key, expected_value in expected.items():
        full_key = f"{parent}{key}"
        if key not in data:
            raise ValueError(f"{file_path}: Missing key '{full_key}'.")

        value = data[key]

        if isinstance(expected_value, dict):
            if not isinstance(value, dict):
                raise ValueError(f"{file_path}: '{full_key}' should be a dictionary.")
            check_structure(value, expected_value, file_path, parent=f"{full_key}.")
        elif isinstance(expected_value, list):
            if not isinstance(value, list):
                raise ValueError(f"{file_path}: '{full_key}' should be a list.")
            if len(expected_value) != 1:
                raise ValueError(f"{file_path}: Expected structure list for '{full_key}' should have exactly one example item.")
            expected_item = expected_value[0]
            for idx, item in enumerate(value):
                item_key = f"{full_key}[{idx}]"
                if isinstance(expected_item, dict):
                    if not isinstance(item, dict):
                        raise ValueError(f"{file_path}: '{item_key}' should be a dictionary.")
                    check_structure(item, expected_item, file_path, parent=f"{item_key}.")
                elif isinstance(expected_item, type):
                    if not isinstance(item, expected_item):
                        raise ValueError(
                            f"{file_path}: '{item_key}' should be of type '{expected_item.__name__}', "
                            f"found '{type(item).__name__}'."
                        )
                elif expected_item is not None:
                    if item != expected_item:
                        raise ValueError(
                            f"{file_path}: '{item_key}' should be '{expected_item}', found '{item}'."
                        )
        elif isinstance(expected_value, type):
            if not isinstance(value, expected_value):
                raise ValueError(
                    f"{file_path}: '{full_key}' should be of type '{expected_value.__name__}', "
                    f"found '{type(value).__name__}'."
                )
        elif expected_value is not None:
            if value != expected_value:
                raise ValueError(
                    f"{file_path}: '{full_key}' should be '{expected_value}', found '{value}'."
                )

# Cross-file validation functions-----------------------------------------------------
def get_team_slug_from_collection(vendor_product, files):
    team_path = next(f for f in files if re.search(r"team\.ya?ml$", f))
    with open(team_path, "r") as f:
        team_yaml = yaml.safe_load(f)
    team_slug = team_yaml['spec']['slug']

    return team_slug

def validate_team_slug_for_collection(vendor_product, files, team_slug):
    collection_path = next(f for f in files if re.search(r"collection\.ya?ml$", f))
    with open(collection_path, "r") as f:
        collection_yaml = yaml.safe_load(f)
    
    collection_slug = collection_yaml['spec']['slug']
    collection_team_slug = collection_yaml['spec']['team_slug']
    if collection_team_slug != team_slug:
        raise ValueError(
            f"{vendor_product}: collection.yaml 'team_slug' ({collection_team_slug}) does not match team.yaml 'slug' ({team_slug})."
        )
    
    return collection_slug

def validate_collection_slug_for_platform_assets(vendor_product, files, collection_slug):
    for asset_type in ["dashboards", "monitors"]:
        for asset_file in files:
            if asset_file.endswith((".yaml", ".yml")):
                if asset_file.startswith(f"templates/{vendor_product}/{asset_type}"):
                    with open(asset_file, "r") as af:
                        data = yaml.safe_load(af)
                    asset_collection_slug = data['spec']['collection_slug']
                    if asset_collection_slug != collection_slug:
                        raise ValueError(
                            f"{vendor_product}: {asset_type[:-1]} '{asset_file}' has collection_slug '{asset_collection_slug}' but expected '{collection_slug}'."
                        )

def validate_team_slug_for_notif_policy(vendor_product, files, team_slug):
    notif_dir = f"templates/{vendor_product}/notification-policies"
    for notif_file in files:
        if notif_file.endswith((".yaml", ".yml")):
            if notif_file.startswith(notif_dir):
                with open(notif_file, "r") as nf:
                    data = yaml.safe_load(nf)
                notif_team_slug = data['spec']['team_slug']
                if notif_team_slug != team_slug:
                    raise ValueError(
                        f"{vendor_product}: notification-policy '{notif_file}' has team_slug '{notif_team_slug}' but expected '{team_slug}'."
                    )

if __name__ == "__main__":
    main()
