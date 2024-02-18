# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import os, sys

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT, '..', '..'))

import quantumsculpt as qs

colornames = []
colors = []
for var in dir(qs.colors):
    if var != 'adjust_lightness' and not var.startswith('__'):
        colornames.append(var)
        colors.append(getattr(qs.colors, var))

plt.figure(dpi=144)
for i in range(0, len(colornames)):
    plt.bar(i, 1.0, width=0.8, color=colors[i])
plt.xticks(np.arange(0, len(colornames)), labels=colornames, rotation=-45)
plt.gca().axes.get_yaxis().set_visible(False)
plt.tight_layout()
plt.savefig('colors.png')