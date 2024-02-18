import os
import matplotlib.pyplot as plt
import quantumsculpt as qs
from quantumsculpt import DensityOfStates

# load the DOSCAR.lobster file via a DensityOfStates class
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
dos = DensityOfStates(filename)

# try to find perfect peak barriers
energies = dos.get_energies()
totaldos = dos.get_total_dos()['states']

# try to find the peaks via fitting
peaks = qs.find_peaks(energies, totaldos)
fitres = qs.fit_gaussians(energies, totaldos, peaks[1])

# build bins based on Gaussian fit; since the peaks are not true Gaussians,
# there is some wiggle room. Normally 6-sigma woudl correspond to 99.73% of the
# curve, but we need slightly larger values here
bins = []
for g in fitres['gaussians']:
    bins.append([g['mu'] - 5*g['sigma'], g['mu'] + 5*g['sigma']])

# plot the total dos, including the fitted peaks
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

# plot the lm-decomposed DOS according to the collection settings
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