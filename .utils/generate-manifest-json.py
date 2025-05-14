#!/usr/bin/env python3

import glob
import json
import yaml

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
    # Print compact since this is consumed by tooling. Users can pipe to jq.
    print(json.dumps(data))

write_output(load_manifests())
