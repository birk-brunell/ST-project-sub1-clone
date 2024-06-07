import json
import subprocess
import os

LOG_DIR = "logs"

def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

def run_image(tag):
    try:
        run_result = subprocess.run(
            ["docker", "run", "-d", tag],
            capture_output=True,
            text=True
        )
        
        container_id = run_result.stdout.strip()

        logs_result = subprocess.run(
            ["docker", "logs", container_id],
            capture_output=True,
            text=True
        )

        with open(os.path.join(LOG_DIR, "container_info.log"), "a") as log_file:
            log_file.write(f"Results for {tag}:\n{logs_result.stdout}\n")
            if logs_result.returncode != 0:
                log_file.write(f"Errors for {tag}:\n{logs_result.stderr}\n")

        print(f"Container {container_id} running for inspection. Attach to it with: docker attach {container_id}")

    except subprocess.CalledProcessError as e:
        with open(os.path.join(LOG_DIR, "failed_runs.log"), "a") as log_file:
            log_file.write(f"Failed to run Docker image {tag}: {str(e)}\n")

def main():
    setup_logging()
    
    try:
        with open(os.path.join(LOG_DIR, "built_images.json"), "r") as file:
            built_tags = json.load(file)
        
        for tag in built_tags:
            run_image(tag)
    except FileNotFoundError:
        print("No built images found. Please run the build_images.py script first.")
        return

if __name__ == "__main__":
    main()
