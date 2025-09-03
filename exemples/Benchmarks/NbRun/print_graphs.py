# print_graphs_new.py
from __future__ import annotations
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Union
import hashlib
import pickle
import matplotlib

matplotlib.use("Agg")  # on sauve des images, pas d'affichage interactif
import matplotlib.pyplot as plt

Record = List[Any]  # [size, problem, waiting_time, execution_time, _from, throw]

# --- Utils --------------------------------------------------------------------


def make_hashable(obj):
    """
    Convertit récursivement objets mutables en structures immuables hashables.
    - list/tuple -> tuple(...)
    - set/frozenset -> tuple trié des éléments convertis
    - dict -> tuple trié de (clé, valeur_convertie)
    Autres types laissés tels quels (int, float, str, ...).
    """
    # list ou tuple -> tuple de versions hashables
    if isinstance(obj, (list, tuple)):
        return tuple(make_hashable(x) for x in obj)

    # ensembles -> tuple trié pour stabilité
    if isinstance(obj, (set, frozenset)):
        return tuple(sorted((make_hashable(x) for x in obj), key=repr))

    # dictionnaires -> tuple trié de paires (clé, valeur)
    if isinstance(obj, dict):
        return tuple(
            sorted(((make_hashable(k), make_hashable(v)) for k, v in obj.items()), key=repr)
        )

    return obj


def slug(x: Any) -> str:
    return hashlib.md5(repr(x).encode("utf-8")).hexdigest()[:8]


def short_str(x: Any, maxlen: int = 80) -> str:
    s = repr(x)
    return s if len(s) <= maxlen else s[: maxlen - 1] + "…"


# --- Filtres (un par champ, sauf throw) --------------------------------------


def filter_by_size(
    records: Iterable[Record],
    min_size: Optional[int] = None,
    max_size: Optional[int] = None,
    allowed: Optional[Iterable[int]] = None,
) -> List[Record]:
    allow = set(allowed) if allowed is not None else None
    out: List[Record] = []
    for r in records:
        size = int(r[0])
        if allow is not None and size not in allow:
            continue
        if min_size is not None and size < min_size:
            continue
        if max_size is not None and size > max_size:
            continue
        out.append(r)
    return out


def filter_by_problem(
    records: Iterable[Record],
    allowed: Optional[Iterable[Any]] = None,
    predicate: Optional[Callable[[Any], bool]] = None,
) -> List[Record]:
    """`allowed` doit contenir des problems *normalisés* (via make_hashable)."""
    allow_norm = set(make_hashable(p) for p in allowed) if allowed is not None else None
    out: List[Record] = []
    for r in records:
        prob_norm = make_hashable(r[1])
        if allow_norm is not None and prob_norm not in allow_norm:
            continue
        if predicate is not None and not predicate(r[1]):
            continue
        out.append(r)
    return out


def filter_by_waiting_time(
    records: Iterable[Record],
    min_wt: Optional[Union[int, float]] = None,
    max_wt: Optional[Union[int, float]] = None,
    allowed: Optional[Iterable[Union[int, float]]] = None,
) -> List[Record]:
    allow = set(allowed) if allowed is not None else None
    out: List[Record] = []
    for r in records:
        wt = r[2]
        if allow is not None and wt not in allow:
            continue
        if min_wt is not None and wt < min_wt:
            continue
        if max_wt is not None and wt > max_wt:
            continue
        out.append(r)
    return out


def filter_by_execution_time(
    records: Iterable[Record],
    min_exec: Optional[float] = None,
    max_exec: Optional[float] = None,
) -> List[Record]:
    out: List[Record] = []
    for r in records:
        t = float(r[3])
        if min_exec is not None and t < min_exec:
            continue
        if max_exec is not None and t > max_exec:
            continue
        out.append(r)
    return out


def filter_by_source(
    records: Iterable[Record],
    sources: Optional[Iterable[str]] = None,  # ex: {"lockcell", "verrou"}
) -> List[Record]:
    if sources is None:
        return list(records)
    allow = {s.lower() for s in sources}
    return [r for r in records if str(r[4]).lower() in allow]


