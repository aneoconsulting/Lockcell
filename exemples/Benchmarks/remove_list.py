import pickle
from pathlib import Path


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
        if not (
            o[0] == to_remove[0]
            and o[1] == to_remove[1]
            and o[2] == to_remove[2]
            and o[3] >= to_remove[3]
        )
    ]
    save_all(path, objs)


if __name__ == "__main__":
    pkl_path = Path(__file__).resolve().parent / "data/lockcell_bench.pkl"
    size = 128
    problem = [([0, 64, 96], 1.0)]
    waiting_time = 1
    exec_time = 0
    input(
        f"Are you sure to delete {[size, problem, waiting_time]} if execution time is >= {exec_time}"
    )
    remove_one(pkl_path, [size, problem, waiting_time, exec_time])
