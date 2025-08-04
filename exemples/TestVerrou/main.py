PRINT_GRAPH = False
import os
import sys
from pathlib import Path
os.environ["LOCKCELL_CONFIG"] = str(Path(__file__).parent/ "config.yaml")


from lockcell import MultiViz, VerrouConf, constants, controllers
import tools

# For potential print
Viz = MultiViz(active=PRINT_GRAPH)

## For verrou Test
config = VerrouConf.ConfigVerrou(constants.USER_WORKING_DIR, "DD_RUN", "DD_CMP.py")
config.setMode("Analyse")
input("press Enter to continue...")

# Parse the file to get the deltas
print("[INFO] Parsing the original file")
config.parseGenRunFile()
searchspace = config.generateSearchSpace()
print("[INFO] Parsing done, searchspace generated")

from pathlib import Path
config.workdir = Path(constants.TASK_WORKING_DIR + "/verrou")

# Launching RDDMin
res = controllers.RDDMIN(searchspace, tools.say, tools.finalSay, config, Viz)


# Potential graphprint
if PRINT_GRAPH:
    Viz.aff_all()
