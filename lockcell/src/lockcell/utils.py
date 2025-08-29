from enum import Enum, auto
from dataclasses import dataclass


class Status(Enum):
    NO_JOB = auto()
    JOB_CREATED = auto()
    RUNNING = auto()
    UPDATED = auto()
    FAILED = auto()
    COMPLETED = auto()


@dataclass
class StatusClass:
    """
    A class that wraps Status in order to allow the heritage of status
    It can be compared with a Status without problem

    Attributes:
       phase (Status): The status
    """

    phase: Status

    def __eq__(self, other):
        if isinstance(other, Status):
            return self.phase is other

        if isinstance(other, StatusClass):
            return self.phase is other.phase
        return NotImplemented

    def __str__(self):
        return str(self.phase.name)


@dataclass
class RDDMinStatus(StatusClass):
    """
    RDDMinStatus Status class of RDDMin, can store the step of the computation
    Inherit from StatusClass and can be compared with Status

    Attributes:
        step (int): The step of the algorithm
    """

    step: int = 0

    def __repr__(self):
        return f"Status(phase={self.phase.name!r}, step={self.step})"

    def __str__(self):
        if self.phase is Status.RUNNING or self.phase is Status.UPDATED:
            return f"{self.phase.name} (iteration : {self.step})"
        return str(self.phase.name)

    def __eq__(self, other):
        if isinstance(other, Status):
            return self.phase is other
        if isinstance(other, StatusClass):
            return self.phase is other.phase
        return NotImplemented


def is_running(status: StatusClass) -> bool:
    """
    Asserts if a status is on a running state

    Args:
        status (StatusClass): The status
    """
    return status == Status.RUNNING or status == Status.UPDATED
