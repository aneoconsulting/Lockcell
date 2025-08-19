from pymonik import task

from ..config.BaseConfig import BaseConfig
from .Results import TaskResult, RDDMinResult
from .utils import AminusB
from .Task import nTask

@task(require_context=True)
def running_rddmin_task(ctx, search_space : list, config : BaseConfig, previous_result : tuple = None): # type: ignore

    ctx.logger.info("test")
    if previous_result:
        # to delete as soon as TaskResult will be implemented in Task.py
        previous_result :TaskResult = TaskResult(*previous_result)

        if previous_result.test_of_delta:
            return RDDMinResult(previous_result, None)

        # Does the union of the lists contained in failing_subset_list
        all = sum(previous_result.failing_subset_list , [])
        search_space = AminusB(search_space, all)

    result = nTask.invoke(search_space, 2, config, None) # type: ignore
    next = running_rddmin_task.invoke(search_space, config, result) # type: ignore
    return RDDMinResult(result, next)