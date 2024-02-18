import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, '..'))

from quantumsculpt import DensityOfStates, CrystalOrbitalHamiltonPopulation
import quantumsculpt as qs

###
# create a clean DOS for the CO molecule
###############################################################################
filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
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
nsigma = 6
for g in fitres['gaussians']:
    bins.append([g['mu'] - nsigma*g['sigma'], g['mu'] + nsigma*g['sigma']])
bins.append((-35,0))

fig, ax = plt.subplots(2,4, dpi=144, figsize=(14,8))
qs.plot_total_dos(ax[0,0], 
                  dos, 
                  grid=True,
                  bins=bins,
                  ylim=(-25,5),
                  title='Total DOS CO$_{\\text{g}}$')

# specify which collections of projections to plot
collection = [
    {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$\sigma$', 'color': '#FF0000AA', 'style': 'filled'},
    {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$\pi$', 'color': '#0000FFAA', 'style': 'filled'},
    {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$int - \sigma$', 'color': '#FF0000AA', 'style': 'integrated'},
    {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$int - \pi$', 'color': '#0000FFAA', 'style': 'integrated'}
]

qs.plot_gathered_dos(ax[0,1], 
                     dos,
                     collection, 
                     grid=True, 
                     ylim=(-25,5), 
                     legend=True,
                     title='lm-DOS CO$_{\\text{(g)}}$',
                     bins=bins)

collection = [
    {'set': ['all-2s', 'all-2p_x']},
    {'set': ['all-2p_y', 'all-2p_z']}
]

cogasdos = qs.integrate_dos_bins(dos, bins, collection)
# for b in cogasdos:
#     print(b['bin'])
    
#     for i in b['idos']:
#         print('\t', i['set'], i['idos'])

# gather the total number of states for the bins
# print('Bins for gasesous CO')
# for b in qs.integrate_dos_bins(dos, bins):
#     print(b)

filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'COHPCAR.lobster')
cohp = CrystalOrbitalHamiltonPopulation(filename)

sigmaset = qs.cohp_generate_sets('C1', 'O2', ['2s','2p_x'])
piset = qs.cohp_generate_sets('C1', 'O2', ['2p_y','2p_z'])

qs.plot_averaged_cohp(ax[0,2],
                      cohp, 
                      grid=True,
                      bins=bins,
                      ylim=(-25,5),
                      icohp=True,
                      title='Total COHP CO$_{\\text{(g)}}$',
                      legend=True)

# specify which collections of projections to plot
collection = [
    {'set': sigmaset, 
     'legendlabel' : '$\sigma$', 
     'color': '#FF0000AA', 
     'style': 'filled'},
    {'set': piset, 
     'legendlabel' : '$\pi$', 
     'color': '#0000FFAA', 
     'style': 'filled'},
    {'set': sigmaset, 
     'legendlabel' : '$int - \sigma$', 
     'color': '#FF0000AA', 
     'style': 'integrated'},
    {'set': piset, 
     'legendlabel' : '$int - \pi$', 
     'color': '#0000FFAA', 
     'style': 'integrated'}
]

qs.plot_gathered_cohp(ax[0,3],
                      cohp,
                      collections=collection,
                      grid=True,
                      bins=bins,
                      title='Decomposed COHP CO$_{\\text{(g)}}$',
                      ylim=(-25,5),
                      legend=True)


collection = [
    {'set': sigmaset},
    {'set': piset}
]

cohpgasdos = qs.integrate_cohp_bins(cohp, bins, collection)
# for b in cohpgasdos:
#     print(b['bin'])
    
#     for i in b['icohp']:
#         print('\t', i['set'], i['icohp'])

###
# create a clean DOS and COHP for adsorbed CO
###############################################################################

filename = os.path.join('D:/', 'Data', 'Xianxuan', 'COADS', '010', 'DOSCAR.lobster')
dos = DensityOfStates(filename)

# specify where to place the bins for orbital deconvolution
bins = [
    (-22.8,-21.5),
    (-10,-9.4),
    (-7,-5),
    (-5,0),
    (-35,0.0),
]

# specify which collections of projections to plot
collection = [
    {'set': ['57-all','58-all'],
     'legendlabel' : 'total', 
     'color': '#000000AA', 
     'style': 'filled', 
     'stack': True},
    {'set': ['57-all','58-all'], 
     'legendlabel' : 'int total', 
     'color': '#000000FF', 
     'style': 'integrated'},
]

qs.plot_gathered_dos(ax[1,0], 
                     dos, 
                     collection,
                     grid=True,
                     ylim=(-25,5),
                     legend=True,
                     addspins=True,
                     bins=bins,
                     title='Total dos')

sigmaset = qs.dos_generate_sets([57,58], ['2s','2p_x'])
piset = qs.dos_generate_sets([57,58], ['2p_y','2p_z'])

# specify which collections of projections to plot
collection = [
    {'set': sigmaset, 
     'legendlabel' : '$\sigma$', 
     'color': '#FF0000AA', 
     'style': 'filled', 
     'stack': True},
    {'set': piset, 
     'legendlabel' : '$\pi$', 
     'color': '#0000FFAA', 
     'style': 'filled', 
     'stack': True},
    {'set': sigmaset, 
     'legendlabel' : '$int - \sigma$', 
     'color': '#FF0000AA', 
     'style': 'integrated'},
    {'set': piset, 
     'legendlabel' : '$int - \pi$', 
     'color': '#0000FFAA', 
     'style': 'integrated'}
]

qs.plot_gathered_dos(ax[1,1], 
                     dos, 
                     collection,
                     grid=True,
                     ylim=(-25,5),
                     legend=True,
                     addspins=True,
                     bins=bins,
                     title='lm-DOS CO$_{\\text{ads}}$')

collection = [
    {'set': sigmaset},
    {'set': piset}
]

coadsdos = qs.integrate_dos_bins(dos, bins, collection)
# for b in coadsdos:
#     print(b['bin'])
    
#     for i in b['idos']:
#         print('\t', i['set'], i['idos'])

filename = os.path.join('D:/', 'Data', 'Xianxuan', 'COADS', '010', 'COHPCAR.lobster')
cohp = CrystalOrbitalHamiltonPopulation(filename)

qs.plot_averaged_cohp(ax[1,2], 
                      cohp, 
                      grid=True,
                      bins=bins,
                      ylim=(-25,5),
                      icohp=True,
                      title='Total COHP CO$_{\\text{ads}}$',
                      legend=True)

sigmaset = qs.cohp_generate_sets('O58', 'C57', ['2s','2p_x'])
piset = qs.cohp_generate_sets('O58', 'C57', ['2p_y','2p_z'])

# specify which collections of projections to plot
collection = [
    {'set': sigmaset, 
     'legendlabel' : '$\sigma$', 
     'color': '#FF0000AA', 
     'style': 'filled',
     'stack': True},
    {'set': piset, 
     'legendlabel' : '$\pi$', 
     'color': '#0000FFAA', 
     'style': 'filled',
     'stack': True},
    {'set': sigmaset, 
     'legendlabel' : '$int - \sigma$', 
     'color': '#FF0000AA', 
     'style': 'integrated'},
    {'set': piset, 
     'legendlabel' : '$int - \pi$', 
     'color': '#0000FFAA', 
     'style': 'integrated'}
]

qs.plot_gathered_cohp(ax[1,3],
                      cohp,
                      collections=collection,
                      grid=True,
                      bins=bins,
                      title='Decomposed COHP CO$_{\\text{ads}}$',
                      ylim=(-25,5),
                      legend=True)

# specify which collections of projections to plot
collection = [
    {'set': sigmaset},
    {'set': piset}
]

cohpadsdos = qs.integrate_cohp_bins(cohp, bins, collection)
# for b in cohpadsdos:
#     print(b['bin'])
    
#     for i in b['icohp']:
#         print('\t', i['set'], i['icohp'])
          
plt.tight_layout()

fig, ax = plt.subplots(1, 2, dpi=144)

# collect DOS data and visualize it
dosco_sigma_gas = [
    cogasdos[0]['idos'][0]['idos'],
    cogasdos[1]['idos'][0]['idos'],
    cogasdos[2]['idos'][0]['idos'] + cogasdos[3]['idos'][0]['idos'],
    0.0
]
dosco_pi_gas = [
    cogasdos[0]['idos'][1]['idos'],
    cogasdos[1]['idos'][1]['idos'],
    cogasdos[2]['idos'][1]['idos'] + cogasdos[3]['idos'][1]['idos'],
    0.0
]
dosco_sigma_ads = [
    coadsdos[i]['idos'][0]['idos'] for i in range(0,4)
]
dosco_pi_ads = [
    coadsdos[i]['idos'][1]['idos'] for i in range(0,4)
]

ax[0].barh(np.arange(0,4)+0.125, dosco_sigma_gas, height=0.25, color='#AA000055')
ax[0].barh(np.arange(0,4)+0.375, dosco_pi_gas, height=0.25, color='#0000AA55')
ax[0].barh(np.arange(0,4)+0.625, dosco_sigma_ads, height=0.25, color='#AA0000')
ax[0].barh(np.arange(0,4)+0.875, dosco_pi_ads, height=0.25, color='#0000AA')
ax[0].barh(4.125, cogasdos[-1]['idos'][0]['idos'] + cogasdos[-1]['idos'][0]['idos'],
           height=0.25, color='#00000055')
ax[0].barh(4.375, coadsdos[-1]['idos'][0]['idos'] + coadsdos[-1]['idos'][0]['idos'],
           height=0.25, color='#000000')
ax[0].set_ylim(0,4.5)
ax[0].hlines([0,1,2,3,4], 0, 12, linestyle='--', color='black')
ax[0].set_yticks([0.5,1.5,2.5,3.5,4.25], ['$3\sigma$','$4\sigma$','$5\sigma+1\pi$','$2\pi$', 'total'])
ax[0].set_xlim(0,12)
ax[0].set_title('DOS')
ax[0].grid(linestyle='--', color='black', alpha=0.5)
ax[0].set_xlabel('iDOS [-]')

# collect COHP data and visualize it
cohp_sigma_gas = [
    cohpgasdos[0]['icohp'][0]['icohp'],
    cohpgasdos[1]['icohp'][0]['icohp'],
    cohpgasdos[2]['icohp'][0]['icohp'] + cohpgasdos[3]['icohp'][0]['icohp'],
    0.0,
]
cohp_pi_gas = [
    cohpgasdos[0]['icohp'][1]['icohp'],
    cohpgasdos[1]['icohp'][1]['icohp'],
    cohpgasdos[2]['icohp'][1]['icohp'] + cohpgasdos[3]['icohp'][1]['icohp'],
    0.0,
]
cohp_sigma_ads = [
    cohpadsdos[i]['icohp'][0]['icohp'] for i in range(0,4)
]
cohp_pi_ads = [
    cohpadsdos[i]['icohp'][1]['icohp'] for i in range(0,4)
]

ax[1].barh(np.arange(0,4)+0.125, cohp_sigma_gas, height=0.25, color='#AA000055')
ax[1].barh(np.arange(0,4)+0.375, cohp_pi_gas, height=0.25, color='#0000AA55')
ax[1].barh(np.arange(0,4)+0.625, cohp_sigma_ads, height=0.25, color='#AA0000')
ax[1].barh(np.arange(0,4)+0.875, cohp_pi_ads, height=0.25, color='#0000AA')
ax[1].barh(4.125, cohpgasdos[-1]['icohp'][0]['icohp'] + cohpgasdos[-1]['icohp'][1]['icohp'],
           height=0.25, color='#00000055')
ax[1].barh(4.375, cohpadsdos[-1]['icohp'][0]['icohp'] + cohpadsdos[-1]['icohp'][1]['icohp'],
           height=0.25, color='#000000')
ax[1].set_ylim(0,4.5)
ax[1].hlines([0,1,2,3,4], -25, 5, linestyle='--', color='black')
ax[1].set_yticks([0.5,1.5,2.5,3.5,4.25], ['$3\sigma$','$4\sigma$','$5\sigma+1\pi$','$2\pi$', 'total'])
ax[1].set_xlim(-25,5)
ax[1].set_title('COHP')
ax[1].grid(linestyle='--', color='black', alpha=0.5)
ax[1].set_xlabel('iCOHP [-]')

plt.tight_layout()