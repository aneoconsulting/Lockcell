import cloudpickle

# Modules to pass to the tasks
from .config import BaseConfig as BaseConfigModule
from .config import TestConfig as TestConfigModule
from .Tasks import utils
from . import VerrouConf

# Modules to expose to the user
from .graphViz import MultiViz
from .controllers import RDDMIN, SRDDMIN
from .VerrouConf import ConfigVerrou
from .constants import USER_SCRIPTS_PATH, USER_WORKING_DIR, TASK_WORKING_DIR
from .config.BaseConfig import BaseConfig
from .config.TestConfig import TestConfig

# Register modules for cloudpickle by value (transmitting the task's essential code to PymoniK)

cloudpickle.register_pickle_by_value(BaseConfigModule)
cloudpickle.register_pickle_by_value(utils)
cloudpickle.register_pickle_by_value(TestConfigModule)
cloudpickle.register_pickle_by_value(VerrouConf)

# Exposing key classes/functions at package level
__all__ = [
    "MultiViz",
    "RDDMIN",
    "SRDDMIN",
    "BaseConfig",
    "TestConfig",
    "ConfigVerrou",
    "USER_SCRIPTS_PATH",
    "USER_WORKING_DIR",
    "TASK_WORKING_DIR",
]

del BaseConfigModule, TestConfigModule, utils, VerrouConf

# Version
__version__ = "0.7.0"
