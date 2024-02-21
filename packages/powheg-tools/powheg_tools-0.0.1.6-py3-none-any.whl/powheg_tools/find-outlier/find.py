#!/usr/bin/python

import sys

import numpy as np
import pylhe

abs_max = [(0, 0, "")]

rel_max = [(0, 0, "")]

for arg in sys.argv[1:]:
    for i, event in enumerate(pylhe.read_lhe_with_attributes(arg)):
        # print(event.particles)
        # print(event.weights)
        warr = np.array(list(event.weights.values()))
        warr = warr[7:]
        # print(warr)
        max_difference = np.max(np.abs(np.subtract.outer(warr, warr)))
        # relative difference
        rel_difference = max_difference / np.average(warr)

        if max_difference > abs_max[-1][0]:
            abs_max.append((max_difference, i, arg))
            abs_max.sort(reverse=True, key=lambda x: x[0])
            abs_max = abs_max[:10]
        if rel_difference > rel_max[-1][0]:
            rel_max.append((rel_difference, i, arg))
            rel_max.sort(reverse=True, key=lambda x: x[0])
            rel_max = rel_max[:10]
        # print(i,max_difference)
    # print(pylhe.read_lhe_init(arg))
print(sys.argv[1:])
print("abs_max")
print(abs_max)
print("rel_max")
print(rel_max)
