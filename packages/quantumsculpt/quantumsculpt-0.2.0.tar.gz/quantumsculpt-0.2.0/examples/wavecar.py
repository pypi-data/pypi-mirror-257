import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from pytessel import PyTessel

def main():

    # add a reference to load the module
    ROOT = os.path.dirname(__file__)
    sys.path.append(os.path.join(ROOT, '..'))
    
    from cloudwatcher import Wavecar
    
    filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'WAVECAR_ALIGNED')
    wf = Wavecar(filename, lgamma=True)
    
    unitcell = wf.get_unitcell()
    cgrid = wf.get_grid() * 4 # create a custom grid to enhance the resolution
    psis = []
    
    # produce contour plots
    fig, ax = plt.subplots(2,3, dpi=144, figsize=(8,5))
    for i in range(0,6):
        psi = wf.build_wavefunction(ispin=1, ikpt=1, iband=i+1, norm=True,
                                    ngrid=cgrid, order='zyx')
        psis.append(psi) # store for isosurface generation
        
        row = i//3
        col = i%3
        m_ax = ax[row,col]
        m_ax.imshow(psi[:,psi.shape[1]//2,:].real, interpolation='bicubic',
                           origin='lower', extent=(0,unitcell[0,0],0,unitcell[2,2]),
                           vmin=-0.1, vmax=0.1, cmap='PRGn')
        m_ax.set_xlabel('x [Å]')
        m_ax.set_ylabel('z [Å]')
        m_ax.grid(linestyle='--', color='black', alpha=0.5)
        m_ax.set_title('MO %i' % (i+1))    
        
    plt.tight_layout()
    
    # produce isosurfaces
    for i in range(0,6):
        build_isosurface('co_mo%02i_pos.ply' % (i+1), psis[i].real, unitcell,  0.03)
        build_isosurface('co_mo%02i_neg.ply' % (i+1), psis[i].real, unitcell, -0.03)
    
def build_isosurface(filename, scalarfield, unitcell, isovalue):
    # generate some data
    pytessel = PyTessel()
    vertices, normals, indices = pytessel.marching_cubes(scalarfield.flatten(), scalarfield.shape, unitcell.flatten(), isovalue)
    pytessel.write_ply(filename, vertices, normals, indices)
    
if __name__ == '__main__':
    main()
