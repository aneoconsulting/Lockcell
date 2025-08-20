from typing import TYPE_CHECKING

from ..utils import Status, RDDMinStatus, is_running
from ..Tasks.Results import RDDMinResult, unfake_result, TaskResult
from ..Tasks.TaskMaster import running_rddmin_task
from .algo_base import DeltaDebugHandler

if TYPE_CHECKING:
    from ..core import Lockcell


class RDDMin(DeltaDebugHandler):
    def __init__(self, lock: "Lockcell"):
        super().__init__(lock)
        self._lockcell._job_status = RDDMinStatus(Status.JOB_CREATED, step=0)
        self._last_known_iteration: RDDMinResult | None = None
        self._final_result: list[list] = []

    def start(self):
        self._last_known_iteration = unfake_result(
            running_rddmin_task.invoke(  # type: ignore
                self._lockcell._search_space,
                self._lockcell._config,
                pymonik=self._lockcell._session,
            )
            .wait()
            .get(),
            self._lockcell._session,
        )
        self._update_status(Status.RUNNING)
        self._new_step()

    def update(self) -> bool:
        if not self._last_known_iteration:
            raise RuntimeError("Cannot update a result that is not started")

        # Can give the impression that we dont take into account the last iteration but actually the last one only asses that the previous one terminated with true testing the global delta so no need to compute it
        while self._last_known_iteration.next is not None:
            if self._is_ready(self._last_known_iteration.iteration_result):
                # Retrieve the result of the last iteration
                intermediate_result: TaskResult = (
                    self._last_known_iteration.iteration_result.wait().get()
                )
                # TODO: Remove when good implem of Task.py (currently returning a tuple and not a TaskResult)
                intermediate_result = TaskResult(*intermediate_result)  # type: ignore

                # Add it to the buffer (for update), the final result, and updates the lockcell search_space
                self._add_to_buffer(intermediate_result.failing_subset_list)
                self._final_result.extend(intermediate_result.failing_subset_list)
                # sum(list, []) concatenate a list of list of elt to make it a giant list of elt
                self._lockcell._reduce_search_space(
                    sum(intermediate_result.failing_subset_list, [])
                )

                # goes to the next iteration
                self._last_known_iteration = unfake_result(
                    self._last_known_iteration.next.wait().get(), self._lockcell._session
                )
                self._update_status(Status.UPDATED)
                self._new_step()
            else:
                return super().is_updated()

        self._update_status(Status.COMPLETED)
        return super().is_updated()

    def wait(self):
        if not (is_running(self._lockcell._job_status) or self.is_done):
            raise RuntimeError(
                f"Tried to wait for a result with {self._lockcell._job_status} status"
            )

        if self._last_known_iteration is None:
            raise AttributeError("Tried to wait for a non existing result")

        # Can give the impression that we dont take into account the last iteration but actually the last one only asses that the previous one terminated with true testing the global delta so no need to compute it
        while self._last_known_iteration.next is not None:
            # Wait for the result of the last iteration
            intermediate_result: TaskResult = (
                self._last_known_iteration.iteration_result.wait().get()
            )
            # TODO: Remove when good implem of Task.py (currently returning a tuple and not a TaskResult)
            intermediate_result = TaskResult(*intermediate_result)  # type: ignore

            # Add it to the buffer (for update), the final result, and updates the lockcell search_space
            self._add_to_buffer(intermediate_result.failing_subset_list)
            self._final_result.extend(intermediate_result.failing_subset_list)
            # sum(list, []) concatenate a list of list of elt to make it a giant list of elt
            self._lockcell._reduce_search_space(sum(intermediate_result.failing_subset_list, []))

            # goes to the next iteration
            self._last_known_iteration = unfake_result(
                self._last_known_iteration.next.wait().get(), self._lockcell._session
            )
            self._update_status(Status.UPDATED)
            self._new_step()
        self._update_status(Status.COMPLETED)
        return self

    def get_result(self) -> list[list]:
        if not self.is_done:
            raise RuntimeError(
                "get_result can only be used when the result is ready (use the DeltaDebugHandler.done property to verify it)"
            )
        return self._final_result

    def _new_step(self):
        self._lockcell._job_status.step += 1  # type: ignore
