import os
import matplotlib.pyplot as plt
import sys

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, '..', '..'))

from quantumsculpt import DensityOfStates
import quantumsculpt as qs

# load the DOSCAR.lobster file via a DensityOfStates class
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'hco_gasphase', 'DOSCAR_alt.lobster')
dos = DensityOfStates(filename)

collections = [{'set': 'all-all'}]
bins = [(-50,0)]

print(qs.integrate_dos_bins(dos, bins, collections))