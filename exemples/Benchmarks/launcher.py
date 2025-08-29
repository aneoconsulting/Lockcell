import argparse
import pickle
from pathlib import Path


def load_all(path: Path):
    """Charge tous les objets picklés successifs."""
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--print",
        action="store_true",
        help="Afficher le contenu des fichiers lockcell et verrou",
    )
    args = parser.parse_args()

    # chemins vers tes deux fichiers
    fichier_verrou = Path(__file__).resolve().parent / "data/todo_verrou.pkl"
    fichier_lockcell = Path(__file__).resolve().parent / "data/todo_lockcell.pkl"

    # si option -p activée, afficher les contenus
    if args.print:
        print("=== Lockcell ===")
        for rec in load_all(fichier_lockcell):
            print(rec[:-1], end="")
            if rec[-1]:
                print("forced", end="")
            print()
        print("=== Verrou ===")
        for rec in load_all(fichier_verrou):
            print(rec[:-1], end="")
            if rec[-1]:
                print(" forced", end="")
            print()
    else:
        # format : size, problem, waiting_time, False
        to_add = [
            [
                2**7,
                [
                    ([1], 0.3),
                    ([8], 0.3),
                    ([2, 9], 0.3),
                    ([42, 40], 0.5),
                    ([118, 114, 115, 127], 0.5),
                ],
                0.5,
                False,
            ]
        ]

        # écraser les fichiers avec ces données
        with fichier_lockcell.open("wb") as f_l:
            for x in to_add:
                pickle.dump(x, f_l)

        with fichier_verrou.open("wb") as f_v:
            for x in to_add:
                pickle.dump(x, f_v)
