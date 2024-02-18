import os
import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from quantumsculpt import CrystalOrbitalHamiltonPopulation
import quantumsculpt as qs

# load the COHPCAR.lobster file via a CrystalOrbitalHamiltonPopulation class
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'hco_gasphase', 'COHPCAR.lobster')
cohp = CrystalOrbitalHamiltonPopulation(filename)

# specify which collections of projections to plot
total = qs.cohp_generate_sets('O3', 'C1', ['2s','2p_x','2p_y','2p_z'])
sigmasetcohp = qs.cohp_generate_sets('O3', 'C1', ['2s','2p_x'])
pisetcohp = qs.cohp_generate_sets('O3', 'C1', ['2p_y','2p_z'])
collection = [
    {'set': sigmasetcohp, 
     'legendlabel' : '$\sigma$', 
     'color': qs.colors.red, 
     'style': 'filled',
     'stack': True},
    {'set': pisetcohp, 
     'legendlabel' : '$\pi$', 
     'color': qs.colors.blue, 
     'style': 'filled',
     'stack': True},
    {'set': sigmasetcohp, 
     'legendlabel' : '$int - \sigma$', 
     'color': qs.colors.red, 
     'style': 'integrated'},
    {'set': pisetcohp, 
     'legendlabel' : '$int - \pi$', 
     'color': qs.colors.blue, 
     'style': 'integrated'},
    {'set': total, 
     'legendlabel' : 'total', 
     'color': qs.colors.black, 
     'style': 'integrated'}
]

bins = [
        (-30,0),
]

fig, ax = plt.subplots(1,1, dpi=144)

qs.plot_gathered_cohp(ax,
                      cohp,
                      collections=collection,
                      grid=True,
                      title=r'$\sigma / \pi$-COHP HCO$_{\mathrm{ads}}$',
                      ylim=(-25,5),
                      bins=bins,
                      legend=True)

energies = cohp.get_energies()
data = cohp.get_dataitem(6)['icohp']

ax.plot(data,
        energies,
        color='purple',
        zorder=-1)

collection = qs.cast_to_collection(sigmasetcohp, pisetcohp, total)
cohpint = qs.integrate_cohp_bins(cohp, bins, collection)

print(cohpint)