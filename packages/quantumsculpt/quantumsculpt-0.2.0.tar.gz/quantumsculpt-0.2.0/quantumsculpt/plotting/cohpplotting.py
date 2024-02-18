import numpy as np
from ..cohp import CrystalOrbitalHamiltonPopulation
from ..colors import adjust_lightness
import matplotlib.axes
from .plotdecorators import composed, addgrid, addlimits, addlegend, addtitle, addbins
from matplotlib.ticker import MultipleLocator
from scipy.interpolate import CubicSpline

@composed(addgrid, addlimits, addlegend, addtitle, addbins)
def plot_averaged_cohp(ax:matplotlib.axes.Axes,
                       cohp:CrystalOrbitalHamiltonPopulation,
                       icohp=False,
                       **kwargs):
    """
    Plot averaged COHP plot for the COHPCAR.lobster file

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Matplotlib axes object
    cohp : CrystalOrbitalHamiltonPopulation
        COHP object
    icohp : TYPE, optional
        Whether to also show the integrated COHP. Default is False.
    **kwargs : TYPE
        Supplementary plotting arguments

    Returns
    -------
    None.

    """
    __plot_cohp(ax,
                cohp.get_energies(),
                cohp.get_average_cohp()['cohp'],
                label='cohp')
    
    if icohp:
        __plot_cohp(ax,
                    cohp.get_energies(),
                    cohp.get_average_cohp()['icohp'],
                    linestyle='--',
                    label='icohp')
        
def cohp_generate_sets(atom1, atom2, orbs):
    sets = []
    for o1 in orbs:
        for o2 in orbs:
            sets.append('%s[%s]->%s[%s]' % (atom1, o1, atom2, o2))
            sets.append('%s[%s]->%s[%s]' % (atom2, o1, atom1, o2))
    return sets
      
@composed(addgrid, addlimits, addlegend, addtitle, addbins)  
def plot_gathered_cohp(ax:matplotlib.axes.Axes,
                       cohp:CrystalOrbitalHamiltonPopulation,
                       collections:list[dict],
                       **kwargs):
    """
    Generate COHP plots for specific collections

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Matplotlib axes object
    cohp : CrystalOrbitalHamiltonPopulation
        COHP object.
    collections : list[dict]
        List of collection (see below)
    **kwargs
        Supplementary plotting arguments (see below)

    Returns
    -------
    None.

    """
    
    for item in collections:
        cohps = np.zeros(cohp.get_npts())
        for s in item['set']:
            for cohpdata in cohp.get_dataitems():
                if cohpdata['label'] == s:
                    cohps += cohpdata['icohp'] if item['style'] == 'integrated' else cohpdata['cohp']

        __plot_cohp(ax,
                    cohp.get_energies(),
                    cohps,
                    color=item['color'],
                    style='line' if item['style'] == 'integrated' else item['style'],
                    linestyle='--' if item['style'] == 'integrated' else '-',
                    label=item['legendlabel'])

def integrate_cohp_bins(cohp:CrystalOrbitalHamiltonPopulation,
                       bins:list,
                       collections:list[dict]) -> list[dict]:
    """
    Integrate the COHP for a list of bins

    Parameters
    ----------
    cohp : CrystalOrbitalHamiltonPopulation
        cohp object
    bins : list
        list of tuples containing lower and upper limits of the bins
    collections : list[dict]
        list of projections to gather (see below)

    Returns
    -------
    list[dict]
        list of dictionaries containing bin limits and total cohp per bin
    """
    energies = cohp.get_energies()
    icohps = np.zeros((len(collections), cohp.get_npts()))
    
    for i,item in enumerate(collections):
        for s in item['set']:
            for cohpdata in cohp.get_dataitems():
                if cohpdata['label'] == s:
                    icohps[i,:] += cohpdata['icohp']

    result = []
    for b in bins:
        result.append({
            'bin' : b,
            'icohp': [],
        })
        
        for i,item in enumerate(collections):
            cs = CubicSpline(energies, icohps[i])
            
            result[-1]['icohp'].append({
                'set': item['set'],
                'icohp' : cs(b[1]) - cs(b[0]),
            })
    
    return result

def __plot_cohp(ax:matplotlib.axes._axes.Axes,
                energies:np.ndarray[np.float32],
                cohpvalues:np.ndarray[np.float32],
                color='#000000',
                label=None,
                style=None,
                linestyle=None,
                dosobject=None):
    
    if linestyle is None:
        linestyle = '-'
       
    if style is None or style == 'line':
        ax.plot(cohpvalues, energies, color=color, label=label, 
                linestyle=linestyle)
    elif style == 'filled':
        ax.fill_betweenx(energies, 0, cohpvalues, color=color, 
                         label=label, linestyle=linestyle,
                         edgecolor=adjust_lightness(color, 0.5),
                         linewidth=0.5)
    else:
        raise Exception('Unknown keyword style = %s' % style)
        
    ax.set_xlabel('COHP [-]')
    ax.set_ylabel('Energy $E - E_{f}$ [eV]')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))