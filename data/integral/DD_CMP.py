#!/usr/bin/python3
import sys
import argparse


def extractValue(rep):
    with open(rep + "/result.dat") as f:
        lines = f.readlines()
        last_line = lines[-1]
        return float(last_line.split()[1])  # example : get the second column


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verrou DD_CMP commandline")
    parser.add_argument("ref", help="Reference directory of verrou computation")
    parser.add_argument("perturbed", help="Perturbed directory of verrou computation")
    args = parser.parse_args()

    vref = extractValue(args.ref)
    vcur = extractValue(args.perturbed)
    rel = abs((vref - vcur) / vref)
    if rel < 5e-9:
        sys.exit(0)  # OK
    else:
        sys.exit(1)  # KO
