import os
import sys

import yaml

__all__ = [
    "projects",
]

PROJECTS_ROOT_DIR = os.path.dirname(__file__)

projects_filepath = os.path.join(PROJECTS_ROOT_DIR, "projects-config.yml")
if not os.path.isfile(projects_filepath):
    print(f"Please set {projects_filepath} config file.")
    sys.exit()
with open(projects_filepath) as f:
    projects = yaml.safe_load(f)

if __name__ == "__main__":
    from pprint import pprint

    pprint(projects)
   