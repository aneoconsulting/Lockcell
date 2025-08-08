"""
Created on : 2025-07-07
Author   : Erwan Tchaleu
Email    : erwan.tchale@gmail.com

"""

from pymonik import Pymonik, MultiResultHandle

from .Tasks.Task import nTask
from .Tasks.utils import AminusB
from .config.BaseConfig import BaseConfig
import time
from .graphViz import MultiViz


### CODE ###########################################################################""


N = 2**10
searchspace = [i for i in range(N)]


def dd_min(searchspace: list, config: BaseConfig, graph=None):
    return nTask.invoke(searchspace, 2, config, graph)  # type: ignore


def RDDMIN(searchspace: list, func, finalfunc, config: BaseConfig, viz: MultiViz = MultiViz()):
    with Pymonik(endpoint="172.29.94.180:5001", environment={"pip": ["numpy"]}):
        start = time.time()
        result = dd_min(searchspace, config, viz.newGraph()).wait().get()
        i = 1
        tot = []
        while not result[1]:
            # On retire les doublons
            dic = {}
            res = []
            for key in result[0]:
                if key.__str__() not in dic:
                    res.append(key)
                    dic[key.__str__()] = True
            # On transmet
            if func is not None:
                func(res, i)

            # Ajout au total + réduction du searchspace, puis on relance un dd_min
            tot.extend(res)
            all = sum(result[0], [])
            searchspace = AminusB(searchspace, all)
            result = dd_min(searchspace, config, viz.newGraph()).wait().get()
            i += 1
        if finalfunc is not None:
            finalfunc(tot, i)
        stop = time.time()
        return tot, i, (stop - start)


def SRDDMIN(
    searchspace: list,
    nbRunTab: list,
    found,
    config: BaseConfig,
    viz: MultiViz = MultiViz(),
):
    # TODO: Preprocessing of nbRunTab

    findback = {}
    i = 0
    tot = []
    for run in nbRunTab:
        findback[run] = i
        i += 1
    with Pymonik(endpoint="172.29.94.180:5001", environment={"pip": ["numpy"]}):
        firstFail = False
        for run in nbRunTab:
            config.setNbRun(run)
            result = dd_min(searchspace, config, viz.newGraph()).wait().get()
            if result[1]:
                continue
            while not result[1]:
                firstFail = True
                config.setNbRun(run)
                done = False
                Args = [(res, 2, config) for res in result[0]]
                storeResult = nTask.map_invoke(Args).wait().get()

                # TODO: Quand l'implem de la disponibilité au plus tot sera prête faudra adapter
                while not done:
                    ready = [i for i in range(len(storeResult))]
                    notReady = config.listminus([i for i in range(len(storeResult))], ready)
                    nextArgs = []
                    waiting = MultiResultHandle([storeResult[idx] for idx in notReady])
                    didit = [storeResult[idx] for idx in ready]

                    # préparation des configuration pour les tâches suivantes,
                    for res in didit:
                        where = findback[res[2].nbRun]
                        if (
                            where + 1 >= len(nbRunTab)
                        ):  # Si on a déjà atteint le nombre de run max, on ajoute la sortie à tot et on réduit le search space
                            tot.extend(res[0])
                            all = sum(res[0], [])
                            found(res[0])
                            searchspace = config.listminus(searchspace, all)
                            continue

                        nextrun = nbRunTab[
                            where + 1
                        ]  # Sinon on trouve le nombre de run suivant et on prépare le lancement des tâches filles
                        onesized = []
                        for sub in res[0]:
                            if len(sub) == 1:
                                onesized.append(sub)
                                continue
                            newconf = config.copy()
                            newconf.setNbRun(nextrun)
                            nextArgs.append((sub, 2, newconf))
                        if onesized != []:
                            tot.extend(onesized)
                            all = sum(onesized, [])
                            found(onesized)
                            searchspace = config.listminus(searchspace, all)
                    if nextArgs:
                        if not waiting.result_handles:
                            storeResult = nTask.map_invoke(nextArgs)
                        else:
                            waiting.extend(nTask.map_invoke(nextArgs))
                            storeResult = waiting
                    else:
                        if not waiting:
                            done = True
                            continue
                    storeResult = storeResult.wait().get()
                result = dd_min(searchspace, config, viz.newGraph()).wait().get()
        if firstFail:
            return tot
        raise RuntimeError(
            f"SRDDMin : testing the subset {nbRunTab[-1]} times has never returned false"
        )
