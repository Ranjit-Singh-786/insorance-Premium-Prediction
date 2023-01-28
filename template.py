import os
from pathlib import Path
import logging
# define the logging object
formt = "%(lineno)d--%(name)s--%(asctime)s--%(levelname)s--%(message)s"
logging.basicConfig(
    level = logging.INFO,
    format = formt
)
# to enter the project name
while True:
    project_name = input("Enter your project name: ")
    if project_name !='':
        break
logging.info(f"Creating project by name: {project_name}")

list_of_files = [
    ".github/workflows/.gitkeep",    # to keep unnecessary data. just like .gitignore
    ".github/workflows/main.yaml",    # for github pipeline to CI/CD pipeline
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",  # ml pipeline file will be created inside the component
    f"{project_name}/entity/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/config.py",
    f"{project_name}/exception.py",
    f"{project_name}/predictor.py",
    f"{project_name}/utils.py",
    f"configs/config.yaml",
    "requirements.txt",  # to define all the dependencies
    "setup.py",  # to get source code as a library
    "main.py"     
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating a new directory at : {filedir} for file: {filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating a new file: {filename} for path: {filepath}")
    else:
        logging.info(f"file is already present at: {filepath}")