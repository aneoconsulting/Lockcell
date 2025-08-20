from typing import TYPE_CHECKING

from pymonik import ResultHandle

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

    def start(self):
        super().start()
        self._expected_result = nTask.invoke(  # type: ignore
            self._lockcell._search_space,
            2,
            self._lockcell._config,
            self._graph_root,
            pymonik=self._lockcell._session,
        )
        self._update_status(Status.RUNNING)

    def update(self) -> bool:
        if not self._expected_result:
            raise RuntimeError("Cannot update a result that is not started")
        if (
            self._is_ready(self._expected_result)
            and not self._lockcell._job_status == Status.COMPLETED
        ):
            self._result = self._expected_result.get()[0]  # type: ignore
            self._lockcell._job_status.phase = Status.COMPLETED
            self._add_to_buffer(self._expected_result.get()[0])  # type: ignore
            self._update_status(Status.COMPLETED)
            return True
        return False

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

    def get_result(self) -> list[list]:
        if not self.is_done:
            raise RuntimeError(
                "get_result can only be used when the result is ready (use the DeltaDebugHandler.done property to verify it)"
            )
        return self._result
