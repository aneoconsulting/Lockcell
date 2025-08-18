import os
from pathlib import Path

os.environ["LOCKCELL_CONFIG"] = str(Path(__file__).parent / "config.yaml")

import pytest
import logging

from lockcell import RDDMIN, TestConfig
import tools

logger = logging.getLogger(__name__)


def _assert_same_elems(res, expected):
    assert {tuple(sorted(x)) for x in res} == {tuple(sorted(pb)) for pb, _ in expected}


def _print_step_through_logger(result: list[list], iteration_number: int):
    logger.info(tools.RDDMin_print(result, iteration_number))


def _print_final_through_logger(result: list[list], iteration_number: int):
    logger.info(tools.final_print(result, iteration_number))


@pytest.mark.parametrize(
    "N, one_sized_failing_set, two_sized_failing_set, three_sized_failing_set, mode",
    [
        (2**5, 2, 2, 1, "default"),
        (2**6, 3, 2, 1, "default"),
        (2**7, 3, 3, 2, "default"),
        (2**7, 3, 3, 2, "Analyse"),
    ],
)
def test_random(
    N,
    one_sized_failing_set,
    two_sized_failing_set,
    three_sized_failing_set,
    mode,
):
    ## For Mock Test
    config = TestConfig(N=N)
    config.set_mode(mode)

    config.generate_problems(
        (one_sized_failing_set, 1, 0, 0),
        (two_sized_failing_set, 2, 3, 1),
        (three_sized_failing_set, 3, 2, 1),
        non_overlapping=True,
    )

    searchspace = config.generate_search_space()
    logger.debug(f"[INFO] Searchspace generated :\n {searchspace}")

    # Launching RDDMin
    res = RDDMIN(
        searchspace=searchspace,
        func=_print_step_through_logger,
        finalfunc=_print_final_through_logger,
        config=config,
    )
    print(res)
    print(config.Pb)
    _assert_same_elems(res[0], config.Pb)


@pytest.mark.slow
def test_robust():
    ## For Mock Test
    # Specific problem set that makes the Analyser sweat lol
    config = TestConfig(
        N=2**7,
        problems=[
            ([56], 0.3),
            ([94], 0.3),
            ([42, 40], 0.5),
            ([118, 114, 115], 0.5),
            ([76, 80, 78, 82], 0.5),
        ],
    )
    config.set_mode("Analyse")

    searchspace = config.generate_search_space()
    logger.debug(f"[INFO] Searchspace generated :\n {searchspace}")

    # Launching RDDMin
    result = RDDMIN(
        searchspace=searchspace,
        func=_print_step_through_logger,
        finalfunc=_print_final_through_logger,
        config=config,
    )
    _assert_same_elems(result[0], config.Pb)
