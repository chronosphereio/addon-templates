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
from team import Team
from collection import Collection
from dashboard import Dashboard
from monitor import Monitor
from notification_policy import NotificationPolicy
from manifest import Manifest

ALL_ASSET_TYPES = {
    "dashboards": (".yaml", ".yml"),
    "monitors": (".yaml", ".yml"),
    "notification-policies": (".yaml", ".yml"),
    "collectors": (".yaml", ".yml"),
    "processors": (".json",),
    "parsers": (".conf",),
}

PLATFORM_ASSET_TYPES = ["dashboards", "monitors", "notification-policies"]

def main():
    if len(sys.argv) < 2:
        print("Correct Usage: python validate_addon.py <list of changed files>")
        sys.exit(1)

    # Step 1: List of changed files (input from GitHub Actions workflow)
    changed_files = sys.argv[1]
    with open(changed_files, 'r') as f:
        changed_files = [line.strip() for line in f if line.strip()]

    print(f"Found {len(changed_files)} files to validate:")
    for file in changed_files:
        print(file)

    # Step 2: Group by vendor-product
    changed_by_dir = defaultdict(list)
    for changed_file in changed_files:
        if changed_file.startswith("templates/"):
            parts = changed_file.split("/")
            if len(parts) >= 3:
                vendor_product = parts[1]
                changed_by_dir[vendor_product].append(changed_file)
    
    # Step 3: Directory-level, file-level & cross-file validation 
    all_errors = []

    for vendor_product, files in changed_by_dir.items():
        print(f"\nValidating templates/{vendor_product}")
        
        existing_asset_dirs, errors = validate_vendor_product_dir(vendor_product, files)
        all_errors.extend(errors)
        
        cross_file_errors = validate_cross_file_references(vendor_product, files, existing_asset_dirs)
        all_errors.extend(cross_file_errors)

        print(f"templates/{vendor_product} passed validation")

    if all_errors:
        print("\nValidation failed with the following errors:")
        for err in all_errors:
            print(f"- {err}")
        sys.exit(1)

# Validation functions------------------------------------------------------------

# Directory-level validation
def validate_vendor_product_dir(vendor_product, files):
    errors = []

    errors.extend(validate_json_files_parseable(vendor_product, files))
    errors.extend(check_readme_file(vendor_product, files))
    errors.extend(check_manifest_file(vendor_product, files))

    existing_asset_dirs, result = check_existing_asset_dirs(vendor_product, files)
    errors.extend(result)

    errors.extend(check_asset_dir_dependencies(vendor_product, existing_asset_dirs))
    errors.extend(check_required_files_in_assets(vendor_product, files, existing_asset_dirs))
    errors.extend(check_platform_asset_files(vendor_product, files, existing_asset_dirs))

    return existing_asset_dirs, errors

# Cross-file validation
def validate_cross_file_references(vendor_product, files, existing_asset_dirs):
    errors = []

    if existing_asset_dirs.intersection(PLATFORM_ASSET_TYPES):
        team_slug = get_team_slug_from_collection(vendor_product, files)
        collection_slug = None

        if team_slug:
            collection_slug, result = validate_team_slug_for_collection(vendor_product, files, team_slug)
            errors.extend(result)

            errors.extend(validate_team_slug_for_notif_policy(vendor_product, files, team_slug))

            if collection_slug:
                errors.extend(validate_collection_slug_for_platform_assets(vendor_product, files, collection_slug))
            else:
                errors.append(f"Skipping cross-file validation for {vendor_product} due to missing collection slug.")
        else:
            errors.append(f"Skipping cross-file validation for {vendor_product} due to missing team slug.")

    return errors

# Directory-level validation functions-------------------------------------------------------------------------------------------------------

def validate_json_files_parseable(vendor_product, files):
    errors = []

    for file in files:
        if file.endswith(".json"):
            try:
                with open(file, "r") as f:
                    json.load(f)
            except Exception as e:
                errors.append(f"{file}: JSON could not be parsed. Error: {e}")
    
    return errors