def filter_by_size_problem(
    records: Iterable[Record], allowed_pairs: Iterable[tuple[int, Any]]
) -> list[Record]:
    """
    Garde uniquement les records dont (size, problem) est dans allowed_pairs.
    """
    allowed_norm = {(int(s), make_hashable(p)) for (s, p) in allowed_pairs}
    out = []
    for r in records:
        size, problem = int(r[0]), r[1]
        if (size, make_hashable(problem)) in allowed_norm:
            out.append(r)
    return out


# --- Chargement des records --------------------------


def load_records_with_source(pkl_path: Union[str, Path], source: str) -> List[Record]:
    """
    Charge un fichier contenant une suite de pickle.dump([size, problem, waiting_time, execution_time], f)
    et ajoute un 5e champ '_from' = source ('verrou' ou 'lockcell').
    """
    p = Path(pkl_path)
    out: List[Record] = []
    with p.open("rb") as f:
        while True:
            try:
                args = pickle.load(f)
                out.append([args[0], args[1], args[2], args[3], source])
            except EOFError:
                break

    return out


# --- Groupage par problem -> waiting_time -> source --------------------------


def group_by_problem_waiting_source(
    records: Iterable[Record],
) -> Dict[Any, Dict[Any, Dict[str, List[Record]]]]:
    """
    Retourne un dict:
      { problem_norm: {
           waiting_time: {
              "lockcell": [records triés par size],
              "verrou":   [records triés par size],
           }, ...
         }, ...
      }
    """
    grouped: Dict[Any, Dict[Any, Dict[str, List[Record]]]] = {}
    for r in records:
        size, problem, wt, _, src = r[:5]
        pkey = make_hashable(problem)
        grouped.setdefault(pkey, {}).setdefault(wt, {}).setdefault(str(src), []).append(r)

    # trier par size
    for pkey in grouped:
        for wt in grouped[pkey]:
            for src in grouped[pkey][wt]:
                grouped[pkey][wt][src].sort(key=lambda rr: int(rr[0]))
    return grouped


# --- Tracés: une image créée à chaque appel ----------------------------------


