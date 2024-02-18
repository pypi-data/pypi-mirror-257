import os
import matplotlib.pyplot as plt
import quantumsculpt as qs
from quantumsculpt import DensityOfStates

# load the DOSCAR.lobster file via a DensityOfStates class
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
dos = DensityOfStates(filename)

# plot the total dos, including the fitted peaks
fig, ax = plt.subplots(2,2, dpi=144, figsize=(8,8))
qs.plot_total_dos(ax[0,0], 
                  dos, 
                  grid=True, 
                  ylim=(-25,5),
                  title='Total DOS CO(g)')

# specify which collections of projections to plot
collection = [
    {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$\sigma$', 'color': '#FF0000AA', 'style': 'filled'},
    {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$\pi$', 'color': '#0000FFAA', 'style': 'filled'},
    {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$int - \sigma$', 'color': '#FF0000AA', 'style': 'integrated'},
    {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$int - \pi$', 'color': '#0000FFAA', 'style': 'integrated'}
]

# plot the lm-decomposed DOS according to the collection settings
qs.plot_gathered_dos(ax[0,1], 
                     dos,
                     collection, 
                     grid=True, 
                     ylim=(-25,5), 
                     legend=True,
                     title='lm-DOS CO(g)')

# specify which collections of projections to plot
collection = [
    {'set': ['1-2s', '1-2p_x'], 'legendlabel' : '$\sigma$', 'color': '#FF0000AA', 'style': 'filled'},
    {'set': ['1-2p_y', '1-2p_z'], 'legendlabel' : '$\pi$', 'color': '#0000FFAA', 'style': 'filled'},
    {'set': ['1-2s', '1-2p_x'], 'legendlabel' : '$int - \sigma$', 'color': '#FF0000AA', 'style': 'integrated'},
    {'set': ['1-2p_y', '1-2p_z'], 'legendlabel' : '$int - \pi$', 'color': '#0000FFAA', 'style': 'integrated'}
]

# plot the lm-decomposed DOS according to the collection settings
qs.plot_gathered_dos(ax[1,0], 
                     dos,
                     collection, 
                     grid=True, 
                     xlim=(0,10),
                     ylim=(-25,5), 
                     legend=True,
                     title='lm-DOS carbon atom')

# specify which collections of projections to plot
collection = [
    {'set': ['2-2s', '2-2p_x'], 'legendlabel' : '$\sigma$', 'color': '#FF0000AA', 'style': 'filled'},
    {'set': ['2-2p_y', '2-2p_z'], 'legendlabel' : '$\pi$', 'color': '#0000FFAA', 'style': 'filled'},
    {'set': ['2-2s', '2-2p_x'], 'legendlabel' : '$int - \sigma$', 'color': '#FF0000AA', 'style': 'integrated'},
    {'set': ['2-2p_y', '2-2p_z'], 'legendlabel' : '$int - \pi$', 'color': '#0000FFAA', 'style': 'integrated'}
]

# plot the lm-decomposed DOS according to the collection settings
qs.plot_gathered_dos(ax[1,1], 
                     dos,
                     collection, 
                     grid=True, 
                     xlim=(0,10),
                     ylim=(-25,5), 
                     legend=True,
                     title='lm-DOS oxygen atom')

plt.tight_layout()