"""
Created on : 2025-07-07
Author   : Erwan Tchaleu
Email    : erwan.tchale@gmail.com

"""
import time
from copy import copy
from typing import Any

from pymonik import Pymonik, MultiResultHandle, ResultHandle

from .Tasks.Task import nTask
from .Tasks.utils import AminusB
from .config.BaseConfig import BaseConfig
from .status import Status
from .graphViz import MultiViz

class Lockcell:
    def __init__(self, endpoint :str | None, config: BaseConfig, python_environnement : dict[str, Any] = {}) -> None:

        # Configuration
        self._endpoint : str | None = endpoint
        self._config : BaseConfig = config
        self._search_space : list = config.generate_search_space()
        self._pymonik_environnement : dict[str, Any] = python_environnement

        self._default_session = Pymonik(endpoint=self._endpoint, partition="pymonik", environment=self._pymonik_environnement).__enter__()
        self._sessions : list[tuple[Pymonik, int]]= []

        # Status
        self._running : bool = False

        # Constants
        self.INTERNAL_SP = None
    
    def __del__(self):
        for session in self._sessions:
            session[0].__exit__(None, None, None)
        self._default_session.__exit__(None, None, None)

    ### DeltaDebug code

    def dd_min(self, search_space : list | None, config: BaseConfig, graph=None):
        if search_space:
            return nTask.invoke(search_space, 2, config, graph).wait().get()  #type: ignore
        return nTask.invoke(self._search_space, 2, config, graph).wait().get()  #type: ignore

    def _dd_min(self, search_space : list | None, config: BaseConfig, graph=None):
        if search_space:
            return nTask.invoke(search_space, 2, config, graph)  #type: ignore
        return nTask.invoke(self._search_space, 2, config, graph, pymonik=self._default_session)  #type: ignore

    def RDDMIN(self, log_function = None, final_log_function = None, viz: MultiViz = MultiViz()):
        start = time.time()
        result = self._dd_min(self.INTERNAL_SP, self.config, viz.newGraph()).wait().get()
        i = 1
        tot = []
        while not result[1]:
            res = result[0]
            # On transmet
            if log_function is not None:
                log_function(res, i)

            # Ajout au total + réduction du searchspace, puis on relance un dd_min
            tot.extend(res)
            all = sum(result[0], [])
            self._reduce_search_space(all)
            result = self._dd_min(self.INTERNAL_SP, self.config, viz.newGraph()).wait().get()
            i += 1
        if final_log_function is not None:
            final_log_function(tot, i)
        stop = time.time()
        return tot, i, (stop - start)

    #TODO: Make it run directly on PymoniK
    def SRDDMIN(
        self,
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
        with Pymonik(endpoint=self._endpoint, environment=self._pymonik_environnement):
            firstFail = False
            for run in nbRunTab:
                config.set_nb_run(run)
                result = self._dd_min(self.INTERNAL_SP, config, viz.newGraph()).wait().get()
                if result[1]:
                    continue
                while not result[1]:
                    firstFail = True
                    config.set_nb_run(run)
                    done = False
                    Args = [(res, 2, config) for res in result[0]]
                    storeResult = nTask.map_invoke(Args).wait().get() #type: ignore

                    # TODO: Quand l'implem de la disponibilité au plus tot sera prête faudra adapter
                    while not done:
                        ready = [i for i in range(len(storeResult))]
                        notReady = AminusB([i for i in range(len(storeResult))], ready)
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
                                self._reduce_search_space(all)
                                continue

                            nextrun = nbRunTab[
                                where + 1
                            ]  # Sinon on trouve le nombre de run suivant et on prépare le lancement des tâches filles
                            onesized = []
                            for sub in res[0]:
                                if len(sub) == 1:
                                    onesized.append(sub)
                                    continue
                                newconf = copy(config)
                                newconf.set_nb_run(nextrun)
                                nextArgs.append((sub, 2, newconf))
                            if onesized != []:
                                tot.extend(onesized)
                                all = sum(onesized, [])
                                found(onesized)
                                self._reduce_search_space(all)
                        if nextArgs:
                            if not waiting.result_handles:
                                storeResult = nTask.map_invoke(nextArgs) #type: ignore
                            else:
                                waiting.extend(nTask.map_invoke(nextArgs)) #type: ignore
                                storeResult = waiting
                        else:
                            if not waiting:
                                done = True
                                continue
                        storeResult = storeResult.wait().get() #type: ignore
                    result = self._dd_min(self.INTERNAL_SP, config, viz.newGraph()).wait().get()
            if firstFail:
                return tot
            raise RuntimeError(
                f"SRDDMin : testing the subset {nbRunTab[-1]} times has never returned false"
            )
        
    ### Attribute Manager

    @property
    def config(self) -> BaseConfig:
        return self._config
    
    @property
    def endpoint(self) -> str | None:
        return self._endpoint

    @property
    def search_space(self) -> list:
        return self._search_space  
    
    @property
    def python_environnement(self) -> dict[str, Any]:
        return self._pymonik_environnement

    @config.setter
    def config(self, config: BaseConfig) -> bool:
        if self.is_running:
            return False
        self._config = copy(config)
        self._search_space = self._config.generate_search_space()
        return True
    
    @property
    def is_running(self) -> bool:
        return self._running
        
    ### Helpers
    def _reduce_search_space(self, to_subtract : list):
        self._search_space = AminusB(self._search_space, to_subtract)
    
    def _is_ready(self, session : Pymonik, result : ResultHandle) -> bool:
        armonik_result_pointer = session._results_client.get_result(result.result_id)
        return armonik_result_pointer.status == 2

