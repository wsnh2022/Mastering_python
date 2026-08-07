# version 2.0
# Phase 1 - file and folder creation
# Phase 2 - Python virtual environment

import venv
from pathlib import Path

print("--------------------------------")
base_path = input(
    "Enter path to create project in: (leave blank for current folder):\n"
)
project_name = Path(input("Enter project name: "))

# Combine the base path and the project name
project = Path(base_path) / project_name

# --- CREATE PROJECT FOLDER ---
if not project.exists():
    # # parents=True ensures it creates intermediate folders if the base path doesn't exist yet
    project.mkdir(parents=True)
    print("--------------------------------")
    print("PROJECT FOLDER & FILE CREATED ✅")
    print("--------------------------------")
    print(f"📁 {project}")

# --- CREATE SRC FOLDER ---
if not (project / "src").exists():
    (project / "src").mkdir()
    print(" ├──📁 src")

# --- CREATE VENV ---
venv_dir = project / ".venv"
if not venv_dir.exists():
    print(" ├──📁 venv (Setting up virtual environment... please wait)")
    venv.create(venv_dir, with_pip=True)

files = [".env", "README.md", "requirements.txt", "main.py"]

for file in files:
    file_path = project / file

    if not file_path.exists():
        file_path.touch()
        print(f" │   └──📄 {file}")
    else:
        print(f" │   └──📄 {file} (already exists)")

print("--------------------------------")
print("use → venv\\Scripts\\activate from project directory\n")