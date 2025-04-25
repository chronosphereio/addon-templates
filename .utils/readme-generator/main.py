import folder_nav
import generate_md

def generate_all():
    root_dir = "../../templates"

    manifest_data = folder_nav.iterate_file_structure(root_dir)

    generate_md.generate_md(manifest_data)

    return

generate_all()