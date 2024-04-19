import os
from pathlib import Path

list_of_files = [
    ".gitignore",
    "README.md",
    "requirements.txt",
    "setup.py",
    "src/__init__.py",
    "src/main.py",
    "src/utils.py",
    "app.py",
    "scripts/run.sh",
    "templates/index.html",
    "static/css/style.css",
    "static/js/script.js",
    "static/img",
    "uploads/file.txt",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir , filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass

