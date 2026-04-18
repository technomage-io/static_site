import os
import shutil

def copy_directory(src, dst):
    # 1. Delete destination directory if it exists
    if os.path.exists(dst):
        shutil.rmtree(dst)
        print(f"Deleted existing directory: {dst}")

    # 2. Recreate destination directory
    os.mkdir(dst)
    print(f"Created directory: {dst}")

    # 3. Recursively copy contents
    def recursive_copy(current_src, current_dst):
        for item in os.listdir(current_src):
            src_path = os.path.join(current_src, item)
            dst_path = os.path.join(current_dst, item)

            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
                print(f"Copied file: {src_path} -> {dst_path}")
            else:
                os.mkdir(dst_path)
                print(f"Created directory: {dst_path}")
                recursive_copy(src_path, dst_path)

    recursive_copy(src, dst)
