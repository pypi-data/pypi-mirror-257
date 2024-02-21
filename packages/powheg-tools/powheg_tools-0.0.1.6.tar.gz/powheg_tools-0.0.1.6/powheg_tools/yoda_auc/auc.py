#!/usr/bin/env python3
import yoda
from sklearn import metrics

for f in ["../alice_pwhg_cc.yoda", "../alice_pwhg_bb.yoda"]:
    m = yoda.read(f)
    print(f"{f}:")
    for k, s in m.items():
        v = metrics.auc([p.x() for p in s.points()], [p.y() for p in s.points()])
        k = k.replace("ALICE_2020_I1797621", "ALICE_2020_I1797621.*")
        print(f' -c "{k} {v}" ', end="")
    print()