def check_readme_file(vendor_product, files):
    readme_file = f"templates/{vendor_product}/README.md"
    if readme_file not in files:
        return [f"{vendor_product}: Missing README.md in the commit/PR."]
    return []

def check_manifest_file(vendor_product, files):
    manifest_file = next(
        (f for f in files if re.fullmatch(rf"templates/{vendor_product}/manifest\.ya?ml", f)),
        None
    )
    if not manifest_file:
        return [f"{vendor_product}: Missing manifest YAML file in the commit/PR."]
    
    return validate_manifest_file(manifest_file)

def check_existing_asset_dirs(vendor_product, files):
    existing_asset_dirs = set()

    for asset_type in ALL_ASSET_TYPES:
        if any(f.startswith(f"templates/{vendor_product}/{asset_type}/") for f in files):
            existing_asset_dirs.add(asset_type)
    if not existing_asset_dirs:
        return set(), [f"templates/{vendor_product}: Must contain at least one asset directory: {', '.join(ALL_ASSET_TYPES)}."]
    return existing_asset_dirs, []

def check_asset_dir_dependencies(vendor_product, existing_asset_dirs):
    has_monitors = "monitors" in existing_asset_dirs
    has_notification_policies = "notification-policies" in existing_asset_dirs
    if has_monitors and not has_notification_policies:
        return [f"{vendor_product}: The monitors directory requires a notification-policies directory to be present as well."]
    if has_notification_policies and not has_monitors:
        return [f"{vendor_product}: The notification-policies directory requires a monitors directory to be present as well."]

    return []

def check_required_files_in_assets(vendor_product, files, existing_asset_dirs):
    errors = []

    for asset_type in existing_asset_dirs:
        expected_extensions = ALL_ASSET_TYPES[asset_type]
        expected_ext_str = ', '.join(expected_extensions)

        matching_files = [
            f for f in files
            if f.startswith(f"templates/{vendor_product}/{asset_type}/")
        ]

        if not matching_files:
            errors.append(
                f"{vendor_product}: The {asset_type} directory is missing a file of type {expected_ext_str}."
            )
            continue

        for file in matching_files:
            if not file.endswith(expected_extensions):
                errors.append(f"{file} is not a valid {asset_type} file (expected: {expected_ext_str}).")
                continue

            validator_map = {
                "dashboards": validate_dashboard_file,
                "monitors": validate_monitor_file,
                "notification-policies": validate_notif_policy_file,
            }

            validate_fn = validator_map.get(asset_type)
            if validate_fn:
                errors.extend(validate_fn(file))

    return errors

# Check platform assets have team & collection YAMLs
def check_platform_asset_files(vendor_product, files, existing_asset_dirs):
    errors = []

    has_platform_assets = any(asset_type in existing_asset_dirs for asset_type in PLATFORM_ASSET_TYPES)
    if not has_platform_assets:
        return []

    # Collection file check
    collection_files = [
        f for f in files
        if f.startswith(f"templates/{vendor_product}/") and re.search(r"collection\.ya?ml$", f)
    ]

    if len(collection_files) != 1:
        errors.append(f"{vendor_product}: Expected 1 *collection YAML file, found {len(collection_files)}.")
    else:
        errors.extend(validate_collection_file(collection_files[0]) or [])

    # Team file check
    team_files = [
        f for f in files
        if f.startswith(f"templates/{vendor_product}/") and re.search(r"team\.ya?ml$", f)
    ]

    if len(team_files) != 1:
        errors.append(f"{vendor_product}: Expected 1 *team YAML file, found {len(team_files)}.")
    else:
        errors.extend(validate_team_file(team_files[0]) or [])

    return errors

# File-level validation functions----------------------------------------------------------------------------------

def validate_manifest_file(manifest_file):
    try:
        with open(manifest_file, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"{manifest_file}: YAML could not be parsed. Error: {e}"]
        
    try:
        Manifest.parse_obj(data)
    except Exception as e:
        return [f"{manifest_file}: {e}"]

    return []

def validate_team_file(team_file):
    try:
        with open(team_file, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"{team_file}: YAML could not be parsed. Error: {e}"]

    try:
        Team.parse_obj(data)
    except Exception as e:
        return [f"{team_file}: {e}"]

    return []
    
