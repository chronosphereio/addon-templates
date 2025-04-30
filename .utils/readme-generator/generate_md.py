import os
import math
from mdutils.mdutils import MdUtils

def generate_md(manifest_data):
    for manifest in manifest_data:
        
        readme_data = manifest_data[manifest]

        output_dir = readme_data["filepath"]
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, 'README')

        # MdUtils adds '.md' to the filename automatically
        readme_md_path = output_path + ".md"

        # Remove existing README if it exists
        if os.path.exists(readme_md_path):
            os.remove(readme_md_path)


        readme_file = MdUtils(file_name=output_path, title='README')

        readme_file.new_header(level=1, title=readme_data["name"])
        readme_file.new_paragraph(readme_data["description"])

        if len(readme_data["docs"]) != 0:
            readme_file.new_header(level=2, title="Documentation")
            items = []
            for doc_title, doc_link in readme_data["docs"].items():
                link = readme_file.new_inline_link(link=doc_link, text=doc_title)
                items.append(link)

            readme_file.new_list(items)
        readme_file.new_header(level=2, title="Available Assets")
        table_row_count = math.ceil(len(readme_data["asset_table"]) / 3)
        readme_file.new_table(columns=3, rows=table_row_count, text=readme_data["asset_table"])

        readme_file.new_header(level=2, title="Requirements")
        readme_file.new_list([
            "A Team to own the Collection (Either included or custom team)",
            "A Collection to own the asset (Either included or custom collection)",
            "A Collector to provide data",
            "Chronosphere Tenant"
        ])
        for dashboard in readme_data["dashboards"]:
            readme_file.new_header(level=2, title=dashboard["name"])
            readme_file.new_list(dashboard["panel_groups"])
        
        if len(readme_data["monitors"]) >= 1:
            readme_file.new_header(level=2, title="Monitors")
            readme_file.new_list(readme_data["monitors"])
        
        if len(readme_data["collectors"]) >= 1:
            readme_file.new_header(level=2, title="Collectors")
            readme_file.new_list(readme_data["collectors"])

        if len(readme_data["parsers"]) >= 1:
            readme_file.new_header(level=2, title="Parsers")
            readme_file.new_list(readme_data["parsers"])

        if len(readme_data["processors"]) >= 1:
            readme_file.new_header(level=2, title="Processors")
            readme_file.new_list(readme_data["processors"])

        readme_file.create_md_file()
    return