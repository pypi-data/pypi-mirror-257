#!/usr/bin/env python3
import argparse


def main():

    parser = argparse.ArgumentParser(description="Generate powheg seeds")

    # Adding optional argument with default value
    parser.add_argument(
        "--n", "--number", type=int, default=2000, help="number of seeds"
    )
    parser.add_argument("-s", "--start", type=int, default=1, help="start value")
    parser.add_argument("-e", "--end", type=int, default=32768, help="end value")
    parser.add_argument(
        "-o", "--output", type=str, default="pwgseeds.dat", help="output file"
    )

    args = parser.parse_args()

    with open(args.output, "w") as f:
        for i in range(args.start, args.end, int(args.end / args.n)):
            print(i, file=f)


if __name__ == "__main__":
    main()
