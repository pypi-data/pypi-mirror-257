import os
import matplotlib.pyplot as plt
import quantumsculpt as qs
from quantumsculpt import DensityOfStates

# load the DOSCAR.lobster file via a DensityOfStates class
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
dos = DensityOfStates(filename)

# specify where to place the bins for orbital deconvolution
bins = [
    (-23,-21),
    (-6,-5),
    (-3.8,-2.1),
    (-1,1),
]

fig, ax = plt.subplots(1,2, dpi=144, figsize=(8,4))
qs.plot_total_dos(ax[0], 
                  dos, 
                  grid=True, 
                  ylim=(-25,5),
                  title='Total DOS CO(g)',
                  bins=bins)

# specify which collections of projections to plot
collection = [
    {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$\sigma$', 'color': '#FF0000AA', 'style': 'filled'},
    {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$\pi$', 'color': '#0000FFAA', 'style': 'filled'},
    {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$int - \sigma$', 'color': '#FF0000AA', 'style': 'integrated'},
    {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$int - \pi$', 'color': '#0000FFAA', 'style': 'integrated'}
]

qs.plot_gathered_dos(ax[1], 
                     dos,
                     collection, 
                     grid=True, 
                     ylim=(-25,5), 
                     legend=True,
                     title='lm-DOS CO(g)',
                     bins=bins)

# gather the total number of states for the bins
for res in qs.integrate_dos_bins(dos, bins):
    print(res)

plt.tight_layout()