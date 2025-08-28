from typing import TYPE_CHECKING
from ..Tasks.utils import TaskTag
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
        self._result_per_iteration: list[list[list]] = []
        self._final_result: list[list] = []
        self._link_tag(TaskTag.THROWN)
        self._link_tag(TaskTag.RDDMIN_CHAIN)

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
        if self.is_done:
            return False
        if not self._last_known_iteration:
            raise RuntimeError("Cannot update a result that is not started")

        test = False

        if self._update_tag(TaskTag.THROWN):
            self._update_status(Status.UPDATED)
            test = True

        if self._update_tag(TaskTag.RDDMIN_CHAIN):
            test = True
        return test

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
            self._add_result_to_buffer(intermediate_result.failing_subset_list)
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

    def _flush_metadata_buffers_into_result_buffer(self):
        for thrown in self._metadata_buffers[TaskTag.THROWN]:
            thrown_result: list = self._get_task_result(thrown, tuple)[0][0]
            if not _already_contains(self._final_result, thrown_result):
                self._add_result_to_buffer(thrown_result)
                self._final_result.append(thrown_result)
        self._metadata_buffers[TaskTag.THROWN] = []

        for _ in self._metadata_buffers[TaskTag.RDDMIN_CHAIN]:
            self._next_iteration()
            self._new_step()
        self._metadata_buffers[TaskTag.RDDMIN_CHAIN] = []

    def get_result(self) -> list[list]:
        if not self.is_done:
            raise RuntimeError(
                "get_result can only be used when the result is ready (use the DeltaDebugHandler.done property to verify it)"
            )
        return self._final_result

    def _next_iteration(self):
        if self._last_known_iteration is None:
            raise AttributeError("Cannot retrieve the next_iteration of a non existing result")

        try:
            iteration_result = self._get_result_handle(self._last_known_iteration.iteration_result)
        except RuntimeError as e:
            raise RuntimeError(f"Error while retrieving the last iteration : {e}")

        # TODO: Remove when good implem of Task.py (currently returning a tuple and not a TaskResult)
        iteration_result = TaskResult(*iteration_result)  # type: ignore

        if iteration_result.test_of_delta:
            self._update_status(Status.COMPLETED)
            return
        self._result_per_iteration.append(iteration_result.failing_subset_list)
        if self._last_known_iteration.next is None:
            raise SystemError(
                "Since test of delta is false, there should be a next iteration but it is None"
            )

        self._result_per_iteration.append(iteration_result.failing_subset_list)
        self._last_known_iteration = unfake_result(
            self._last_known_iteration.next.wait().get(), self._lockcell._session
        )
        print(f"\n*** ITERATION {self._lockcell._job_status.step} DONE ***")  # type: ignore
        print("Summary : ", self._result_per_iteration[-1].__str__()[1:-1])

    def _new_step(self):
        self._lockcell._job_status.step += 1  # type: ignore


def _already_contains(all: list[list], item: list):
    for x in all:
        if set(x) == set(item):
            return True
    return False
