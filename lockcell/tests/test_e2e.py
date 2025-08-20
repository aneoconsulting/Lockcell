import os
from pathlib import Path

os.environ["LOCKCELL_CONFIG"] = str(Path(__file__).parent / "config.yaml")

import cloudpickle
import pytest
import logging

from lockcell import Lockcell, TestConfig

logger = logging.getLogger(__name__)


def _assert_same_elements(res, expected):
    assert {tuple(sorted(x)) for x in res} == {tuple(sorted(pb)) for pb, _ in expected}


def _setup_lockcell():
    import lockcell

    cloudpickle.register_pickle_by_value(lockcell)


@pytest.mark.parametrize(
    "N, one_sized_failing_set, two_sized_failing_set, three_sized_failing_set, mode_ddmin, lockcell_mode",
    [
        (2**5, 2, 2, 1, "default", "rddmin"),
        (2**6, 3, 2, 1, "default", "rddmin"),
        (2**7, 3, 3, 2, "Analyse", "rddmin"),
    ],
)
def test_random(
    N,
    one_sized_failing_set,
    two_sized_failing_set,
    three_sized_failing_set,
    mode_ddmin,
    lockcell_mode,
):
    _setup_lockcell()
    ## For Mock Test
    config = TestConfig(N=N)
    config.set_mode(mode_ddmin)

    config.generate_problems(
        (one_sized_failing_set, 1, 0, 0),
        (two_sized_failing_set, 2, 3, 1),
        (three_sized_failing_set, 3, 2, 1),
        non_overlapping=True,
    )

    search_space = config.generate_search_space()
    logger.debug(f"[INFO] Searchspace generated :\n {search_space}")

    with Lockcell(
        endpoint="172.29.94.180:5001", config=config, environnement={"pip": ["numpy"]}
    ) as lock:
        lock.set_job(lockcell_mode)
        lock.run()
        lock.wait()
        result = lock.get_result()

        logger.info("Found result : " + str(result))
        logger.info("Config result : " + str(config.Pb))
    _assert_same_elements(result, config.Pb)


@pytest.mark.slow
def test_robust():
    ## For Mock Test
    _setup_lockcell()
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

    with Lockcell(
        endpoint="172.29.94.180:5001", config=config, environnement={"pip": ["numpy"]}
    ) as lock:
        lock.run_rddmin()
        lock.wait()
        result = lock.get_result()

        logger.info("Found result : " + str(result))
        logger.info("Config result : " + str(config.Pb))
    _assert_same_elements(result, config.Pb)
