import os
from pathlib import Path
import time

os.environ["LOCKCELL_CONFIG"] = str(Path(__file__).parent / "config.yaml")

import pickle
import lockcell
import cloudpickle


from lockcell import Lockcell, Status
from config import BenchConfig
import config

cloudpickle.register_pickle_by_value(lockcell)
cloudpickle.register_pickle_by_value(config)


def load_records_with_source(pkl_path: str | Path, source: str) -> list:
    """
    Charge un fichier contenant une suite de pickle.dump([size, problem, waiting_time, execution_time], f)
    et ajoute un 5e champ '_from' = source ('verrou' ou 'lockcell').
    """
    out = []
    p = Path(pkl_path)
    if not p.exists():
        return out

    with p.open("rb") as f:
        while True:
            try:
                rec = pickle.load(f)  # CHARGER UNE SEULE FOIS
            except EOFError:
                break

            # accepter list ou tuple
            if isinstance(rec, (list, tuple)):
                n = len(rec)
                if n >= 4:
                    size, problem, waiting_time, execution_time = rec[:4]
                    throws = rec[4] if n >= 5 else None
                    out.append([size, problem, waiting_time, throws])
                else:
                    # format inattendu, on ignore ou on lève une erreur
                    # raise ValueError(f"Record trop court: {rec}")
                    continue
            else:
                # format inattendu (ex: dict) -> adapte ici si besoin
                # raise TypeError(f"Type non supporté: {type(rec)}")
                continue
    return out


def _assert_same_elements(res, expected):
    assert {tuple(sorted(x)) for x in res} == {tuple(sorted(pb)) for pb, _ in expected}


def load_all(path: str | Path):
    """Charge tous les objets picklés successifs."""
    path = Path(path)
    objs = []
    if not path.exists():
        return objs
    with path.open("rb") as f:
        while True:
            try:
                objs.append(pickle.load(f))
            except EOFError:
                break
    return objs


def save_all(path: str | Path, objs):
    """Réécrit un .pkl avec une séquence d’objets."""
    path = Path(path)
    with path.open("wb") as f:
        for obj in objs:
            pickle.dump(obj, f)


def remove_one(path: str | Path, to_remove):
    """
    Retire une liste `to_remove` (égalité Python ==) du fichier.
    Si plusieurs correspondent, elles seront toutes supprimées.
    """
    objs = load_all(path)
    objs = [
        o
        for o in objs
        if not (o[0] == to_remove[0] and o[1] == to_remove[1] and o[2] == to_remove[2])
    ]
    save_all(path, objs)


if __name__ == "__main__":
    pre_test = []
    pkl_path = Path(__file__).resolve().parent / "data/todo_lockcell.pkl"
    with pkl_path.open("rb") as f:
        while True:
            try:
                size, problem, waiting_time, force = pickle.load(f)
                pre_test.append([size, problem, waiting_time, force])
            except EOFError:
                break

    done = load_records_with_source(
        Path(__file__).resolve().parent / "data/lockcell_bench.pkl", "lockcell"
    )
    done_norm = [
        [size, problem, waiting_time] for size, problem, waiting_time, test in done if test
    ]
    to_test = []
    for size, problem, waiting_time, force in pre_test:
        if [size, problem, waiting_time] not in done_norm or force:
            if force:
                remove_one(
                    Path(__file__).resolve().parent / "data/lockcell_bench.pkl",
                    [size, problem, waiting_time],
                )
            if [size, problem, waiting_time] not in to_test:
                to_test.append([size, problem, waiting_time])
    print("-" * 30, "LAUNCHING COMPUTATION", "-" * 30)
    if not to_test:
        print("nothing to do")
        exit(0)

    n = len(to_test)
    print(f"launching {n} tests :")
    for size, problem, waiting_time in to_test:
        print(f"to_launch : size={size}, waiting_time={waiting_time}, problem={problem}")
    counter = 1
    for size, problem, waiting_time in to_test:
        with open("data/lockcell_bench.pkl", "ab") as file:
            # For potential print
            ## For Mock Test
            print(size, problem, waiting_time)
            config_ = BenchConfig(N=size, problems=problem, waiting_time_in_second=waiting_time)
            config_.set_mode("Analyse")

            updates: list[tuple[list, float]] = []
            with Lockcell(
                endpoint="172.29.94.180:5001", config=config_, environnement={"pip": ["numpy"]}
            ) as lock:
                lock.run_rddmin()
                start = time.time()
                status = lock.get_status()
                counter = 0
                while status != Status.COMPLETED:
                    if status == Status.UPDATED:
                        update = lock.get_update()
                        update_time = time.time() - start
                        for failing_set in update:
                            counter += 1
                            updates.append((failing_set, update_time))
                            print(f"Update at {(time.time() - start):.2f}s ---> {update}")
                    lock.update()
                    status = lock.get_status()
                    if counter <= 3:
                        time.sleep(2)
                    time.sleep(4.5)
                update = lock.get_update()
                update_time = time.time() - start
                for failing_set in update:
                    updates.append((failing_set, update_time))
                    print(f"Last update at {(time.time() - start):.2f}s ---> {update}")
                results = lock.get_result()
                stop = time.time()
                execution_time = stop - start
                _assert_same_elements(results, config_.Pb)

            pickle.dump([size, problem, waiting_time, execution_time, updates], file)
            print(
                f"run {counter}/{n} :done : size={size}, waiting_time={waiting_time}, problem={problem}, execution_time={execution_time}",
                "\n",
                "-" * 150,
            )
            counter += 1
