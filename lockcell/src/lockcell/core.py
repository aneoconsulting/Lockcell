"""
Created on : 2025-07-07
Author   : Erwan Tchaleu
Email    : erwan.tchale@gmail.com

"""
from enum import Enum
from copy import copy
from typing import Any
from abc import ABC, abstractmethod

from lockcell.Tasks.Results import RDDMinResult, TaskResult
from pymonik import Pymonik, ResultHandle
from yaml import Node

from .Tasks.Task import nTask
from .Tasks.TaskMaster import running_rddmin_task
from .Tasks.utils import AminusB
from .config.BaseConfig import BaseConfig
from .utils import Phase, Status, RDDMinStatus

class Job(Enum):
    DDMin = "ddmin"
    RDDMIN = "rddmin"   


class Lockcell:

    # Interface for a way to execute Delta Debug (like DDMin, RDDMin, SRDDMin, ...)
    class DeltaDebugHandler(ABC):
        def __init__(self, lock : "Lockcell"):
            self._lockcell = lock
            self._lockcell._status = Status(Phase.JOB_CREATED)
        
        @abstractmethod
        def start(self):
            self._lockcell._status = Status(Phase.RUNNING)

        @abstractmethod
        def update(self) -> Any:
            pass

        @abstractmethod
        def wait(self) -> Any:
            pass

        @property
        def done(self):
            return self._lockcell._job_status == Phase.COMPLETED
        
        @abstractmethod
        def get_result(self) -> list[list]:
            if not self.done:
                raise RuntimeError("get_result can only be used when the result is ready (use the DeltaDebugHandler.done property to verify it)")
        
        def _is_ready(self, result : ResultHandle) -> bool:
            armonik_result_pointer = self._lockcell._session._results_client.get_result(result.result_id)
            return armonik_result_pointer.status == 2

    # Register that makes the correspondence between the jobs and the names
    _JOB_TO_CLASS: dict[Job, type[DeltaDebugHandler]] = {}


    class RDDMin(DeltaDebugHandler):
        def __init__(self, lock : "Lockcell"):
            super().__init__(lock)
            self._lockcell._job_status = RDDMinStatus(Phase.JOB_CREATED)
            self._last_known_iteration : RDDMinResult | None = None
            self._failing_subset : list[list] = []


        def start(self):
            self._last_known_iteration = running_rddmin_task.invoke(self._lockcell._search_space, self._lockcell._config).wait().get() # type: ignore
            self._lockcell._job_status.phase = Phase.RUNNING
            self._lockcell._job_status.step = 1
        
        def update(self) -> list[list[list]]:
            if not self._last_known_iteration:
                raise RuntimeError("Cannot update a result that is not started")
            
            new_results : list[list[list]] = []
            # Can give the impression that we dont take into account the last iteration but actually the last one only asses that the previous one terminated with true testing the global delta so no need to compute it
            while self._last_known_iteration.next is not None:
                if self._is_ready(self._last_known_iteration.iteration_result):

                    # Retrieve the result of the last iteration
                    intermediate_result : TaskResult = self._last_known_iteration.iteration_result.wait().get()
                    new_results.append(intermediate_result.failing_subset_list)
                    self._failing_subset.extend(intermediate_result.failing_subset_list)
                    # sum(list, []) concatenate a list of list of elt to make it a giant list of elt
                    self._lockcell._reduce_search_space(sum(intermediate_result.failing_subset_list, []))

                    # goes to the next iteration
                    self._last_known_iteration = self._last_known_iteration.next.wait().get()
                else:
                    return new_results
            self._lockcell._job_status.phase = Phase.COMPLETED
            return new_results

        def get_result(self) -> list[list]:
            super().get_result()
            return self._failing_subset    

    class DDMin(DeltaDebugHandler):
        def __init__(self, lock: "Lockcell", graph_root : Node  | None = None):
            super().__init__(lock)
            self._expected_result : ResultHandle[TaskResult]
            self._result : list[list] = []
            self._graph_root = graph_root

        def start(self):
            super().start()
            self._expected_result = nTask.invoke(self._lockcell._search_space, 2, self._lockcell._config, self._graph_root, pymonik=self._lockcell._session)

        
        def update(self) -> list[list]:
            if self._is_ready(self._expected_result):
                self._result = self._expected_result.wait().get().failing_subset_list
                self._lockcell._status.phase = Phase.COMPLETED
                return self._result
            return []

        def wait(self):
            self._expected_result.wait()
            print("lol")
            return self
        
        def get_result(self) -> list[list]:
            super().get_result()
            return self._result

    _JOB_TO_CLASS[Job.RDDMIN] = RDDMin
    _JOB_TO_CLASS[Job.DDMin] = DDMin



    def __init__(self, endpoint :str | None, config: BaseConfig, *, partition : str = "pymonik", environnement : dict[str, Any] = {}) -> None:

        # Configuration
        self._endpoint : str | None = endpoint
        self._config : BaseConfig = copy(config)
        self._search_space : list = self._config.generate_search_space()
        self._environnement : dict[str, Any] = environnement

        self._session = Pymonik(endpoint=self._endpoint, partition=partition, environment=self._environnement)

        # Data of the delta Debug
        self._result : list[list] = []
        self._handler : Lockcell.DeltaDebugHandler | None = None
        
        # Status
        self._job_status : Status = Status(Phase.NO_JOB)
        self._open : bool = False

        # Constants
        self.INTERNAL_SP = None
    
    def __del__(self):
        self.close()

    ### User functions

    def run(self):
        if not self._open:
            raise RuntimeError("Cannot run a job on a closed session, please use Lockcell.open() before running anything")
        if self._handler is None:
            raise RuntimeError("Cannot run a job if there is not job, please use Lockcell.run_[JOB_NAME] instead or use Lockcell.set_job before the run call")
        self._handler.start()

    def run_rddmin(self):
        self.set_job(Job.RDDMIN)
        self.run()
    
    def run_ddmin(self):
        self.set_job(Job.DDMin)
        self.run()

    def wait(self):
        print("lol")
        if self._handler is None:
            raise RuntimeError("Cannot wait for the job : no job is running")
        print("lol")
        self._handler.wait()
    
    def set_job(self, job: str | Job) -> None:
        # If a string was passed, transforms it into a Job instance
        if isinstance(job, str):
            key = job.strip().lower()
            for test_job in self._JOB_TO_CLASS:
                if test_job.value == key:
                    job_enum = test_job
                    break
            else:
                valid = ", ".join(self.valid_jobs())
                raise ValueError(f"Unknown Job : {job!r}. Valid job names are : {valid}.")
        elif isinstance(job, Job):
            job_enum = job
        else:
            raise TypeError("job must be a str or a Job.")

        handler_class = self._JOB_TO_CLASS[job_enum]
        self._handler = handler_class(self) 
        self._status = Status(Phase.JOB_CREATED)
    
        
    ### Attribute Manager

    @property
    def config(self) -> BaseConfig:
        return self._config
    
    @property
    def endpoint(self) -> str | None:
        return self._endpoint

    @property
    def search_space(self) -> list:
        return self._search_space  
    
    @property
    def environnement(self) -> dict[str, Any]:
        return self._environnement

    @property
    def is_open(self) -> bool:
        return self._open

    @property
    def is_running(self) -> bool:
        return self._job_status == Phase.RUNNING
    

    @config.setter
    def config(self, config: BaseConfig):
        if self.is_open:
            raise RuntimeError("Please close the current session before trying to change the configuration, use Lockcell.close() (then you can reopen it with Lockcell.open())")
        self._config = copy(config)
        self._search_space = self._config.generate_search_space()
    
    @environnement.setter
    def environnement(self, environnement: dict[str, Any]):
        if self.is_open:
            raise RuntimeError("Please close the current session before trying to change the environnement, use Lockcell.close() (then you can reopen it with Lockcell.open())")
        self._session.environment = environnement
    
    @endpoint.setter
    def endpoint(self, endpoint: str | None):
        if self.is_open:
            raise RuntimeError("Please close the current session before trying to change the endpoint, use Lockcell.close() (then you can reopen it with Lockcell.open())")
        self._session._endpoint = endpoint

    @search_space.setter
    def search_space(self, search_space : list):
        if self.is_open:
            raise RuntimeError("Please close the current session before trying to change the endpoint, use Lockcell.close() (then you can reopen it with Lockcell.open())")
        self._search_space = search_space
        
    # Helpers

    def _reduce_search_space(self, to_subtract : list):
        self._search_space = AminusB(self._search_space, to_subtract)
    

    # To handle PymoniK session
    
    def open(self):
        self._open = True
        self._session.__enter__()

    def close(self):
        self._open = False
        self._session.__exit__(None, None, None)

    
    # For usage with context : with

    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.close()
    
    
    # Class Methods
    
    @classmethod
    def valid_jobs(cls) -> list[str]:
        return [j.value for j in cls._JOB_TO_CLASS.keys()]