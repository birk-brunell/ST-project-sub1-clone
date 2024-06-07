import subprocess
import os

def run_script(script_name):
    """Run a Python script and print its output."""
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    print(f"Running {script_name}...")
    print(result.stdout)
    if result.stderr:
        print(f"Errors:\n{result.stderr}")

scripts_to_run = [
    "generate_requirements.py",
    'copy_test_suite.py',
    "build_images.py",
    "run_images.py",
    'remove_test_suite.py'
]

for script in scripts_to_run:
    if os.path.exists(script):
        run_script(script)
    else:
        print(f"Script {script} not found.")
