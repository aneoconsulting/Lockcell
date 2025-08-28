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
    def __init__(self, lock: "Lockcell", graph_root: Node | None = None):
        super().__init__(lock)
        self._expected_result: ResultHandle[TaskResult] | None = None
        self._result: list[list] = []
        self._graph_root = graph_root
        self._link_tag(TaskTag.THROWN)
        self._link_tag(TaskTag.END_ROOT)

    def start(self):
        options = self._lockcell._session.task_options
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
        if not self.is_done:
            raise RuntimeError(
                "get_result can only be used when the result is ready (use the DeltaDebugHandler.done property to verify it)"
            )
        return self._result


def _already_contains(all: list[list], item: list):
    for x in all:
        if set(x) == set(item):
            return True
    return False
