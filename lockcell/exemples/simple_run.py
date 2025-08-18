import os
from pathlib import Path

os.environ["LOCKCELL_CONFIG"] = str(Path(__file__).parent / "config.yaml")

from lockcell import MultiViz, RDDMIN, TestConfig
import tools

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
    res = RDDMIN(searchspace, tools.RDDMin_print, tools.final_print, config, Viz)

    # Potential graphprint
    if PRINT_GRAPH:
        Viz.aff_all()
