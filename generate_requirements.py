import subprocess
import os

def generate_requirements(directory="pickle_test_suite"):
    """Generate requirements.txt using pipreqs."""
    try:
        os.makedirs(directory, exist_ok=True)
        subprocess.run(["pipreqs", directory, "--force"], check=True)
        print(f"requirements.txt generated in {directory}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate requirements.txt: {str(e)}")

def main():
    generate_requirements()

if __name__ == "__main__":
    main()