def plot_per_problem_linear(
    records: Iterable[Record],
    out_dir: Union[str, Path] = "plots",
    linestyle_map: Optional[Dict[str, str]] = None,
) -> None:
    """
    Graphe par problem : y = execution_time, x = size.
    Une courbe par (waiting_time, _from). Sauvegarde PNG par problem.
    """
    if linestyle_map is None:
        linestyle_map = {"verrou": "--", "lockcell": "-"}
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    grouped = group_by_problem_waiting_source(records)
    for pkey, wt_map in grouped.items():
        plt.figure()
        for wt, by_src in wt_map.items():
            for src, recs in sorted(by_src.items()):
                xs = [int(r[0]) for r in recs]
                ys = [float(r[3]) for r in recs]
                plt.plot(
                    xs,
                    ys,
                    linestyle=linestyle_map.get(src, "-"),
                    marker="o",
                    label=f"wt={wt} ({src})",
                )
        plt.xlabel("size")
        plt.ylabel("execution_time")
        plt.title(f"Problem : {short_str(pkey)}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        fname = out / f"problem_{slug(pkey)}.png"
        plt.savefig(fname, dpi=200)
        plt.close()
        print("Figure enregistrée :", fname)


def plot_per_problem_xlog(
    records: Iterable[Record],
    out_dir: Union[str, Path] = "plots",
    linestyle_map: Optional[Dict[str, str]] = None,
) -> None:
    """
    Même graphe que ci-dessus mais avec l'axe X (size) en échelle log.
    """
    if linestyle_map is None:
        linestyle_map = {"verrou": "--", "lockcell": "-"}
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    grouped = group_by_problem_waiting_source(records)
    for pkey, wt_map in grouped.items():
        plt.figure()
        for wt, by_src in wt_map.items():
            for src, recs in sorted(by_src.items()):
                xs = [int(r[0]) for r in recs]
                ys = [float(r[3]) for r in recs]
                plt.plot(
                    xs,
                    ys,
                    linestyle=linestyle_map.get(src, "-"),
                    marker="o",
                    label=f"wt={wt} ({src})",
                )
        plt.xlabel("size")
        plt.ylabel("execution_time")
        plt.title(f"Problem : {short_str(pkey)}")
        plt.xscale("log")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        fname = out / f"problem_{slug(pkey)}_xlog.png"
        plt.savefig(fname, dpi=200)
        plt.close()
        print("Figure enregistrée :", fname)


def plot_fxy_per_problem(
    records: Iterable[Record],
    fxy: Callable[[float, float], float],
    name: str = "formula",
    out_dir: Union[str, Path] = "plots",
) -> None:
    """
    3e graphe par problem : trace f(x,y) en fonction de size,
    avec x = execution_time (lockcell), y = execution_time (verrou).
    On aligne les points par 'size' (intersection des sizes présents).
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    grouped = group_by_problem_waiting_source(records)

    for pkey, wt_map in grouped.items():
        plt.figure()
        plotted_any = False
        for wt, by_src in wt_map.items():
            if "lockcell" not in by_src or "verrou" not in by_src:
                continue
            lock = {int(r[0]): float(r[3]) for r in by_src["lockcell"]}
            verr = {int(r[0]): float(r[3]) for r in by_src["verrou"]}
            common_sizes = sorted(set(lock) & set(verr))
            if not common_sizes:
                continue
            xs = common_sizes
            vals = [fxy(lock[s], verr[s]) for s in xs]
            plt.plot(xs, vals, marker="o", label=f"wt={wt}")
            plotted_any = True

        if not plotted_any:
            plt.close()
            continue

        plt.xlabel("size")
        plt.ylabel(name)
        plt.title(f"Problem : {short_str(pkey)}")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        fname = out / f"problem_{slug(pkey)}_{name}.png"
        plt.savefig(fname, dpi=200)
        plt.close()
        print("Figure enregistrée :", fname)


def plot_execution_vs_size(
    records: Iterable[Record], title: str, out_dir: Union[str, Path] = "plots"
) -> None:
    """
    Trace execution_time en fonction de size, sans séparer par problem.
    On distingue les séries par (waiting_time, _from).
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # regrouper par (waiting_time, source)
    from collections import defaultdict

    groups = defaultdict(list)
    for r in records:
        size, _, wt, exec_time, src = r[:5]
        groups[(wt, src)].append((int(size), float(exec_time)))

    plt.figure()
    for (wt, src), pts in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        pts.sort(key=lambda x: x[0])
        xs, ys = zip(*pts)
        linestyle = "--" if src == "verrou" else "-"
        plt.plot(xs, ys, marker="o", linestyle=linestyle, label=f"wt={wt} ({src})")

    plt.xlabel("size")
    plt.ylabel("execution_time")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # nom de fichier à partir du titre
    safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in title)
    fname = out / f"{safe_name}.png"
    plt.savefig(fname, dpi=200)
    plt.close()
    print("Figure enregistrée :", fname)


def plot_fxy_vs_size(records, fxy, title: str, out_dir: str | Path = "plots", name: str = "fxy"):
    """
    Trace f(x,y) en fonction de size.
    x = exec_time lockcell
    y = exec_time verrou
    fxy(x,y) est la valeur affichée.
    Suppose que pour chaque size on a exactement un record lockcell et un record verrou.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # regrouper par (waiting_time)
    from collections import defaultdict

    by_wt = defaultdict(lambda: {"lockcell": [], "verrou": []})
    for r in records:
        size, _, wt, exec_time, src = r[:5]
        by_wt[wt][src].append((int(size), float(exec_time)))

    plt.figure()
    for wt, srcmap in by_wt.items():
        lock = {s: t for s, t in srcmap["lockcell"]}
        verr = {s: t for s, t in srcmap["verrou"]}

        common = sorted(set(lock) & set(verr))
        if not common:
            continue

        xs = common
        vals = []
        for s in common:
            try:
                vals.append(fxy(lock[s], verr[s]))
            except Exception as e:
                raise RuntimeError(f"Erreur sur size={s}, lock={lock[s]}, verr={verr[s]}") from e

        plt.plot(xs, vals, marker="o", label=f"wt={wt}")

    plt.xlabel("size")
    plt.ylabel(name)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in title)
    fname = out / f"{safe_name}_{name}.png"
    plt.savefig(fname, dpi=200)
    plt.close()
    print("Figure enregistrée :", fname)


def plot_execution_vs_size_xlog(
    records: Iterable[Record], title: str, out_dir: Union[str, Path] = "plots"
) -> None:
    """
    Trace execution_time en fonction de size, sans séparer par problem.
    On distingue les séries par (waiting_time, _from).
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # regrouper par (waiting_time, source)
    from collections import defaultdict

    groups = defaultdict(list)
    for r in records:
        size, _, wt, exec_time, src = r[:5]
        groups[(wt, src)].append((int(size), float(exec_time)))

    plt.figure()
    for (wt, src), pts in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        pts.sort(key=lambda x: x[0])
        xs, ys = zip(*pts)
        linestyle = "--" if src == "verrou" else "-"
        plt.plot(xs, ys, marker="o", linestyle=linestyle, label=f"wt={wt} ({src})")

    plt.xlabel("size")
    plt.ylabel("execution_time")
    plt.title(title)
    plt.xscale("log")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # nom de fichier à partir du titre
    safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in title)
    fname = out / f"{safe_name}.png"
    plt.savefig(fname, dpi=200)
    plt.close()
    print("Figure enregistrée :", fname)


