import os
import shutil

source_dir = "./pickle_test_suite"
destination_dir = "./docker_build_scripts"

for subdir in os.listdir(destination_dir):
    subdir_path = os.path.join(destination_dir, subdir)
    if os.path.isdir(subdir_path):
        for file_name in os.listdir(source_dir):
            full_file_name = os.path.join(source_dir, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, subdir_path)
                print(f"Loading {file_name} to {subdir_path}")
