def main():
    PRINT_GRAPH = False
    import os
    import sys
    from pathlib import Path
    if len(sys.argv) > 0:
        os.environ["LOCKCELL_CONFIG"] = str(Path(__file__)/ "config.yaml")
    else:
        raise ValueError("Missing arguments: please provide the path to the config file.")



    from lockcell import *
    import tools

    # For potential print
    Viz = MultiViz(active=PRINT_GRAPH)

    ## For verrou Test
    config = VerrouConf.ConfigVerrou(constants.USER_WORKING_DIR + "/verrou", "DD_RUN", "DD_CMP.py")
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


if __name__ == "__main__":
    main()
