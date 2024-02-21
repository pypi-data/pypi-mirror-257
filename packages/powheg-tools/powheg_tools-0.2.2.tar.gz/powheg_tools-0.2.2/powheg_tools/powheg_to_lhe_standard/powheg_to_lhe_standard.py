import os
import sys

import pylhe

# Read list of files passed as arguments


if len(sys.argv) < 2:
    print("Usage: %s <lhe files>" % sys.argv[0])
    sys.exit(1)

lhe_files = sys.argv[1:]

# Read the LHE files
for lhe_file in lhe_files:
    events = pylhe.read_lhe_with_attributes(lhe_file)
