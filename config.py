import os
import sys

import yaml

__all__ = [
    "projects",
]

PROJECTS_ROOT_DIR = os.path.dirname(__file__)

config_filepath = os.path.join(PROJECTS_ROOT_DIR, "projects-config.yml")
if not os.path.isfile(config_filepath):
    print(f"Please set {config_filepath} config file.")
    sys.exit()
with open(config_filepath) as f:
    projects = yaml.safe_load(f)

if __name__ == "__main__":
    from pprint import pprint

    pprint(projects)
   