import os
import json
import subprocess

LOG_DIR = "logs"

def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    for log_file in ["build_results.log", "failed_runs.log", "container_info.log"]:
        open(os.path.join(LOG_DIR, log_file), 'w').close()

def generate_tag(subdir):
    parts = subdir.split('_')
    if len(parts) == 3:
        os_name, os_version, python_version = parts
        python_version = python_version.replace('python', 'python-')
        tag = f"{os_name}-{os_version}-{python_version}"
        return tag
    else:
        raise ValueError(f"Unexpected directory name format: {subdir}")

def build_image(subdir):
    tag = generate_tag(subdir)
    directory = os.path.join("docker_build_scripts", subdir)
    try:
        build_result = subprocess.run(["docker", "build", "-t", tag, "."], capture_output=True, text=True, cwd=directory)
        if build_result.returncode != 0:
            print(f"Build failed for {tag}: {build_result.stderr}")
            with open(os.path.join(LOG_DIR, "build_results.log"), "a") as log_file:
                log_file.write(f"Build errors for {tag}:\n{build_result.stderr}\n")
            return None
        else:
            with open(os.path.join(LOG_DIR, "build_results.log"), "a") as log_file:
                log_file.write(f"Build succeeded for {tag}.\n")
        return tag
    except subprocess.CalledProcessError as e:
        with open(os.path.join(LOG_DIR, "build_results.log"), "a") as log_file:
            log_file.write(f"Failed to build Docker image for {subdir}: {str(e)}\n")
        return None

def main():
    setup_logging()
    
    base_dir = "docker_build_scripts"
    built_tags = []
    
    for subdir in os.listdir(base_dir):
        if os.path.isdir(os.path.join(base_dir, subdir)):
            try:
                tag = build_image(subdir)
                if tag:
                    built_tags.append(tag)
            except ValueError as e:
                print(f"Skipping {subdir}: {e}")
                with open(os.path.join(LOG_DIR, "build_results.log"), "a") as log_file:
                    log_file.write(f"Skipping {subdir}: {str(e)}\n")
    
    with open(os.path.join(LOG_DIR, "built_images.json"), "w") as file:
        json.dump(built_tags, file)

if __name__ == "__main__":
    main()
