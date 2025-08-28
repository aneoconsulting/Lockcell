import os
from pathlib import Path
import time

os.environ["LOCKCELL_CONFIG"] = str(Path(__file__).parent / "config.yaml")

import lockcell
import cloudpickle


from lockcell import MultiViz, Lockcell, TestConfig, Status

cloudpickle.register_pickle_by_value(lockcell)

if __name__ == "__main__":
    PRINT_GRAPH = False

    # For potential print
    Viz = MultiViz(active=PRINT_GRAPH)

    ## For Mock Test
    config = TestConfig(N=2**6)
    config.set_mode("Analyse")
    input("press Enter to continue...")

    config.generate_problems((3, 1, 0, 0), (2, 2, 3, 1), (1, 3, 2, 1), non_overlapping=True)
    config.add_problem([1, config.N - 1])

    with Lockcell(
        endpoint="172.29.94.180:5001", config=config, environnement={"pip": ["numpy"]}
    ) as lock:
        lock.run_rddmin()
        for i in range(4):
            status = lock.get_status()
            if status == Status.UPDATED:
                print("Update :", lock.get_update())
            if status == Status.COMPLETED:
                print("WoW :", lock.get_update())
                break
            time.sleep(2)
        lock.wait()
        print("Last Update : ", lock.get_update())
        print("Full : ", lock.get_result())
        print(config.Pb)

    # Potential graphprint
    if PRINT_GRAPH:
        Viz.aff_all()
