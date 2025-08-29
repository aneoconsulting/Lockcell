import time
from typing import Iterable, List, Tuple
from lockcell import TestConfig
import copy


class BenchConfig(TestConfig):
    def __init__(
        self,
        N: int,
        problems: List[Tuple[List[int], float]] | None = None,
        nbRun: int | None = None,
        waiting_time_in_second: float = 0,
    ):
        super().__init__(N, problems, nbRun)
        self._waiting_time_in_second: float = waiting_time_in_second

    def test_(self, subspace: Iterable[int]) -> bool:
        time.sleep(self._waiting_time_in_second)
        return super().test_(subspace)

    def __copy__(self) -> "BenchConfig":
        """
        Shallow configuration copy (problems are deep-copied to remain independent).

        Returns:
            TestConfig: A new config instance with the same N/nbRun/problems.
        """
        copy_ = BenchConfig(
            N=self.N,
            problems=copy.deepcopy(self.Pb),
            nbRun=self.nbRun,
            waiting_time_in_second=self._waiting_time_in_second,
        )
        copy_.mode = self.mode
        return copy_
