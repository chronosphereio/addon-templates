import os
import yaml

def generate_manifest(directory):
    """Generates a manifest.yaml file in the given directory.

    Args:
        directory: The path to the directory.
    """

    manifest_file = os.path.join(directory, "manifest.yaml")
    if os.path.exists(manifest_file):
        print(f"Manifest file already exists in {directory}")
        return

    asset_list = []

    print(f"Processing technology: {os.path.basename(directory)}")

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".yaml", ".yml")) and file != "manifest.yaml":
                file_path = os.path.join(root, file)
                # Use os.path.relpath to get the relative path from the directory
                rel_path = os.path.relpath(file_path, directory)
                with open(file_path, "r") as f:
                    try:
                        yaml_data = yaml.safe_load(f)
                        asset_type = yaml_data.get("kind")
                        name = yaml_data.get("spec", {}).get("name")
                        slug = yaml_data.get("spec", {}).get("slug")

                        # Extract description from annotations if available and it's a Monitor
                        description = ""
                        if asset_type == "Monitor":
                            description = yaml_data.get("spec", {}).get("annotations", {}).get("description", "")

                        asset_list.append({
                            "asset_type": asset_type,
                            "name": name,
                            "slug": slug,
                            "file": rel_path, # Use the relative path here
                            "config_required": "no",
                            "description": description,
                            "author": "Chronosphere",  # Add author field with default value
                            "source": "CS"  # Add source field with default value
                        })
                    except yaml.YAMLError as e:
                        print(f"Error parsing YAML file {file_path}: {e}")

    manifest_data = {
        "tech_type": os.path.basename(directory),
        "icon": "",
        "data_source_and_docs": [
            {
                "title": "",
                "url": ""
            }
        ],
        "asset_list": asset_list
    }

    with open(manifest_file, "w") as f:
        yaml.dump(manifest_data, f, indent=2)
    print(f"Manifest file created in {directory}")

def test_manifest(directory):
    """Tests the manifest.yaml file and provides a summary."""

    manifest_file = os.path.join(directory, "manifest.yaml")
    tech_name = os.path.basename(directory)

    if not os.path.exists(manifest_file):
        print(f"No manifest file found in {directory}. Generating a scaffold...")
        generate_manifest(directory)
        return

    try:
        with open(manifest_file, "r") as f:
            manifest_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {manifest_file}: {e}")
        return

    expected_assets = {}  # Store asset counts by type
    all_files = [] #store all files for later checking.
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".yaml", ".yml")) and file != "manifest.yaml":
                file_path = os.path.join(root, file)
                # Use os.path.relpath to get the relative path
                rel_path = os.path.relpath(file_path, directory)
                all_files.append(rel_path) # Append the relative path
                with open(file_path, "r") as f:
                    try:
                        yaml_data = yaml.safe_load(f)
                        asset_type = yaml_data.get("kind")
                        name = yaml_data.get("spec", {}).get("name")
                        slug = yaml_data.get("spec", {}).get("slug")
                        if asset_type:
                            expected_assets[asset_type] = expected_assets.get(asset_type, 0) + 1
                    except yaml.YAMLError as e:
                        print(f"Error parsing YAML file {file_path}: {e}")

    manifest_assets = manifest_data.get("asset_list", [])
    manifest_asset_counts = {}
    for asset in manifest_assets:
        asset_type = asset.get("asset_type")
        manifest_asset_counts[asset_type] = manifest_asset_counts.get(asset_type, 0) + 1

    missing_assets = []
    manifest_files = [asset.get("file") for asset in manifest_assets]
    for file in all_files:
      if file not in manifest_files:
        missing_assets.append(file)

    if missing_assets:
      print("The following files are missing from the manifest:")
      for file in missing_assets:
        print(f"  - file: {file}")
      print("Consider adding them to the manifest or regenerating the scaffold.")
      test_successful = False
    else:
      test_successful = True

    print("\nTest Summary:")
    print(f"Tech Name: {tech_name}")
    for asset_type, count in expected_assets.items():
        manifest_count = manifest_asset_counts.get(asset_type, 0)
        print(f"Number of {asset_type} found: {count} (Manifest: {manifest_count})")
        if count != manifest_count:
          test_successful=False

    if test_successful:
        print("Successful Test")
    else:
        print("Test Failed")

    # Check for optional fields
    if not manifest_data.get("icon"):
        print("Recommendation: Consider adding an icon to the manifest.")
    if not manifest_data.get("data_source_and_docs"):
        print("Recommendation: Consider adding data source and docs to the manifest.")

if __name__ == "__main__":
    templates_directory = os.path.join(os.getcwd(), "templates")
    if not os.path.exists(templates_directory):
        print("templates directory not found")
        exit()

    subdirectories = [d for d in os.listdir(templates_directory) if os.path.isdir(os.path.join(templates_directory, d))]

    print("Available technologies:")
    for i, subdir in enumerate(subdirectories):
        print(f"{i+1}. {subdir}")

    choice = int(input("Enter the number of the technology to process: "))
    selected_directory = os.path.join(templates_directory, subdirectories[choice - 1])

    test_manifest(selected_directory)
