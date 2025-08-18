from pymonik import task

from ..config.BaseConfig import BaseConfig
from ..graph import Node
from .Results import TaskResult
from .utils import AminusB
from .Task import nTask

@task
def running_rddmin_task(search_space : list, config : BaseConfig, graph_root : Node, previous_result : tuple = None): # type: ignore

    if previous_result:
        # to delete as soon as TaskResult will be implemented in Task.py
        previous_result :TaskResult = TaskResult(*previous_result)

        # Does the union of the lists contained in failing_subset_list
        all = sum(previous_result.failing_subset_list , [])
        search_space = AminusB(search_space, all)

    result = nTask.invoke(search_space, 2, config, graph_root) # type: ignore
    next = running_rddmin_task.invoke(search_space, config, graph_root, result) # type: ignore
    return (result, next)