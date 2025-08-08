from __future__ import annotations

from typing import List, Tuple, Optional, Iterable
from .BaseConfig import BaseConfig
import copy
import random


class TestConfig(BaseConfig):
    """
    Configuration for tests over a finite integer search space [0, N).

    The configuration maintains a list of “problem” subsets `Pb`. Each element of `Pb`
    is a tuple `(subset, p)` where:
        - `subset` is a list[int] describing a minimal failing subset,
        - `p` is an optional probability/weight (float) attached to that subset.

    A test succeeds (returns True) iff the provided `subspace` does NOT fully contain
    any of the configured failing subsets. If it fully contains at least one of them,
    the test fails (returns False).
    """

    def __init__(
        self,
        N: int,
        problems: Optional[List[Tuple[List[int], float]]] = None,
        nbRun: Optional[int] = None,
    ):
        """
        Args:
            N: Size of the integer search space (the space is range(0, N)).
            problems: Optional initial failing subsets as (subset, p).
            nbRun: Number of runs to perform (passed through to BaseConfig).
        """
        super().__init__(nbRun=nbRun)
        if not isinstance(N, int) or N <= 0:
            raise ValueError("N must be a positive integer.")
        self.N: int = N
        self.Pb: List[Tuple[List[int], float]] = []

        if problems:
            self.Pb = copy.deepcopy(problems)

    # ------------------------
    # BaseConfig API
    # ------------------------

    def generate_search_space(self) -> list:
        """
        Return the full integer search space as a list of indices.

        Returns:
            list[int]: [0, 1, 2, ..., N-1]
        """
        return list(range(self.N))

    def test_(self, subspace: Iterable[int]) -> bool:
        """
        Evaluate whether `subspace` passes the test.

        The test fails (returns False) if `subspace` fully contains any configured
        failing subset from `self.Pb`. Otherwise it passes (returns True).

        Args:
            subspace: An iterable of indices proposed as a candidate subset.

        Returns:
            bool: True if the test passes; False if it fails.
        """
        # Convert once for membership tests.
        subspace_set = set(subspace)
        for failing_subset, _p in self.Pb:  # Probability yet not implemented
            if _contains_all(subspace_set, failing_subset):
                return False
        return True

    def __copy__(self) -> "TestConfig":
        """
        Shallow configuration copy (problems are deep-copied to remain independent).

        Returns:
            TestConfig: A new config instance with the same N/nbRun/problems.
        """
        copy_ = TestConfig(
            N=self.N,
            problems=copy.deepcopy(self.Pb),
            nbRun=self.nbRun,
        )
        copy_.mode = self.mode
        return copy_

    # ------------------------
    # Problem generation
    # ------------------------

    def clear_problems(self) -> "TestConfig":
        """
        Remove all configured failing subsets.
        """
        self.Pb.clear()
        return self

    def add_problem(self, subset: Iterable[int], p: float = 1.0) -> "TestConfig":
        """
        Add a single failing subset.

        Args:
            subset: Iterable of indices (will be stored as a sorted unique list).
            p: Optional weight/probability attached to the subset.

        Raises:
            ValueError: If any index is out of bounds.
        """
        normalized = _normalize_subset(subset, self.N)
        self.Pb.append((normalized, float(p)))
        return self

    def generate_problems(
        self,
        *groups: Tuple[int, int, float, float],
        non_overlapping: bool = True,
        seed: int | None = None,
    ) -> "TestConfig":
        """
        Generate failing subsets according to group specifications.

        Each group is a tuple: (count, size, sigma, p)
            - count (int): how many subsets to generate in this group.
            - size  (int): size of each subset to generate.
            - sigma (float): spread parameter; higher means "less clustered".
            - p     (float): weight/probability associated to each generated subset.

        If `non_overlapping` is True (default), subsets are sampled without overlap across
        all generated subsets (i.e., elements are drawn without replacement from the remaining pool).
        If there aren’t enough remaining elements to satisfy a group, a ValueError is raised.

        If `non_overlapping` is False, subsets are generated from the full space; elements
        may repeat across different subsets (but not within a single subset).

        Args:
            *groups: One or more (count, size, sigma, p) tuples.
            non_overlapping: Enforce disjointness between generated subsets.
            seed: Optional RNG seed for reproducibility.

        Raises:
            ValueError: If parameters are inconsistent or space is insufficient.

        Returns:
            TestConfig: self (for chaining).
        """
        if seed is not None:
            random.seed(seed)

        # Copy a pool of available indices if we activate disjointness.
        pool: List[int] = list(range(self.N))

        for idx, (count, size, sigma, p) in enumerate(groups, start=1):
            if not (isinstance(count, int) and count > 0):
                raise ValueError(f"group {idx}: count must be a positive integer")
            if not (isinstance(size, int) and 0 < size <= self.N):
                raise ValueError(f"group {idx}: size must be in [1, N]")
            if sigma < 0:
                raise ValueError(f"group {idx}: sigma must be >= 0")

            for _ in range(count):
                if non_overlapping:
                    # Draw a subset without replacing elements back into the pool.
                    if len(pool) < size:
                        raise ValueError(
                            f"Not enough elements remaining to generate a size-{size} subset "
                            f"(pool={len(pool)})."
                        )
                    subset = _gen_clustered_subset_from_pool(pool, size, sigma)
                else:
                    subset = _gen_clustered_subset(range(self.N), size, sigma)

                self.Pb.append((sorted(subset), float(p)))

        return self


