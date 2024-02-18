import os
import matplotlib.pyplot as plt
from quantumsculpt import Wavecar
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

# add a reference to load the module
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'WAVECAR')
wf = Wavecar(filename, lgamma=False)

# grab data from WAVECAR file
unitcell = wf.get_unitcell()
grid = wf.get_grid() * 4

# plot the result of the real and imaginary part
fig, ax = plt.subplots(2,3, dpi=144, figsize=(8,4))

xx = np.linspace(0, unitcell[0,0], grid[0])
zz = np.linspace(0, unitcell[2,2], grid[2])

levels = np.linspace(-2.0,2.0,17)

for i in range(0,6):
    ao = wf.build_wavefunction(1, 1, i+1, order='zyx', ngrid=grid)
    ao = wf.optimize_real(ao)
    
    row = i//3
    column = i%3
    
    m_ax = ax[row, column]
    
    im = m_ax.contourf(xx, zz, ao[:,grid[1]//2,:].real, origin='lower',
               extent=(0, unitcell[0,0], 0, unitcell[2,2]),
               vmin=levels[0], vmax=levels[-1],
               cmap='PRGn', levels=levels)
    m_ax.contour(xx, zz, ao[:,grid[1]//2,:].real, origin='lower',
               extent=(0, unitcell[0,0], 0, unitcell[2,2]),
               vmin=levels[0], vmax=levels[-1],
               colors='black', levels=levels,
               linewidths=0.5)
    
    m_ax.set_title('MO %i (E =  %f eV)' % (i+1, wf.get_eigenvalue(1, 1, i+1)))
    
    # create colorbar
    divider = make_axes_locatable(m_ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im, cax=cax, orientation='vertical')
    
    m_ax.set_aspect('equal', adjustable='box')
    m_ax.set_xlabel('x-coordinate [Å]')
    m_ax.set_ylabel('z-coordinate [Å]')
    m_ax.grid(linestyle='--', color='black', alpha=0.3)
    m_ax.set_xticks(np.linspace(0,10,6))
    m_ax.set_yticks(np.linspace(0,10,6))
    plt.tight_layout()