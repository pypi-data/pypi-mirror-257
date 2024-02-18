import numpy as np
from ..dos import DensityOfStates
from ..colors import adjust_lightness
import matplotlib.axes
from .plotdecorators import composed, addgrid, addlimits, addlegend, addtitle, addbins
from matplotlib.ticker import MultipleLocator
from scipy.interpolate import CubicSpline

@composed(addgrid, addlimits, addlegend, addtitle, addbins)
def plot_total_dos(ax:matplotlib.axes.Axes,
                   dos:DensityOfStates,
                   addspins:bool=False,
                   **kwargs):
    """
    Plot the total density of states

    Parameters
    ----------
    ax : matplotlib.axes._axes.Axes
        matplotlib axis object
    dos : DensityOfStates
        density of states object
    **kwargs
        Supplementary plotting arguments (see below)

    Raises
    ------
    Exception
        Raises an exception upon unknown spin configuration
    """
    
    if dos.get_spin_state() == 'restricted' or addspins == True:
        __plot_dos(ax,
                   dos.get_total_dos()['energies'],
                   dos.get_total_dos()['states'])
    elif dos.get_spin_state() == 'unrestricted':
        __plot_dos(ax,
                   dos.get_total_dos()['energies'],
                   dos.get_total_dos()['states_up'])
        __plot_dos(ax,
                   dos.get_total_dos()['energies'],
                   -dos.get_total_dos()['states_down'])
    else:
        raise Exception('Unknown spin configuration: %s' % dos.get_spin_state())

@composed(addgrid, addlimits, addlegend, addtitle, addbins)
def plot_gathered_dos(ax:matplotlib.axes.Axes,
                      dos:DensityOfStates,
                      collections:list[dict],
                      addspins=False,
                      **kwargs):
    """
    Create a plot for specific orbital projections

    Parameters
    ----------
    ax : matplotlib.axes._axes.Axes
        matplotlib axis object
    dos : DensityOfStates
        density of states object
    collections : list[dict]
        list of projections to gather (see below)
    addspins : bool, optional
        whether to combine spin-up and spin-down, by default False
    **kwargs
        Supplementary plotting arguments (see below)

    Raises
    ------
    Exception
        Raises exception upon unknown spin configuration
        
    Notes
    -----
    :code:`collections` are a list of dictionaries composed of the following
    keys: `code:`set`, :code:`legendlabel`, :code:`color`, and :code:`style`.
    The :code:`set` item should contain a list of atom-orbital pairs, e.g. :code:`all-2s`,
    :code:`1-2p_x`, :code:`4-3d_z2` and so on. The keyword :code:`all` implies that
    the particular atomic orbital is captured for all atoms in the system.
    """
       
    if dos.get_spin_state() == 'restricted' or addspins == True:
        
        # used for stacked plots
        stack = np.zeros(dos.get_npts(), dtype=np.float32)
        
        for item in collections:
            sumdos = np.zeros(dos.get_npts(), dtype=np.float32)
            
            for i in range(1,dos.get_nr_atoms()+1):
                atomdos = dos.get_dos_atom(i)
                for state in atomdos['states']:
                    if ('%i-%s' % (i,state['label'])) in item['set']:
                        sumdos += state['states']
                        continue
                    if ('all-%s' % (state['label'])) in item['set']:
                        sumdos += state['states']
                        continue
                    if ('%i-all' % i) in item['set']:
                        sumdos += state['states']
                        continue
                    if 'all-all' in item['set']:
                        sumdos += state['states']
                        continue
                    
            __plot_dos(ax, 
                       dos.get_energies(), 
                       sumdos, 
                       color=item['color'],
                       label=item['legendlabel'],
                       style=item['style'] if 'style' in item else None,
                       dosobject = dos,
                       stack=stack)
            
            if 'stack' in item.keys() and item['stack'] == True:
                stack += sumdos
            
    elif dos.get_spin_state() == 'unrestricted':
        
        # used for stacked plots
        stackup = np.zeros(dos.get_npts())
        stackdown = np.zeros(dos.get_npts())
        
        for item in collections:
            sumdosup = np.zeros(dos.get_npts())
            sumdosdown = np.zeros(dos.get_npts())
            
            for i in range(1,dos.get_nr_atoms()+1):
                atomdos = dos.get_dos_atom(i)
                for state in atomdos['states']:
                    if ('%i-%s' % (i,state['label'])) in item['set']:
                        sumdosup += state['states_up']
                        sumdosdown += state['states_down']
                        continue
                    if ('all-%s' % (state['label'])) in item['set']:
                        sumdosup += state['states_up']
                        sumdosdown += state['states_down']
                        continue
                    if ('%i-all' % i) in item['set']:
                        sumdosup += state['states_up']
                        sumdosdown += state['states_down']
                        continue
                    if 'all-all' in item['set']:
                        sumdosup += state['states_up']
                        sumdosdown += state['states_down']
                        continue
                    
            __plot_dos(ax, 
                       dos.get_energies(), 
                       sumdosup, 
                       color=item['color'],
                       label=item['legendlabel'],
                       style=item['style'] if 'style' in item else None,
                       dosobject = dos)
        
            __plot_dos(ax, 
                       dos.get_energies(), 
                       -sumdosdown, 
                       color=item['color'],
                       style=item['style'] if 'style' in item else None,
                       dosobject = dos)
            
            if 'stack' in item.keys() and item['stack'] == True:
                stackup += sumdosup
                stackdown += sumdosdown
    else:
        raise Exception('Unknown spin configuration: %s' % dos.get_spin_state())

