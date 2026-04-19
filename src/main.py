from copystatic import copy_directory
from generate_page import generate_page

def main():
    # Step 1: Copy static → public
    copy_directory("static", "public")
    print("Static files copied successfully.")

    # Step 2: Generate index.html from markdown + template
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html"
    )

if __name__ == "__main__":
    main()
