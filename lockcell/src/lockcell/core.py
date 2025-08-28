from enum import Enum
from copy import copy
from typing import Any

from pymonik import Pymonik

from .delta_algorithms import DeltaDebugHandler, RDDMin, DDMin
from .Tasks.utils import AminusB
from .config.BaseConfig import BaseConfig
from .utils import Status, StatusClass


class Job(Enum):
    DDMin = "ddmin"
    RDDMIN = "rddmin"


class Lockcell:
    # Register that makes the correspondence between the jobs and the names
    _JOB_TO_CLASS: dict[Job, type[DeltaDebugHandler]] = {}

    _JOB_TO_CLASS[Job.RDDMIN] = RDDMin
    _JOB_TO_CLASS[Job.DDMin] = DDMin

    def __init__(
        self,
        endpoint: str | None,
        *,
        config: BaseConfig,
        partition: str = "pymonik",
        environnement: dict[str, Any] = {},
    ) -> None:
        # Configuration
        self._endpoint: str | None = endpoint
        self._config: BaseConfig = copy(config)
        self._search_space: list = self._config.generate_search_space()
        self._environnement: dict[str, Any] = environnement

        self._session = Pymonik(
            endpoint=self._endpoint, partition=partition, environment=self._environnement
        )

        # Data of the delta Debug
        self._result: list[list] = []
        self._handler: DeltaDebugHandler | None = None

        # Status
        self._job_status: StatusClass = StatusClass(Status.NO_JOB)
        self._open: bool = False

        # Constants
        self.INTERNAL_SP = None

    def __del__(self):
        self.close()

    ### User functions

    def run(self):
        """
        Launch a run

        Raises:
            RuntimeError: If the session is not open
            RuntimeError: If there is no job to run
        """
        if not self._open:
            raise RuntimeError(
                "Cannot run a job on a closed session, please use Lockcell.open() before running anything"
            )
        if self._handler is None:
            raise RuntimeError(
                "Cannot run a job if there is not job, please use Lockcell.run_[JOB_NAME] instead or use Lockcell.set_job before the run call"
            )
        self._handler.start()

    def run_rddmin(self):
        """
        Shortcut to run a rddmin
        """
        self.set_job(Job.RDDMIN)
        self.run()

    def run_ddmin(self):
        """
        Shortcut to run a ddmin
        """
        self.set_job(Job.DDMin)
        self.run()

    def wait(self):
        """
        Wait until the end of the calculation

        Raises:
            RuntimeError: If there is no job to wait to
        """
        if self._handler is None:
            raise RuntimeError("Cannot wait for the job : no job is running")
        self._handler.wait()

    def _update(self) -> bool:
        """
        Check for updates in calculus in Armonik

        Raises:
            RuntimeError: If there is no running job

        Returns:
            bool: If it found new updates
        """
        if self._handler is None:
            raise RuntimeError("Cannot update the job : no job is running")
        return self._handler.update()

    def get_update(self) -> list[list]:
        """
        Checks for updates, retrieves and returns them

        Raises:
            RuntimeError: If there is no job running

        Returns:
            list[list]: The new updates ([] if no updates)
        """
        if self._handler is None:
            raise RuntimeError("Cannot get the update of the job : no job is running")
        self._update()
        return self._handler.get_update()

    def get_status(self):
        """
        Check for updates on pymonik, updates the status, and returns it

        Returns:
            StatusClass : The status after updates
        """
        self._update()
        return self._job_status

    def get_result(self):
        """
        Check for updates in armoniK, if the computation if completed after that, returns it

        Raises:
            RuntimeError: If there is no job running
            RuntimeError: If the computation isn't ready

        Returns:
            list[list]: The result of the total computation
        """
        if self._handler is None:
            raise RuntimeError("Cannot retrieve a result from a job if there is not job")
        if not self._handler.is_done:
            self._update()
            if not self._handler.is_done:
                raise RuntimeError("Tried to retrieve the result when is wasn't ready")
        return self._handler.get_result()

    def set_job(self, job: str | Job) -> None:
        """
        Sets a DeltaDebugHandler as a job, takes a job name as parameter

        Args:
            job (str | Job): a job name (represents a job, like Job.RDDMIN or "rddmin")

        Raises:
            ValueError: If the job name passed in argument doesn't match any implemented job
            TypeError: If the argument is neither a str nor a Job
        """
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
        return self._job_status == Status.RUNNING

    @config.setter
    def config(self, config: BaseConfig):
        if self.is_open:
            raise RuntimeError(
                "Please close the current session before trying to change the configuration, use Lockcell.close() (then you can reopen it with Lockcell.open())"
            )
        self._config = copy(config)
        self._search_space = self._config.generate_search_space()

    @environnement.setter
    def environnement(self, environnement: dict[str, Any]):
        if self.is_open:
            raise RuntimeError(
                "Please close the current session before trying to change the environnement, use Lockcell.close() (then you can reopen it with Lockcell.open())"
            )
        self._session.environment = environnement

    @endpoint.setter
    def endpoint(self, endpoint: str | None):
        if self.is_open:
            raise RuntimeError(
                "Please close the current session before trying to change the endpoint, use Lockcell.close() (then you can reopen it with Lockcell.open())"
            )
        self._session._endpoint = endpoint

    @search_space.setter
    def search_space(self, search_space: list):
        if self.is_open:
            raise RuntimeError(
                "Please close the current session before trying to change the endpoint, use Lockcell.close() (then you can reopen it with Lockcell.open())"
            )
        self._search_space = search_space

    # Helpers

    def _reduce_search_space(self, to_subtract: list):
        self._search_space = AminusB(self._search_space, to_subtract)

    # To handle PymoniK session

    def open(self):
        """
        Open the PymoniK session
        """
        self._open = True
        self._session = self._session.create()

    def close(self):
        """
        Close the PymoniK session
        """
        self._open = False
        self._session.close()

    # For usage with context : with

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    # Class Methods

    @classmethod
    def valid_jobs(cls) -> list[str]:
        """
        valid_jobs returns a list of str job names that are valid

        Returns:
            list[str]: _description_
        """
        return [j.value for j in cls._JOB_TO_CLASS.keys()]
