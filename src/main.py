from copystatic import copy_directory
from generate_pages_recursive import generate_pages_recursive
import sys

def main():
    copy_directory("static", "docs")
    print("Static files copied successfully.")

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="docs",
        basepath=basepath
    )

if __name__ == "__main__":
    main()
