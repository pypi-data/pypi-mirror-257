import argparse
import sys

import yoda


def main():

    parser = argparse.ArgumentParser(description="Rename PDF weights in YODA files")

    # Adding optional argument with default value
    parser.add_argument("files", nargs="+", help="YODA files")
    parser.add_argument("-p", "--pdf", type=int, default=27100, help="PDF number")
    parser.add_argument(
        "-n", "--numMembers", type=int, default=65, help="Number of members"
    )
    parser.add_argument("-s", "--start", type=int, default=8, help="Start index")
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        default=-1,
        help="End index, default is numMembers + start - 2",
    )
    parser.add_argument("--prefix", type=str, default="pdf_", help="Output file prefix")

    args = parser.parse_args()

    pdf = args.pdf
    numMembers = args.numMembers
    start = args.start
    end = args.end if args.end > 0 else numMembers + start - 2
    prefix = args.prefix

    weights = {}
    weights[1] = pdf
    for i in range(start, end + 1):
        weights[i] = i + pdf - start + 1

    for f in sys.argv[1:]:
        map = yoda.read(f)
        nmap = {}

        for k, v in map.items():
            n = k
            h = v
            nmap[k] = v
            for w, p in weights.items():
                n = n.replace(f"[W{w}]", f"[PDF{p}]")
                h.setPath(h.path().replace(f"[W{w}]", f"[PDF{p}]"))
            nmap[n] = h

        yoda.write(nmap, args.prefix + f)
