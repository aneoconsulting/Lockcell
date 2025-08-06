import cloudpickle

# Modules to pass to the tasks
from .config import BaseConfig
from .Tasks import utils
from . import VerrouConf

# Modules to expose to the user
from .graphViz import MultiViz
from .controllers import RDDMIN, SRDDMIN
from .VerrouConf import ConfigVerrou
from .constants import USER_SCRIPTS_PATH, USER_WORKING_DIR, TASK_WORKING_DIR

# Register modules for cloudpickle by value (transmitting the task's essential code to PymoniK)

cloudpickle.register_pickle_by_value(BaseConfig)
cloudpickle.register_pickle_by_value(utils)
cloudpickle.register_pickle_by_value(VerrouConf)


# Exposing key classes/functions at package level
__all__ = [
    "MultiViz",
    "RDDMIN",
    "SRDDMIN",
    "ConfigVerrou",
    "USER_SCRIPTS_PATH",
    "USER_WORKING_DIR",
    "TASK_WORKING_DIR",
]

# Version
__version__ = "0.7.0"
