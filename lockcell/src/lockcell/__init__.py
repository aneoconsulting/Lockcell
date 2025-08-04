# Import key modules
import cloudpickle



import lockcell.Tasks.TaskEnv as TaskEnv
import lockcell.controllers as controllers
from lockcell.graphViz import MultiViz
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
