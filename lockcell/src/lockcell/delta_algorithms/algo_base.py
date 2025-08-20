from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from pymonik import ResultHandle

from ..utils import StatusClass, Status

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
        self._update_buffer: list[list] = []

    @abstractmethod
    def start(self):
        """
        launches the calculus
        """

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
        Retrieve all the intermediate results that were created by the computation on ArmoniK and if there was some, updates the status to UPDATED (really important)

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
        if self.is_updated():
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

    def _is_ready(self, result: ResultHandle) -> bool:
        """
        _is_ready Helper that check if a 'result' is ready

        Args:
            result (ResultHandle): The result to check

        Returns:
            bool: True if the result is ready
        """
        armonik_result_pointer = self._lockcell._session._results_client.get_result(
            result.result_id
        )
        # TODO: can check for failure or other status to implements in Status (check in armonik's python API (sth like) ~/.../client/.../result.py)
        return armonik_result_pointer.status == 2

    def _update_status(self, status: Status | StatusClass):
        """
        Updates the status with only a Status object, can apply to all derivative classes of StatusClass

        Args:
            status (Status | StatusClass): The new status
        """
        if isinstance(status, Status):
            status = StatusClass(status)
        self._lockcell._job_status.phase = status.phase

    def _add_to_buffer(self, data: list[list]):
        """
        Add data to the buffer to resituate them during the 'get_update()' call, should be used in 'update()'

        Args:
            data (list[list]): The data to add
        """
        self._update_buffer.extend(data)

    def _clear_buffer(self):
        """
        Clean the buffer

        Returns:
            list[list]: The buffer before it was erased
        """
        tmp = self._update_buffer
        self._update_buffer = []
        return tmp
