# Import key modules
import cloudpickle

from lockcell.Tasks import TaskEnv
from lockcell.graphViz import MultiViz

import lockcell.controllers as controllers
import lockcell.VerrouConf as VerrouConf
import lockcell.constants as constants

# Register modules for cloudpickle by value (transmitting the task's essential code to PymoniK)
cloudpickle.register_pickle_by_value(TaskEnv)
cloudpickle.register_pickle_by_value(controllers)
cloudpickle.register_pickle_by_value(VerrouConf)
cloudpickle.register_pickle_by_value(constants)

# Exposing key classes/functions at package level
__all__ = [
    "MultiViz",
    "controllers",
    "VerrouConf",
    "constants"
]

# Version
__version__ = "0.7.0"
