
import subprocess
import sys
from pathlib import Path

# Project folders
root = Path(__file__).resolve().parent
notebook_folder = root / ".venv" / "notebooks"

def run_script(script):
    file = root / script
    if not file.exists():
        raise FileNotFoundError(f"Missing file: {file}")

    print(f"\nRunning {script}...", flush=True)
    subprocess.run(
        [sys.executable, str(file)],
        cwd=root,
        check=True,
        timeout=300
    )
    print(f"{script} completed.", flush=True)


# 1. Generate data
run_script("generate_data.py")

# 2. Validate data
run_script("validate_data.py")


# 3. Execute both notebooks
notebooks = [
    "Part_AB_Customer_Intelligence.ipynb",
    "Part_CD_Support_Copilot.ipynb"
]

for name in notebooks:
    notebook = notebook_folder / name

    if not notebook.is_file():
        raise FileNotFoundError(f"Notebook not found: {notebook}")

    print(f"\nExecuting {name}...", flush=True)

    subprocess.run(
        [
            sys.executable,
            "-m", "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            "--ExecutePreprocessor.timeout=300",
            str(notebook)
        ],
        cwd=root,
        check=True,
        timeout=360
    )

    print(f"{name} completed successfully.", flush=True)


print("\nAll project scripts and notebooks completed!", flush=True)
