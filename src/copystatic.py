import os
import shutil


def copy_static_files(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for item in os.listdir(src_dir):
        from_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_static_files(from_path, dest_path)
    