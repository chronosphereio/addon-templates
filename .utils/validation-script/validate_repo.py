'''
Script to validate all of the repo's templates. Run it from the addon-templates directory.
'''

import os
import subprocess

file_list_path = "all_files_to_validate.txt"
base_dir = "./templates"

with open(file_list_path, "w") as f:
    for root, _, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, ".")
            f.write(relative_path + "\n")

subprocess.run(["python3", ".utils/validation-script/validate_addon.py", file_list_path])

os.remove(file_list_path)