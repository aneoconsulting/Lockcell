from pymonik import task
from armonik.worker import TaskHandler

from ..constants import LOCKCELL_TAG
from ..config.BaseConfig import BaseConfig
from .Results import FakeRDDMinResult, FakeResult, TaskResult, RDDMinResult, fake_result
from .utils import AminusB, TaskTag
from .Task import nTask

NO_RETURN = FakeResult(0, 0)  # type: ignore


@task(require_context=True, priority=7)
def running_rddmin_task(ctx, search_space: list, config: BaseConfig, previous_result: tuple = None):  # type: ignore
    """
    Allow to make the RDDMin run entirely on ArmoniK
    Retrieve the result of the 'previous_result' of a dd_min run, an the previous 'search_space', reduce the 'search_space' and launch another dd_min with this new 'search_space'.
    Create the same task that takes the result of this dd_min and provides to the user 'ResultHandle's of it's calculation and to the next 'running_ddmin_task'

    Args:
        search_space (list): The previous search_space
        config (BaseConfig): The config used to run the dd_min
        previous_result (tuple, optional): The result of the previous running_rddmin_task. Defaults to None.

    Returns:
        FakeRDDMinResult : to result as said in the description, wrapped in a FakeRDDMinResult to work with cloudpickle
    """
    if previous_result:
        # TODO: to delete as soon as TaskResult will be implemented in Task.py
        previous_result: TaskResult = TaskResult(*previous_result)

        if previous_result.test_of_delta:
            return FakeRDDMinResult(NO_RETURN, None)

        # Does the union of the lists contained in failing_subset_list
        all = sum(previous_result.failing_subset_list, [])
        search_space = AminusB(search_space, all)

    task_handler: TaskHandler = ctx.task_handler
    options = task_handler.task_options
    options.priority = 1
    options.options[LOCKCELL_TAG] = TaskTag.ROOT.value
    result = nTask.invoke(search_space, 2, config, None, task_options=options)  # type: ignore
    options.options[LOCKCELL_TAG] = TaskTag.RDDMIN_CHAIN.value
    options.priority = 7
    next = running_rddmin_task.invoke(search_space, config, result, task_options=options)  # type: ignore
    return fake_result(RDDMinResult(result, next))
