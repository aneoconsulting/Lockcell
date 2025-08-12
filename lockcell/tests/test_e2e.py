import os
from pathlib import Path

os.environ["LOCKCELL_CONFIG"] = str(Path(__file__).parent / "config.yaml")

from lockcell import MultiViz, RDDMIN, TestConfig
from . import tools


def _assert_same_elems(res, expected):
    # set si tu ignores les doublons; sinon Counter
    assert {tuple(x) for x in res} == {tuple(x) for x in expected}


def test_random_default():
    for i in range(3):
        ## For Mock Test
        config = TestConfig(N=2 ** (5 + i))
        config.set_mode("default")

        config.generate_problems((3 + i, 1, 0, 0), (2, 2, 3, 1), (1, 3, 2, 1), non_overlapping=True)

        searchspace = config.generate_search_space()
        print("[INFO] Searchspace generated")

        # Launching RDDMin
        res = RDDMIN(searchspace, tools.say, tools.finalSay, config)
        _assert_same_elems(res, config.Pb)


def test_random_analyse():
    ## For Mock Test
    config = TestConfig(N=2**6)
    config.set_mode("default")

    config.generate_problems((3, 1, 0, 0), (2, 2, 3, 1), (1, 3, 2, 1), non_overlapping=True)

    searchspace = config.generate_search_space()
    print("[INFO] Searchspace generated")

    # Launching RDDMin
    res = RDDMIN(searchspace, tools.say, tools.finalSay, config)
    _assert_same_elems(res, config.Pb)


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
    print("[INFO] Searchspace generated")

    # Launching RDDMin
    res = RDDMIN(searchspace, tools.say, tools.finalSay, config)
    _assert_same_elems(res, config.Pb)


if __name__ == "__main__":
    PRINT_GRAPH = False

    # For potential print
    Viz = MultiViz(active=PRINT_GRAPH)

    ## For Mock Test
    config = TestConfig(N=2**6)
    config.set_mode("Analyse")
    input("press Enter to continue...")

    config.generate_problems((3, 1, 0, 0), (2, 2, 3, 1), (1, 3, 2, 1), non_overlapping=True)

    searchspace = config.generate_search_space()
    print("[INFO] Searchspace generated")

    # Launching RDDMin
    res = RDDMIN(searchspace, tools.say, tools.finalSay, config, Viz)

    # Potential graphprint
    if PRINT_GRAPH:
        Viz.aff_all()
