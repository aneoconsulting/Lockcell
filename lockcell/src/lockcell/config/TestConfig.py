from .BaseConfig import BaseConfig
from typing import List
import copy


class TestConfig(BaseConfig):
    def __init__(self, *args, nbRun=None):
        self.Pb = []
        super().__init__(nbRun)
        if args:
            self.Pb = copy.deepcopy(args[0])

    def GenProb(
        self, N: int, *args
    ):  # TODO: faire en sorte que les ensembles ne se surperposent pas
        self.Pb = []
        space = [i for i in range(N)]
        curN = N
        if args:
            for cle, nbr, et, p in args:
                try:
                    cle_int = int(cle)
                    if cle_int <= 0:
                        raise ValueError(
                            "Génération du problem set impossible, la taille de l'ensemble passée est négative"
                        )
                    for _ in range(cle):
                        idxs = GenSubset(curN, nbr, et)
                        elt = []
                        for idx in sorted(idxs, reverse=True):
                            elt.append(space[idx])
                            del space[idx]

                        self.Pb.append((elt, p))
                        curN -= nbr

                except ValueError as e:
                    raise ValueError(
                        "Erreur lors de la génération du problem set : conversion en entier | "
                        + str(e)
                    )
        else:
            raise ValueError(
                "Erreur lors de la génération du problem set : veuillez donner une taille d'ensemble minimaux au format \"taille de l'ensemble\" : nombre"
            )

    def Test(self, subspace):
        for test in self.Pb:
            if TestConfig.In(subspace, test[0]):
                return False
        return True

    @staticmethod
    def In(tab: list, test: list):
        res = True
        for i in test:
            if i not in tab:
                res = False
                break
        return res

    def copy(self):
        newCopy = TestConfig(self.Pb, self.nbRun)
        return newCopy


### TO GENERATE FAILING SET #####################################################################


def GenSubset(N: int, size: int, ET: float) -> List[int]:
    if size > N:
        raise RuntimeError(f"Cannot generate a {size} sized set in a {N} sized space")
    import numpy as np

    center = np.random.randint(0, N)
    val = [center]
    for _ in range(1, size):
        step = round(np.random.normal(loc=0, scale=ET))
        center += step
        center = max(0, min(center, N - 1))
        i = 1
        while center in val:
            up = max(0, min(center + i, N - 1))
            down = min(max(center - i, 0), N - 1)
            if up not in val:
                center = up
            elif down not in val:
                center = down
            i += 1
        val.append(center)
    return val