def validate_collection_file(collection_file):
    try:
        with open(collection_file, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"{collection_file}: YAML could not be parsed. Error: {e}"]

    try:
        Collection.parse_obj(data)
    except Exception as e:
        return [f"{collection_file}: {e}"]
    
    return []

def validate_dashboard_file(dashboard_file):
    errors = []

    try:
        with open(dashboard_file, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"{dashboard_file}: YAML could not be parsed. Error: {e}"]

    try:
        Dashboard.parse_obj(data)
    except Exception as e:
        errors.append(f"{dashboard_file}: {e}")

    dashboard_json_str = data['spec']['dashboard_json']
    if isinstance(dashboard_json_str, dict):
        return errors
    
    try:
        json.loads(dashboard_json_str)
    except Exception as e:
        errors.append(f"{dashboard_file}: 'dashboard_json' contains invalid JSON: {e}")

    return errors

def validate_monitor_file(monitor_file):
    try:
        with open(monitor_file, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"{monitor_file}: YAML could not be parsed. Error: {e}"]

    try:
        Monitor.parse_obj(data)
    except Exception as e:
        return [f"{monitor_file}: {e}"]
    
    return []

def validate_notif_policy_file(notif_policy_file):
    try:
        with open(notif_policy_file, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"{notif_policy_file}: YAML could not be parsed. Error: {e}"]

    try:
        NotificationPolicy.parse_obj(data)
    except Exception as e:
        return [f"{notif_policy_file}: {e}"]

    return []

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
    team_path = next((f for f in files if re.search(r"team\.ya?ml$", f)), None)
    if not team_path:
        return None
    
    try: 
        with open(team_path, "r") as f:
            team_yaml = yaml.safe_load(f)
    except Exception:
        return None
    
    team_slug = team_yaml.get('spec', {}).get('slug')
    return team_slug

def validate_team_slug_for_collection(vendor_product, files, team_slug):
    errors = []
    collection_slug = None

    collection_path = next((f for f in files if re.search(r"collection\.ya?ml$", f)), None)
    if not collection_path:
        return collection_slug, []

    try:
        with open(collection_path, "r") as f:
            collection_yaml = yaml.safe_load(f)
    except Exception:
        return collection_slug, []
    
    collection_slug = collection_yaml.get('spec', {}).get('slug')
    collection_team_slug = collection_yaml.get('spec', {}).get('team_slug')
    if collection_team_slug != team_slug:
        errors.append(f"{vendor_product}: collection.yaml 'team_slug' ({collection_team_slug}) does not match team.yaml 'slug' ({team_slug}).")
    
    return collection_slug, errors

def validate_collection_slug_for_platform_assets(vendor_product, files, collection_slug):
    errors = []

    for asset_type in ["dashboards", "monitors"]:
        for asset_file in files:
            if asset_file.endswith((".yaml", ".yml")):
                if asset_file.startswith(f"templates/{vendor_product}/{asset_type}"):
                    with open(asset_file, "r") as af:
                        try:
                            data = yaml.safe_load(af)
                        except Exception:
                            continue

                    asset_collection_slug = data.get('spec', {}).get('collection_slug')
                    if asset_collection_slug != collection_slug:
                        errors.append(f"{vendor_product}: {asset_type[:-1]} '{asset_file}' has collection_slug '{asset_collection_slug}' but expected '{collection_slug}'.")
    
    return errors

def validate_team_slug_for_notif_policy(vendor_product, files, team_slug):
    notif_dir = f"templates/{vendor_product}/notification-policies"
    for notif_file in files:
        if notif_file.endswith((".yaml", ".yml")):
            if notif_file.startswith(notif_dir):
                with open(notif_file, "r") as nf:
                    try:
                        data = yaml.safe_load(nf)
                    except Exception:
                        return []

                notif_team_slug = data.get('spec', {}).get('team_slug')
                if notif_team_slug != team_slug:
                    return [f"{vendor_product}: notification-policy '{notif_file}' has team_slug '{notif_team_slug}' but expected '{team_slug}'."]

    return []

if __name__ == "__main__":
    main()
