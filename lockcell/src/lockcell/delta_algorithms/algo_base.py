from __future__ import annotations

import time
import warnings
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING, Type, TypeVar
from grpc._channel import _MultiThreadedRendezvous


from armonik.common import Task
from pymonik import ResultHandle

from ..Tasks.utils import TaskTag
from ..constants import LOCKCELL_TAG
from ..utils import StatusClass, Status
from ..events import TasksFinder


if TYPE_CHECKING:
    from ..core import Lockcell


# Interface for a way to execute Delta Debug (like DDMin, RDDMin, SRDDMin, ...)
class DeltaDebugHandler(ABC):
    """
    Handles the process of a way to perform DDMin (like DDMin, RDDMin, SRDDMin)
    Is an Interface, not implementable, must be seen as a part of lockcell, it will interact with it's attributes (especially '_job_status')
    """

    def __init__(self, lock: "Lockcell"):
        self._lockcell = lock
        self._lockcell._job_status = StatusClass(Status.JOB_CREATED)
        self._result_buffer: list[list] = []

        self._metadata_buffers: dict[TaskTag, list[Task]] = {}
        self._tag_finder: dict[TaskTag, TasksFinder] = {}

    @abstractmethod
    def start(self):
        """
        launches the calculus
        """

    @property
    def is_updated(self) -> bool:
        """
        Asserts if the calculus has updated since the last verification, or if it is completed

        Returns:
            bool: True if status is UPDATED or COMPLETED
        """
        return self._lockcell._job_status == Status.UPDATED or self.is_done

    @abstractmethod
    def update(self) -> bool:
        """
        Retrieve all the intermediate results that were created by the computation on ArmoniK and if there was some, updates the status to UPDATED

        Returns:
            bool: True if it updated things (status can be UPDATED before the call, if nothing was found on that call, will return False)
        """
        pass

    def get_update(self) -> list[list]:
        """
        Return the new updates found by update, set the status to running if it isn't COMPLETED

        Returns:
            list[list]: the updates
        """
        self._flush_metadata_buffers_into_result_buffer()
        if self.is_updated:
            if not self.is_done:
                self._update_status(Status.RUNNING)
            return self._clear_buffer()
        return []

    @property
    def is_done(self):
        return self._lockcell._job_status == Status.COMPLETED

    @abstractmethod
    def wait(self) -> Any:
        """
        Can be called to wait for the end of the computation

        Raises:
            RuntimeError: If the calculation isn't running or completed (if it is FAILED or JOB_CREATED for example)

        Returns:
            Any: self
        """

    @abstractmethod
    def get_result(self) -> list[list]:
        """
        To call when the computation is done, provides the final result

        Raises:
            RuntimeError: If the result isn't ready

        Returns:
            list[list]: The result of the computation
        """

    # Helpers

    T = TypeVar("T")

    def _get_task_result(self, task: Task, cast_type: Type[T] = object) -> T:
        if not task.expected_output_ids:
            raise ValueError("Tried to get the result of task that doesn't produce a result")
        raw_result = self._get_result_handle(
            ResultHandle(
                task.expected_output_ids[0],
                self._lockcell._session._session_id,
                self._lockcell._session,
            )
        )
        if not isinstance(raw_result, cast_type):
            raise TypeError(f"Expected {cast_type}, got {type(raw_result)}")

        return raw_result

    MAX_TRY = 5

    def _get_result_handle(self, to_get: ResultHandle, max_try=MAX_TRY):
        raw_result = None
        for counter in range(max_try):
            try:
                start = time.time()
                raw_result = to_get.wait().get()
                stop = time.time()
                if counter != 0:
                    warnings.warn(
                        RuntimeWarning(
                            f"Result retrieving failed {counter} times, duration of the retrieving phase {stop - start}s, it might be a wrong usage of the function"
                        )
                    )
                break
            except _MultiThreadedRendezvous as e:
                if counter == max_try - 1:
                    raise RuntimeError(f"Error while retrieving task result : {e}")
                else:
                    time.sleep(2)
                    continue
        return raw_result

    def _update_status(self, status: Status | StatusClass):
        """
        Updates the status with only a Status object, can apply to all derivative classes of StatusClass

        Args:
            status (Status | StatusClass): The new status
        """
        if isinstance(status, Status):
            status = StatusClass(status)
        self._lockcell._job_status.phase = status.phase

    @abstractmethod
    def _flush_metadata_buffers_into_result_buffer(self):
        """
        This method makes the link between the metadata buffer that only contains a pointer towards the result and the result buffer that actually contains the results

        It should download the results pointed by the metadata (from every metadata buffer), put them in the result buffer and flush the metadata buffers (really important)s
        """
        pass

    # Tag result helpers

    def _link_tag(self, tag: TaskTag):
        if tag not in self._tag_finder:
            self._tag_finder[tag] = TasksFinder(
                self._lockcell._session._endpoint,
                self._lockcell._session._session_id,
                Task.options[LOCKCELL_TAG] == tag.value,
            )  # type: ignore
            self._metadata_buffers[tag] = []  # initialize buffer for this tag

    def _update_tag(self, tag: TaskTag):
        if tag not in self._tag_finder:
            raise ValueError(f"tag : {tag}, is not linked, cannot search for it")
        news = self._tag_finder[tag].update()
        if news:
            self._update_status(Status.UPDATED)
            self._add_metadata(tag, news)
            return True
        return False

    def _add_metadata(self, tag: TaskTag, data: list[Task]):
        if tag not in self._tag_finder:
            raise ValueError(f"tag : {tag}, is not linked, cannot add metadata for it")
        self._metadata_buffers[tag].extend(data)

    # Result buffer helpers

    def _add_result_to_buffer(self, data: list):
        """
        Add data to the buffer to resituate them during the 'get_update()' call, should be used in 'update()'

        Args:
            data (list[list]): The data to add
        """
        self._result_buffer.append(data)

    def _clear_buffer(self):
        """
        Clean the buffer

        Returns:
            list[list]: The buffer before it was erased
        """
        tmp = self._result_buffer
        self._result_buffer = []
        return tmp
