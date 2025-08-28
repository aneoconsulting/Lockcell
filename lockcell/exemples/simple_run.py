import os
from pathlib import Path
import time

os.environ["LOCKCELL_CONFIG"] = str(Path(__file__).parent / "config.yaml")

import lockcell
import cloudpickle


from lockcell import MultiViz, Lockcell, TestConfig, Status

cloudpickle.register_pickle_by_value(lockcell)


def _same_elements(res, expected):
    return {tuple(sorted(x)) for x in res} == {tuple(sorted(pb)) for pb, _ in expected}


if __name__ == "__main__":
    PRINT_GRAPH = False

    # For potential print
    Viz = MultiViz(active=PRINT_GRAPH)

    ## For Mock Test
    config = TestConfig(
        N=2**7,
        problems=[
            ([1], 0.3),
            ([8], 0.3),
            ([2, 9], 0.3),
            ([42, 40], 0.5),
            ([118, 114, 115, 127], 0.5),
        ],
    )
    config.set_mode("Analyse")
    input("press Enter to continue...")

    with Lockcell(
        endpoint="172.29.94.180:5001", config=config, environnement={"pip": ["numpy"]}
    ) as lock:
        lock.run_rddmin()
        print("started")
        start = time.time()
        status = lock.get_status()
        while status != Status.COMPLETED:
            if status == Status.UPDATED:
                print(f"\nUpdate at {(time.time() - start):.2f}s ---> {lock.get_update()}")
            lock.update()
            status = lock.get_status()
            time.sleep(0.5)
        print(f"Last update at {(time.time() - start):.2f}s ---> {lock.get_update()}")
        res = lock.get_result()
        print("Full : ", res)
        print(config.Pb)
        print("valid : ", _same_elements(res, config.Pb))

    # Potential graphprint
    if PRINT_GRAPH:
        Viz.aff_all()
