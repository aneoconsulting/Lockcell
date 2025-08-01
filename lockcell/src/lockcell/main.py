"""
Created on : 2025-07-07
Author   : Erwan Tchaleu
Email    : erwan.tchale@gmail.com

"""

PRINT_GRAPH = False

import controllers
from Tasks import TaskEnv
from graphViz import MultiViz
import VerrouConf
<<<<<<< HEAD:main.py
=======
import constants
>>>>>>> et/HandleDependencies:lockcell/src/lockcell/main.py
import cloudpickle # Install cloudpickle
cloudpickle.register_pickle_by_value(TaskEnv) # Pour les modules de ton code tu fait du sort que ca soit pickler par value
cloudpickle.register_pickle_by_value(controllers) # Pour les modules de ton code tu fait du sort que ca soit pickler par value
cloudpickle.register_pickle_by_value(VerrouConf) # Pour les modules de ton code tu fait du sort que ca soit pickler par value
cloudpickle.register_pickle_by_value(constants) # Pour les modules de ton code tu fait du sort que ca soit pickler par value


printgraph = False

<<<<<<< HEAD:main.py
N = 2**6
=======
N = 2**7
>>>>>>> et/HandleDependencies:lockcell/src/lockcell/main.py
searchspace = [i for i in range(N)]

def counter(n : int):
    if n <0:
        return "Number Err"
    if n <= 3:
        if n == 1:
            return "First"
        if n == 2:
            return "Second"
        if n == 3:
            return "Third"
    return n.__str__() + "th"

def parseRes(tableau: list[list[str]]) -> list[list[str]]:
    return [
        [s.split("\t")[0] + ":" + s.split("\t")[1] for s in sous_liste]
        for sous_liste in tableau
    ]

def say(res, i):
    
    print(counter(i) + " results : " + parseRes(res).__str__() + "\n" +"-"*80)


def say2(res):
    print("Found : " + parseRes(res).__str__() + "\n" +"-"*80)

def finalSay(res, i):
    print("\n" + "-"*80 +"\n" + "-"*80  + "\n" + "Recursions : " + i.__str__() + " | Total results : " + parseRes(res).__str__()  +"\n" + "-"*80  +"\n" + "-"*80)


<<<<<<< HEAD:main.py
# Problème d'implémentation de la stochasticité, en effet les 1 minimaux d'un période ne failent pas forcément à la suivante il faut un cache ou alors transmette le fait que ce truc ne marche pas
Viz = MultiViz(active=printgraph)
#config = controllers.TestConfig([[[56], 0.3], [[94], 0.3], [[42, 40], 0.5], [[118, 114, 115], 0.5], [[76, 80, 78, 82], 0.5]])# EXCELLENT EXEMPLE avec N = 2**7
#config = controllers.TestConfig([[[0, 2, 4, 6], 0.5]])
#config = controllers.TestConfig([([51], 0.3), ([1], 0.3), ([12, 11], 0.5), ([4, 2, 0], 0.5), ([63, 62, 61], 0.5), ([15, 10, 6], 0.5), ([20, 17, 16], 0.5), ([46, 40, 35], 0.5)])
config = VerrouConf.ConfigVerrou("./verrou", "DD_RUN", "DD_CMP.py")
=======
Viz = MultiViz(active=PRINT_GRAPH)

### For simple Test
#config = controllers.TestConfig([[[56], 0.3], [[94], 0.3], [[42, 40], 0.5], [[118, 114, 115], 0.5], [[76, 80, 78, 82], 0.5]]) # N = 2**7

## For verrou Test
config = VerrouConf.ConfigVerrou(constants.USER_WORKING_DIR + "/verrou", "DD_RUN", "DD_CMP.py")
>>>>>>> et/HandleDependencies:lockcell/src/lockcell/main.py
config.setMode("Analyse")
input("press to continue...")
config.parseGenRunFile()
searchspace = config.generateSearchSpace()
from pathlib import Path
config.workdir = Path(constants.TASK_WORKING_DIR + "/verrou")
res = controllers.RDDMIN(searchspace, say, finalSay, config, Viz)
print(res)


<<<<<<< HEAD:main.py
if printgraph:
=======
if PRINT_GRAPH:
>>>>>>> et/HandleDependencies:lockcell/src/lockcell/main.py
    Viz.aff_all()


