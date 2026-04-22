from copystatic import copy_directory
from generate_pages_recursive import generate_pages_recursive

def main():
    # Step 1: Copy static → public
    copy_directory("static", "public")
    print("Static files copied successfully.")

    # Step 2: Generate index.html from markdown + template
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="public"
)
if __name__ == "__main__":
    main()
