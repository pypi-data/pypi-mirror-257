#!/usr/bin/env python3
import argparse
import os


def main():

    parser = argparse.ArgumentParser(description="Clean up powheg directory")

    # Adding optional argument with default value
    parser.add_argument(
        "--path", default=".", type=str, help="path to powheg directory"
    )

    args = parser.parse_args()

    # remove single file
    for f in [
        "bornequiv",
        "pwg-btlgrid.top",
        "pwggrid.dat",
        "pwgubound.dat",
        "realequivregions-btl",
        "FlavRegList",
        "pwgborngrid.top",
        "pwgcounters.dat",
        "pwghistnorms.top",
        "pwgxgrid.dat",
        "realequivregions-rad",
        "pwgboundviolations.dat",
        "pwgevents.lhe",
        "pwg-stat.dat",
        "pwhg_checklimits",
        "virtequiv",
        "parameters.ol",
    ]:
        p = os.path.join(args.path, f)
        if os.path.exists(p):
            os.remove(p)
    # remove parallel run files
    # TODO


if __name__ == "__main__":
    main()
