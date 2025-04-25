import os
import parsers

def iterate_file_structure(root_dir):
    manifest_data = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            
            if filename == "manifest.yaml":
                filepath = os.path.join(dirpath, filename)
        
                manifest_data[dirpath] = parsers.parse_manifest(filepath)

    return manifest_data