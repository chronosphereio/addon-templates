#!/usr/bin/env python3

import yaml, json, os, glob

BRANCH = os.getenv("BRANCH_NAME", "staging")
OUTPUT_FILE = f"manifests-{BRANCH}.json"
OUTPUT_DIR = os.path.join(".utils", "output")

def load_manifests():
    manifests = []
    for path in glob.glob("templates/*/manifest.yaml"):
        with open(path, "r") as f:
            try:
                data = yaml.safe_load(f)
                manifests.append(data)
            except Exception as e:
                print(f"Error reading {path}: {e}")
    return manifests

def write_output(data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, OUTPUT_FILE), "w") as out:
        json.dump(data, out, indent=2)

write_output(load_manifests())
