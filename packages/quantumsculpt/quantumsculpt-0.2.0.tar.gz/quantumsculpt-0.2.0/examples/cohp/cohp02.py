import os
import matplotlib.pyplot as plt
from quantumsculpt import CrystalOrbitalHamiltonPopulation
import quantumsculpt as qs
import matplotlib


# load the COHPCAR.lobster file via a CrystalOrbitalHamiltonPopulation class
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'COHPCAR.lobster')
cohp = CrystalOrbitalHamiltonPopulation(filename)

# list collections
collections = []
cmap = matplotlib.colormaps['Spectral']
ctr = 0
for o1 in ['2s', '2p_x', '2p_y', '2p_z']:
    for o2 in ['2s', '2p_x', '2p_y', '2p_z']:
        collections.append({
            'set': ['O2[%s]->C1[%s]' % (o1,o2)], 
            'legendlabel' : r'O2[%s] $\rightarrow$ C1[%s]' % (o1.replace('_', ''),o2.replace('_', '')), 
            'color': cmap(float(ctr) / 15),
            'style': 'filled',
            'stack': True
        })
        ctr += 1

fig, ax = plt.subplots(1,1, dpi=144, figsize=(9,6))

qs.plot_gathered_cohp(ax,
                      cohp,
                      collections=collections,
                      grid=True,
                      title=r'$\sigma / \pi$-COHP CO$_{\mathrm{ads}}$',
                      ylim=(-25,5),
                      legend=True)