import pickle
from dataclasses import dataclass
from typing import Any
import matplotlib.pyplot as plt
import warnings
import numpy as np

@dataclass
class Record:
    size: int
    problem: Any  # doit avoir une méthode __str__
    waiting_time: float
    y: float
    trace: list[tuple[list[Any], float]]  # <== NOUVEAU CHAMP
    tag: str

    @classmethod
    def from_list(cls, args: list) -> "Record":
        """Construit un Record à partir d'une liste/tuple d'arguments dans le bon ordre."""
        if len(args) != 6:
            raise ValueError(f"Expected 6 arguments, got {len(args)}")
        return cls(*args)

def obj_to_str(obj) -> str:
    return "zorg"

def load_records(path: str) -> list[Record]:
    """Charge toutes les listes de Record stockées via pickle.dump dans le même fichier.
    Retourne une liste de listes (une par dump).
    """
    records_collections = []
    with open(path, "rb") as f:
        while True:
            try:
                records_collections.append(Record.from_list(pickle.load(f)))
            except EOFError:
                break
    return records_collections


def filter_by_problem(records: list[Record], target_problem_str: str) -> list[Record]:
    return [r for r in records if str(r.problem) == target_problem_str]

def filter_by_waiting_time(records: list[Record], target_waiting_time: float) -> list[Record]:
    return [r for r in records if r.waiting_time == target_waiting_time]

def filter_by_tag(records: list[Record], target_tag: str) -> list[Record]:
    return [r for r in records if r.tag == target_tag]

### PRINTER 

def print_y_vs_size(title: str, lockcell: list[Record], verrou: list[Record]):
    def extract_unique(records, label):
        sizes = {}
        for r in records:
            if r.size in sizes:
                raise ValueError(f"Duplicate size '{r.size}' found in {label}.")
            sizes[r.size] = r.y
        return sizes

    if len(lockcell) != len(verrou):
        warnings.warn(f"Unequal number of records: lockcell={len(lockcell)}, verrou={len(verrou)}")

    lockcell_data = extract_unique(lockcell, "lockcell")
    verrou_data = extract_unique(verrou, "verrou")

    plt.figure()
    plt.plot(
        sorted(lockcell_data.keys()), 
        [lockcell_data[k] for k in sorted(lockcell_data.keys())],
        color='blue', label='lockcell'
    )
    plt.plot(
        sorted(verrou_data.keys()), 
        [verrou_data[k] for k in sorted(verrou_data.keys())],
        color='orange', linestyle='dotted', label='verrou'
    )
    plt.title(title)
    plt.xlabel("size")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)

    plt.savefig(f"plot/{title}.png", bbox_inches='tight')
    plt.close()

def print_y_vs_waiting_time(title: str, lockcell: list[Record], verrou: list[Record]):
    def extract_unique(records, label):
        times = {}
        for r in records:
            if r.waiting_time in times:
                raise ValueError(f"Duplicate waiting_time '{r.waiting_time}' in {label}.")
            times[r.waiting_time] = r.y
        return times

    if len(lockcell) != len(verrou):
        warnings.warn(f"Unequal number of records: lockcell={len(lockcell)}, verrou={len(verrou)}")

    lockcell_data = extract_unique(lockcell, "lockcell")
    verrou_data = extract_unique(verrou, "verrou")

    plt.figure()
    plt.plot(
        sorted(lockcell_data.keys()),
        [lockcell_data[k] for k in sorted(lockcell_data.keys())],
        color='blue', label='lockcell'
    )
    plt.plot(
        sorted(verrou_data.keys()),
        [verrou_data[k] for k in sorted(verrou_data.keys())],
        color='orange', linestyle='dotted', label='verrou'
    )
    plt.title(title)
    plt.xlabel("waiting_time")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)

    plt.savefig(f"plot/{title}.png", bbox_inches='tight')
    plt.close()

def print_trace_comparison(title: str, lockcell: list[Record], verrou: list[Record]):
    if len(lockcell) != 1 or len(verrou) != 1:
        raise ValueError("Each list must contain exactly one Record.")

    trace_l = lockcell[0].trace
    trace_v = verrou[0].trace

    n = max(len(trace_l), len(trace_v))
    x = np.arange(n)
    
    heights_l = [t[1] for t in trace_l]
    heights_v = [t[1] for t in trace_v]

    while len(heights_l) < n:
        heights_l.append(0)
    while len(heights_v) < n:
        heights_v.append(0)

    bar_width = 0.4

    plt.figure()
    plt.bar(x - bar_width/2, heights_l, width=bar_width, color='blue', label='lockcell')
    plt.bar(x + bar_width/2, heights_v, width=bar_width, color='orange', linestyle='dotted', label='verrou')

    plt.title(title)
    plt.xlabel("Object Index")
    plt.ylabel("Recovery Time")
    plt.legend()
    plt.grid(True)

    plt.savefig(f"plot/{title}.png", bbox_inches='tight')
    plt.close()

from typing import Callable

def print_trace_with_labels(title: str, lockcell: list[Record], verrou: list[Record]):
    if len(lockcell) != 1 or len(verrou) != 1:
        raise ValueError("Each list must contain exactly one Record.")

    trace_l = lockcell[0].trace
    trace_v = verrou[0].trace

    n = max(len(trace_l), len(trace_v))
    x = np.arange(n)

    heights_l = [t[1] for t in trace_l]
    heights_v = [t[1] for t in trace_v]
    labels = []

    # Choisir quel objet utiliser pour étiqueter : lockcell ou verrou
    for i in range(n):
        if i < len(trace_l):
            labels.append(obj_to_str(trace_l[i][0]))
        elif i < len(trace_v):
            labels.append(obj_to_str(trace_v[i][0]))
        else:
            labels.append("")

    # Padding des hauteurs
    while len(heights_l) < n:
        heights_l.append(0)
    while len(heights_v) < n:
        heights_v.append(0)

    bar_width = 0.4

    plt.figure()
    plt.bar(x - bar_width/2, heights_l, width=bar_width, color='blue', label='lockcell')
    plt.bar(x + bar_width/2, heights_v, width=bar_width, color='orange', linestyle='dotted', label='verrou')

    plt.title(title)
    plt.xlabel("Object Index")
    plt.ylabel("Recovery Time")
    plt.legend()
    plt.grid(True)

    # Ajouter les labels centrés entre les barres
    for i in range(n):
        y_max = max(heights_l[i], heights_v[i])
        plt.text(x[i], y_max + 0.01, labels[i], ha='center', va='bottom', fontsize=8, rotation=45)

    plt.savefig(f"plot/{title}.png", bbox_inches='tight')
    plt.close()



if __name__ == "__main__":
    verrou_records = load_records("./data/verrou_bench.pkl")
    lockcell_records = load_records("./data/lockcell_bench.pkl")
    print("verrou")
    for rec in verrou_records:
        print(rec.size)
    print("lockcell")
    for rec in lockcell_records:
        print(rec.size, ", ", rec.waiting_time)
    
    
    filtered_lockcell = filter_by_tag(lockcell_records, "SIMPLE")
    filtered_lockcell = filter_by_waiting_time(filtered_lockcell, 1)
    filtered_verrou   = filter_by_tag(verrou_records, "SIMPLE")

    print_y_vs_size("y_vs_size_SIMPLE", filtered_lockcell, filtered_verrou)