# ------------------------
# Helpers
# ------------------------


def _contains_all(container_set: set[int], subset_list: List[int]) -> bool:
    """Return True if all elements of subset_list are in container_set."""
    for x in subset_list:
        if x not in container_set:
            return False
    return True


def _normalize_subset(subset: Iterable[int], N: int) -> List[int]:
    """Sort, deduplicate, and validate subset against [0, N)."""
    s = sorted(set(int(x) for x in subset))
    for x in s:
        if x < 0 or x >= N:
            raise ValueError(f"Index out of bounds in subset: {x} (N={N})")
    return s


def _gen_clustered_subset_from_pool(pool: List[int], size: int, sigma: float) -> List[int]:
    """
    Generate a subset by drawing from a mutable pool (elements removed once chosen).
    The subset is “clustered” around a random center; sigma controls spread.
    """
    # Choose a center by index in the pool
    if not pool:
        raise ValueError("Empty pool")
    center_idx = random.randrange(len(pool))
    center = pool.pop(center_idx)
    chosen = [center]

    # Walk around the center using normal steps; pick nearest available items.
    while len(chosen) < size:
        step = 0 if sigma == 0 else int(round(random.gauss(mu=0.0, sigma=sigma)))
        # propose a candidate in absolute value space by "moving" from center
        candidate = center + step

        # If candidate not in pool, find the closest available neighbor
        if candidate in pool:
            pool.remove(candidate)
            chosen.append(candidate)
        else:
            # binary expansion around candidate to find nearest free point
            offset = 1
            found = False
            while not found:
                up = candidate + offset
                down = candidate - offset
                picked = None
                if down in pool:
                    picked = down
                elif up in pool:
                    picked = up
                elif down < 0 and up > (pool[-1] if pool else candidate):
                    # If we've clearly exhausted search corridor, fallback to random
                    raise ValueError("Pool exhausted unexpectedly.")

                if picked is not None:
                    pool.remove(picked)
                    chosen.append(picked)
                    found = True
                else:
                    offset += 1

    return chosen


def _gen_clustered_subset(space: Iterable[int], size: int, sigma: float) -> List[int]:
    """
    Generate a subset of given size from an immutable space (with replacement across subsets).
    No element repeats within the subset. Clustering controlled by sigma.
    """
    space_list = list(space)
    if size > len(space_list):
        raise ValueError(
            f"Cannot generate subset of size {size} from space of size {len(space_list)}"
        )

    # Pick a random center
    center = random.choice(space_list)
    chosen = {center}

    while len(chosen) < size:
        step = 0 if sigma == 0 else int(round(random.gauss(mu=0.0, sigma=sigma)))
        candidate = center + step
        # Clamp to space bounds and pick nearest in-space value
        if candidate in space_list:
            chosen.add(candidate)
        else:
            # nearest fallback
            nearest = min(space_list, key=lambda v: abs(v - candidate))
            chosen.add(nearest)

    return sorted(chosen)
