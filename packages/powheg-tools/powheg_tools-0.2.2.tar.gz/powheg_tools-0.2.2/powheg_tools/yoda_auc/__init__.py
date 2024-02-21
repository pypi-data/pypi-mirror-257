#!/usr/bin/env python3
import argparse

import yoda
from sklearn import metrics


def main():

    argparser = argparse.ArgumentParser(description="Calculate AUC for YODA files")

    # Adding optional argument with default value
    argparser.add_argument("files", nargs="+", help="YODA files")
    argparser.add_argument(
        "-a",
        "--analysis",
        default="ALICE_2020_I1797621",
        help="analysis name to replace",
    )

    args = argparser.parse_args()

    files = args.files
    analysis = args.analysis

    for f in files:
        m = yoda.read(f)
        print(f"{f}:")
        for k, s in m.items():
            v = metrics.auc([p.x() for p in s.points()], [p.y() for p in s.points()])
            k = k.replace(analysis, analysis + ".*")
            print(f' -c "{k} {v}" ', end="")
        print()
