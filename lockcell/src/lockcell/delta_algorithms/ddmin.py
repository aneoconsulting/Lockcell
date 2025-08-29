from typing import TYPE_CHECKING

from ..Tasks.utils import TaskTag
from pymonik import ResultHandle

from ..constants import LOCKCELL_TAG
from .algo_base import DeltaDebugHandler
from ..utils import Status, is_running
from ..graph import Node
from ..Tasks.Task import nTask
from ..Tasks.Results import TaskResult


if TYPE_CHECKING:
    from ..core import Lockcell


class DDMin(DeltaDebugHandler):
    """
    Delta Debugging Minimization (DDMin) algorithm implementation for Lockcell.

    Delta Debugging Minimization is a handler for delta debugging tasks in the Lockcell framework.
    It manages the execution, update, and result collection for delta debugging jobs, using task tags and result buffers.

    Args:
        lock (Lockcell): The Lockcell instance to operate on.
        graph_root (Node | None): Optional root node for the graph.
    """

    def __init__(self, lock: "Lockcell", graph_root: Node | None = None):
        super().__init__(lock)
        self._expected_result: ResultHandle[TaskResult] | None = None
        self._result: list[list] = []
        self._graph_root = graph_root
        self._link_tag(TaskTag.THROWN)
        self._link_tag(TaskTag.END_ROOT)

    def start(self):
        """
        Start the DDMin process by invoking the root task and updating the status.
        """
        options = self._lockcell._session.task_options
        options.options = options.options.copy()
        options.options[LOCKCELL_TAG] = TaskTag.ROOT.value

        self._expected_result = nTask.invoke(  # type: ignore
            self._lockcell._search_space,
            2,
            self._lockcell._config,
            self._graph_root,
            pymonik=self._lockcell._session,
            task_options=options,
        )
        self._update_status(Status.RUNNING)

    def update(self) -> bool:
        """
        Check for linked tags, retrieve associated tasks and put their metadata in the different buffers
        Also updates the status

        Raises:
            RuntimeError: If the computation is not started

        Returns:
            bool: _description_
        """
        if self.is_done:
            return False
        if not self._expected_result:
            raise RuntimeError("Cannot update a result that is not started")

        test = False
        if self._update_tag(TaskTag.THROWN):
            self._update_status(Status.UPDATED)
            test = True

        if self._update_tag(TaskTag.END_ROOT):
            self._update_status(Status.COMPLETED)
            test = True
        return test

    def wait(self):
        """
        Wait for the expected result to complete, updating the status accordingly.
        Raises:
            RuntimeError: If the job status is not running or done.
            AttributeError: If no expected result exists.
        Returns:
            self
        """
        # TODO: rewrite it using Armonik Event python API
        if not (is_running(self._lockcell._job_status) or self.is_done):
            raise RuntimeError(
                f"Tried to wait for a result with {self._lockcell._job_status} status"
            )
        if not self._expected_result:
            raise AttributeError("Tried to wait for a non existing result")
        self._expected_result.wait()
        self._update_status(Status.COMPLETED)
        return self

    def _flush_metadata_buffers_into_result_buffer(self):
        """
        Retrieve the result associated to metadata from the tag buffers and put them into the main result buffer, avoiding duplicates.
        """
        for thrown in self._metadata_buffers[TaskTag.THROWN]:
            thrown_result: list = self._get_task_result(thrown, list)
            if not _already_contains(self._result, thrown_result):
                self._add_result_to_buffer(thrown_result)
                self._result.append(thrown_result)
        self._metadata_buffers[TaskTag.THROWN] = []

        for root in self._metadata_buffers[TaskTag.END_ROOT]:
            root_result: tuple[list[list], bool] = self._get_task_result(root, tuple)

            # TODO: Remove when good implem of Task.py (currently returning a tuple and not a TaskResult)
            root_result_bis: TaskResult = TaskResult(*root_result)  # type: ignore

            for failing_set in root_result_bis.failing_subset_list:
                if not _already_contains(self._result, failing_set):
                    self._add_result_to_buffer(failing_set)
                    self._result.append(failing_set)
        self._metadata_buffers[TaskTag.END_ROOT] = []

    def get_result(self) -> list[list]:
        """
        Get the result of the DDMin process.
        Raises:
            RuntimeError: If the result is not ready.
        Returns:
            list[list]: The minimized failing subsets.
        """
        if not self.is_done:
            raise RuntimeError(
                "get_result can only be used when the result is ready (use the DeltaDebugHandler.done property to verify it)"
            )
        return self._result


def _already_contains(all: list[list], item: list):
    """
    Checks if 'item' is already present in 'all', comparing as sets.
    Args:
        all (list[list]): The list of lists to check in.
        item (list): The item to check for.
    Returns:
        bool: True if item is present, False otherwise.
    """
    item_set = set(item)
    for x in all:
        if set(x) == item_set:
            return True
    return False
