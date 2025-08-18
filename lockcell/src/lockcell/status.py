from enum import Enum, auto
from dataclasses import dataclass

class Phase(Enum):
    CREATED = auto()
    RUNNING = auto()
    FAILED = auto()
    COMPLETED = auto()
    
@dataclass
class Status:
    phase: str
    step: int = 0

    def __repr__(self):
        return f"Status(phase={self.phase!r}, step={self.step})"

    def __str__(self):
        if self.phase == "RUNNING":
            return f"{self.phase} (étape {self.step})"
        return self.phase