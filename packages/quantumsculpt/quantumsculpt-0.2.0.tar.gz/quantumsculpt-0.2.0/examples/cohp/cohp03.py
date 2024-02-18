import os
import matplotlib.pyplot as plt
from quantumsculpt import CrystalOrbitalHamiltonPopulation
import quantumsculpt as qs
import numpy as np

# load the COHPCAR.lobster file via a CrystalOrbitalHamiltonPopulation class
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'COHPCAR.lobster')
cohp = CrystalOrbitalHamiltonPopulation(filename)

# specify which collections of projections to plot
sigmasetcohp = qs.cohp_generate_sets('O2', 'C1', ['2s','2p_x'])
pisetcohp = qs.cohp_generate_sets('O2', 'C1', ['2p_y','2p_z'])
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
     'style': 'integrated'}
]

bins = [
        (-23,-21),
        (-6,-5),
        (-4,-2),
        (-1,1)
]

fig, ax = plt.subplots(1,1, dpi=144)

qs.plot_gathered_cohp(ax,
                      cohp,
                      collections=collection,
                      grid=True,
                      title=r'$\sigma / \pi$-COHP CO$_{\mathrm{ads}}$',
                      ylim=(-25,5),
                      bins=bins,
                      legend=True)

collection = qs.cast_to_collection(sigmasetcohp, pisetcohp)
cohpint = qs.integrate_cohp_bins(cohp, bins, collection)

colors = [qs.colors.red, qs.colors.blue]
for ii in cohpint:
    for key,value in ii.items():
        if key == 'bin':
            print('* %s -> %s' % (key, value))
        else:
            print(' ', key, '->')
    for j,cohpres in enumerate(ii['icohp']):
        for key,value in cohpres.items():
            print('\t%s -> %s' % (key, value))
        if np.abs(cohpres['icohp']) > 0.5:
            # print text twice to artifically create some shadow
            ax.text(5.1, np.average(ii['bin'])-0.1, '%.2f' % cohpres['icohp'], color='black',
                    va='center', fontweight='bold')
            ax.text(5, np.average(ii['bin']), '%.2f' % cohpres['icohp'], color=colors[j],
                    va='center', fontweight='bold')