# --- Exemple d'utilisation ---
if __name__ == "__main__":
    # chargement des calculs faits
    # chemins vers tes deux fichiers
    fichier_verrou = "data/verrou_bench.pkl"
    fichier_lockcell = "data/lockcell_bench.pkl"

    recs_verrou = load_records_with_source(fichier_verrou, "verrou")
    recs_lockcell = load_records_with_source(fichier_lockcell, "lockcell")
    # fusion
    all_records = recs_verrou + recs_lockcell

    recs = filter_by_source(all_records, {"lockcell", "verrou"})
    recs = filter_by_size(recs, min_size=1, max_size=None)
    # recs = filter_by_waiting_time(recs, allowed=[0, 1, 2])
    # recs = filter_by_execution_time(recs, min_exec=0.0)
    # recs = filter_by_problem(recs, predicate=lambda p: True)

    # 2 graphes par problem (linéaire + X log)
    recs_pb = filter_by_waiting_time(recs, 3, 3)
    plot_per_problem_linear(recs_pb, out_dir="plots")
    plot_per_problem_xlog(recs_pb, out_dir="plots")

    # 3e graphe : définis ta formule f(x, y)
    def my_formula(x_lockcell: float, y_verrou: float) -> float:
        # exemple: ratio
        return y_verrou / x_lockcell if x_lockcell != 0 else float("inf")

    plot_fxy_per_problem(
        recs_pb, fxy=my_formula, name="ratio_verrou_over_lockcell", out_dir="plots"
    )
    to_filter: list[tuple[int, list]] = [(4, [([0], 1.0), ([2], 1.0)])]
    to_filter += [(8, [([0], 1.0), ([4], 1.0)])]
    to_filter += [(16, [([0], 1.0), ([8], 1.0)])]
    to_filter += [(32, [([0], 1.0), ([16], 1.0)])]
    to_filter += [(64, [([0], 1.0), ([32], 1.0)])]
    to_filter += [(128, [([0], 1.0), ([64], 1.0)])]
    recs_evo = filter_by_size_problem(recs, to_filter)
    plot_execution_vs_size(recs_evo, "evolution_two_sets")
    plot_fxy_vs_size(recs_evo, my_formula, "ratio_evo_two_sets")

    to_filter: list[tuple[int, list]] = [(4, [([0, 2], 1.0)])]
    for i in range(3, 10):
        to_filter += [(2**i, [([0, 2 ** (i - 1)], 1.0)])]

    recs_evo = filter_by_size_problem(recs, to_filter)
    recs_evo = filter_by_waiting_time(recs_evo, 2, 2)
    plot_execution_vs_size(recs_evo, "evolution_two_elts")
    plot_execution_vs_size_xlog(recs_evo, "log_evolution_two_elts")
    plot_fxy_vs_size(recs_evo, my_formula, "ratio_evo_two_elts")

    to_filter = [(4, [([0, 2, 3], 1.0)])]
    for i in range(3, 8):
        to_filter += [(2**i, [([0, 2 ** (i - 1), 2 ** (i - 1) + 2 ** (i - 2)], 1.0)])]

    recs_evo = filter_by_size_problem(recs, to_filter)
    recs_evo = filter_by_waiting_time(recs_evo, 1, 1)
    plot_execution_vs_size(recs_evo, "evolution_three_elts")
    plot_execution_vs_size_xlog(recs_evo, "log_evolution_three_elts")
    plot_fxy_vs_size(recs_evo, my_formula, "ratio_evo_three_elts")
