import os

source_dir = "./pickle_test_suite"
destination_dir = "./docker_build_scripts"

for subdir in os.listdir(destination_dir):
    subdir_path = os.path.join(destination_dir, subdir)
    if os.path.isdir(subdir_path):
        for file_name in os.listdir(source_dir):
            file_path_in_subdir = os.path.join(subdir_path, file_name)
            if os.path.isfile(file_path_in_subdir):
                os.remove(file_path_in_subdir)
                print(f"Unload {file_name} from {subdir_path}")
