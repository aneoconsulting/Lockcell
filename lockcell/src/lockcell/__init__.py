import cloudpickle

# Modules to pass to the tasks
from .config import BaseConfig as BaseConfigModule
from .config import TestConfig as TestConfigModule
from .Tasks import utils
from .Tasks import Results
from .Tasks import Task
from .Tasks import TaskMaster

from . import VerrouConf

# Modules to expose to the user
from .graphViz import MultiViz
from .core import Lockcell
from .VerrouConf import ConfigVerrou
from .constants import USER_SCRIPTS_PATH, USER_WORKING_DIR, TASK_WORKING_DIR
from .config.BaseConfig import BaseConfig
from .config.TestConfig import TestConfig

# Register modules for cloudpickle by value (transmitting the task's essential code to PymoniK)

cloudpickle.register_pickle_by_value(BaseConfigModule)
cloudpickle.register_pickle_by_value(utils)
cloudpickle.register_pickle_by_value(TestConfigModule)
cloudpickle.register_pickle_by_value(VerrouConf)
cloudpickle.register_pickle_by_value(Results)
cloudpickle.register_pickle_by_value(Task)
cloudpickle.register_pickle_by_value(TaskMaster)

# Exposing key classes/functions at package level
__all__ = [
    "MultiViz",
    "Lockcell",
    "BaseConfig",
    "TestConfig",
    "ConfigVerrou",
    "USER_SCRIPTS_PATH",
    "USER_WORKING_DIR",
    "TASK_WORKING_DIR",
]

# Version
__version__ = "0.7.0"