def integrate_dos_bins(dos:DensityOfStates,
                       bins:list,
                       collections:list[dict]) -> list[dict]:
    """
    Calculate the total number of states for a list of bins

    Parameters
    ----------
    dos : DensityOfStates
        density of states object
    bins : list
        list of tuples containing lower and upper limits of the bins
    collections : list[dict]
        list of projections to gather (see below)    

    Returns
    -------
    list[dict]
        list of dictionaries containing bin limits and total states per bin
    """
    totaldos = np.zeros((len(collections), dos.get_npts()))
    energies = dos.get_energies()
    
    for j,c in enumerate(collections):
        for i in range(1,dos.get_nr_atoms()+1):
            atomdos = dos.get_dos_atom(i)
            for state in atomdos['states']:
                if ('%i-%s' % (i,state['label'])) in c['set'] or \
                   ('all-%s' % (state['label'])) in c['set'] or \
                   ('%i-all' % i) in c['set'] or \
                    'all-all' in c['set']:
                    totaldos[j,:] += state['states']

    result = []
    for lim in bins:
        result.append({
            'bin' : lim,
            'idos': [],
        })
        
        for i,c in enumerate(collections):
            intdos = np.cumsum(totaldos[i,:]) * dos.get_energy_interval()
            cs = CubicSpline(energies, intdos)
            result[-1]['idos'].append({
                'set': c['set'],
                'idos': cs(lim[1]) - cs(lim[0])
            })
    
    return result

def dos_generate_sets(atomlist:list[int], 
                      orbs:list[str]) -> list[str]:
    """
    Generate a list of atom-orbital pairs

    Parameters
    ----------
    atomlist : list[int]
        list of atoms
    orbs : list[str]
        List of atomic orbitals, e.g. '2s', '2p_x', etc.

    Returns
    -------
    sets : list[str]
        List of atom-orbital interactions

    """
    sets = []
    for a in np.unique(atomlist):
        if a < 1:
            raise Exception('Atom ids need to be larger than 0.')
        for o in np.unique(orbs):
            sets.append('%i-%s' % (a,o))
    return sets

def cast_to_collection(*args) -> list[dict]:
    """
    Convenience function to cast lists of list of atom-orbital pairs into collections

    Parameters
    ----------
    *args
        :code:`*args` can be a list of atom-orbital pairs

    Returns
    -------
    list[dict]
        Formatted set of dictionaries containing integration collections

    """
    return [{'set': a} for a in args]

def __plot_dos(ax:matplotlib.axes.Axes,
               energies:np.ndarray[np.float32],
               dos:np.ndarray[np.float32],
               color='#000000',
               label=None,
               style=None,
               dosobject=None,
               stack=None):
    
    if style is None or style == 'line':
        ax.plot(dos, energies, color=color, label=label)
    elif style == 'filled':
        if stack is not None:
            ax.fill_betweenx(energies, stack, stack + dos, color=color, 
                             label=label, edgecolor=adjust_lightness(color, 0.5),
                             linewidth=0.5)
        else:
            ax.fill_betweenx(energies, 0, dos, color=color, label=label,
                             edgecolor=adjust_lightness(color, 0.5),
                             linewidth=0.5)
    elif style == 'integrated':
        ax.plot(np.cumsum(dos) * dosobject.get_energy_interval(), 
                energies, color=color, linestyle='--', label=label)
    else:
        raise Exception('Unknown keyword style = %s' % style)
        
    ax.set_xlabel('States [-]')
    ax.set_ylabel('Energy $E - E_{f}$ [eV]')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))