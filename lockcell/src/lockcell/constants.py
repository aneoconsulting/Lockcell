"""
Created on : 2025-01-08
Author   : Erwan Tchaleu
Email    : erwan.tchale@gmail.com

"""

import os
import yaml
from pathlib import Path

# Load configuration file path from environment variable
env_config_path = os.getenv("LOCKCELL_CONFIG")

if not env_config_path:
    raise EnvironmentError(
        "Environment variable 'LOCKCELL_CONFIG' is not set.\n"
        "Please set it to the path of your config.yaml file."
    )

config_path = Path(env_config_path)

if not config_path.is_file():
    raise FileNotFoundError(
        f"The config file specified by LOCKCELL_CONFIG does not exist: {config_path}"
    )

# Load YAML configuration
def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

_config = load_config(config_path)
### Exposing the constants

# USER_SIDE
USER_WORKING_DIR = str(Path(_config["paths"]["working_directory"]))
USER_SCRIPTS_PATH = str(Path(__file__).parent / "scripts")

# WORKER_SIDE
TASK_WORKING_DIR = "."
