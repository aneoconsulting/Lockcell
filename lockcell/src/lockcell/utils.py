from enum import Enum, auto
from dataclasses import dataclass

class Phase(Enum):
    NO_JOB = auto()
    JOB_CREATED = auto()
    RUNNING = auto()
    FAILED = auto()
    COMPLETED = auto()

@dataclass
class Status:
    phase: Phase

    def __eq__(self, other):
        if isinstance(other, Phase):
            return self.phase is other
        if isinstance(other, Status):
            return self.phase is other.phase
        return NotImplemented
    
@dataclass
class RDDMinStatus(Status):
    step: int = 0

    def __repr__(self):
        return f"Status(phase={self.phase.name!r}, step={self.step})"

    def __str__(self):
        if self.phase is Phase.RUNNING:
            return f"{self.phase.name} (step {self.step})"
        return self.phase.name