import os
from markdown import markdown_to_html_node, extract_title

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Load template once
    with open(template_path, "r") as f:
        template_content = f.read()

    # Walk through content directory
    for root, dirs, files in os.walk(dir_path_content):
        for filename in files:
            if filename.endswith(".md"):
                md_path = os.path.join(root, filename)

                # Read markdown
                with open(md_path, "r") as f:
                    markdown_content = f.read()

                # Convert markdown → HTML using YOUR parser
                html_node = markdown_to_html_node(markdown_content)
                html_content = html_node.to_html()

                # Extract title
                title = extract_title(markdown_content)

                # Fill template
                full_html = template_content.replace("{{ Title }}", title)
                full_html = full_html.replace("{{ Content }}", html_content)

                # Compute output path
                relative_path = os.path.relpath(root, dir_path_content)
                output_dir = os.path.join(dest_dir_path, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                output_filename = filename.replace(".md", ".html")
                output_path = os.path.join(output_dir, output_filename)

                # Write HTML file
                with open(output_path, "w") as f:
                    f.write(full_html)

                print(f"Generated: {output_path}")
