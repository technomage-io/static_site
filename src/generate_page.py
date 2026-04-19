import os

from markdown import markdown_to_html_node
from markdown import extract_title   # or wherever you defined it

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # 1. Read markdown file
    with open(from_path, "r") as f:
        markdown_content = f.read()

    # 2. Read template file
    with open(template_path, "r") as f:
        template_content = f.read()

    # 3. Convert markdown → HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # 4. Extract title
    title = extract_title(markdown_content)

    # 5. Replace placeholders
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # 6. Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # 7. Write output HTML file
    with open(dest_path, "w") as f:
        f.write(full_html)
