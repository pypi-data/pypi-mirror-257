.. _wavefunction_analysis:
.. index:: wavefunctionanalysis

Wavefunction analysis
=====================

The VASP :code:`WAVECAR` files stores the complete many-electron wave function. By means
of the :code:`Wavecar` class, this file can be read and analyzed and the one-electron 
Kohn-Sham states can be extracted. We here provide a brief overview of the various features.

Extracting Kohn-Sham states from WAVECAR files
----------------------------------------------

To parse the contents of a WAVECAR file, we initialize a :code:`Wavecar` object and
provide the path to the :code:`WAVECAR` file as its argument.

.. code:: python

    import os
    import matplotlib.pyplot as plt
    from quantumsculpt import Wavecar
    import numpy as np

    # add a reference to load the module
    ROOT = os.path.dirname(__file__)
    filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'WAVECAR')
    wf = Wavecar(filename, lgamma=False)

.. important::

    You need to indicate whether the VASP calculation was performed using a Γ-point
    only calculation (i.e. using :code:`vasp_gam`) or not. By default, it is assumed
    the calculation was performed using :code:`vasp_std`. This is the most common
    situation as `Lobster <http://www.cohp.de/>`_ cannot parse Γ-point only calculations.

To extract the Kohn-Sham state, we make use of the function :code:`build_wavefunction` which takes
as input the spin, k-point and band index. Furthermore, we need to specify the ordering of the
grid points as well as the dimensions of the grid. In the code below, we first extract and store
the unitcell matrix used in the calculation. Next, we extract the grid and increase its resolution
by a factor of 4. Using this high-resolution grid, the wave function is extracted for the second
valence orbital of CO. This wave function corresponds to a scalar field whose slowest moving coordinate
is set to :code:`z` and the fastest moving coordinate to :code:`x` as indicated by the :code:`order`
argument.

.. code:: python

    unitcell = wf.get_unitcell()
    grid = wf.get_grid() * 4
    ao = wf.build_wavefunction(1, 1, 2, order='zyx', ngrid=grid)
    dV = wf.get_volume() / np.prod(grid)
    edens = np.einsum('ijk,ijk', ao, ao.conjugate()).real * dV
    print('Total electron density: ', edens)

The extracted wavefunction is normalized, which can be readily proven by integrating the wave
function over the unit cell by means of the following quadrature scheme

.. math::

    I = \int |\psi|^{2} dV \approx \sum_{ijk} |\phi_{ijk}|^{2} \Delta V

wherein :math:`\Delta V` corresponds to the size of a single grid cell as given by

.. math::

    \Delta V = \frac{\Omega}{\prod_{i}N_{i}}

The script as shown above readily shows that the wave function is indeed normalized::

    Total electron density:  1.0000011453787523

Creating contour plots
----------------------

To get an impression of the shape and structure of the wave function, we can readily
study it by projecting the scalar field onto a plane and visualize it. This process
is fairly straightforward. The variable :code:`ao` corresponds to a three-dimensional
(complex-valued) array. By means `slicing <https://numpy.org/doc/stable/user/basics.indexing.html#slicing-and-striding>`_,
we can selectively extract the :math:`xz` plane at the center of the unit cell by means
of :code:`ao[:,grid[1]//2,:]`.

.. note::

    By default, VASP wavefunctions are complex-valued and to get a full impression of the wave function,
    we need to visualize both the real and the imaginary part.

.. code:: python

    from mpl_toolkits.axes_grid1 import make_axes_locatable

    fig, ax = plt.subplots(1,2, dpi=144)

    xx = np.linspace(0, unitcell[0,0], grid[0])
    zz = np.linspace(0, unitcell[2,2], grid[2])

    levels = np.linspace(-2.0,2.0,17)
    im = ax[0].contourf(xx, zz, ao[:,grid[1]//2,:].real, origin='lower',
            extent=(0, unitcell[0,0], 0, unitcell[2,2]),
            vmin=levels[0], vmax=levels[-1],
            cmap='PiYG', levels=levels)
    ax[0].contour(xx, zz, ao[:,grid[1]//2,:].real, origin='lower',
            extent=(0, unitcell[0,0], 0, unitcell[2,2]),
            vmin=levels[0], vmax=levels[-1],
            colors='black', levels=levels,
            linewidths=0.5)

    # create colorbar
    divider = make_axes_locatable(ax[0])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im, cax=cax, orientation='vertical')

    im = ax[1].contourf(xx, zz, ao[:,grid[1]//2,:].imag, origin='lower',
            extent=(0, unitcell[0,0], 0, unitcell[2,2]),
            vmin=levels[0], vmax=levels[-1],
            cmap='PiYG', levels=levels)
    ax[1].contour(xx, zz, ao[:,grid[1]//2,:].imag, origin='lower',
            extent=(0, unitcell[0,0], 0, unitcell[2,2]),
            vmin=levels[0], vmax=levels[-1],
            colors='black', levels=levels,
            linewidths=0.5)

    # create colorbar
    divider = make_axes_locatable(ax[1])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im, cax=cax, orientation='vertical')

    ax[0].set_title('Real part')
    ax[1].set_title('Imaginary part')

    for i in range(0,2):
        ax[i].set_aspect('equal', adjustable='box')
        ax[i].set_xlabel('x-coordinate [Å]')
        ax[i].set_ylabel('z-coordinate [Å]')
    plt.tight_layout()

Execution of the above script yields the following figure.

.. figure:: ../_static/img/wavecar/wavecar00.png

Performing phase mixing
-----------------------

The wave functions are invariant under a multiplication with a complex number

.. math::

    z = \exp \left( i \theta \right)

where :math:`\theta \in (0, 2\pi)`. As such, we aim to find that value :math:`\theta` that
minimizes the objective function :math:`O` as defined by

.. math::

    O = \left(\sum_{ijk} \mathbb{I}\left(\phi_{ijk}\right)^{2}\right) - \left(\sum_{ijk} \mathbb{R}\left(\phi_{ijk}\right)^{2}\right)

where :math:`\mathbb{R}` and :math:`\mathbb{I}` correspond to the real and imaginary parts of a complex number, respectively.
Minimization of :math:`O` yields a wave function that has its real part maximized at the expense of minimizing its imaginary part.
If the imaginary part becomes negligible, we can fully focus on the real part only. The function :code:`optimize_real` has been
designed exactly for this purpose and its use is demonstrated below.

.. code:: python

    import os
    import matplotlib.pyplot as plt
    from quantumsculpt import Wavecar
    import numpy as np
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    import scipy

    # add a reference to load the module
    ROOT = os.path.dirname(__file__)
    filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'WAVECAR')
    wf = Wavecar(filename, lgamma=False)

    # grab data from WAVECAR file
    unitcell = wf.get_unitcell()
    grid = wf.get_grid() * 4
    ao = wf.build_wavefunction(1, 1, 2, order='zyx', ngrid=grid)
    dV = wf.get_volume() / np.prod(grid)

    # optimize real part of wave function
    ao = wf.optimize_real(ao)

    print('Real part: ', np.sum(ao.real**2) * dV)
    print('Imaginary part: ', np.sum(ao.imag**2) * dV)

    # plot the result of the real and imaginary part
    fig, ax = plt.subplots(1,2, dpi=144)

    xx = np.linspace(0, unitcell[0,0], grid[0])
    zz = np.linspace(0, unitcell[2,2], grid[2])

    levels = np.linspace(-2.0,2.0,17)
    im = ax[0].contourf(xx, zz, ao[:,grid[1]//2,:].real, origin='lower',
            extent=(0, unitcell[0,0], 0, unitcell[2,2]),
            vmin=levels[0], vmax=levels[-1],
            cmap='PiYG', levels=levels)
    ax[0].contour(xx, zz, ao[:,grid[1]//2,:].real, origin='lower',
            extent=(0, unitcell[0,0], 0, unitcell[2,2]),
            vmin=levels[0], vmax=levels[-1],
            colors='black', levels=levels,
            linewidths=0.5)

    # create colorbar
    divider = make_axes_locatable(ax[0])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im, cax=cax, orientation='vertical')

    im = ax[1].contourf(xx, zz, ao[:,grid[1]//2,:].imag, origin='lower',
            extent=(0, unitcell[0,0], 0, unitcell[2,2]),
            vmin=levels[0], vmax=levels[-1],
            cmap='PiYG', levels=levels)
    ax[1].contour(xx, zz, ao[:,grid[1]//2,:].imag, origin='lower',
            extent=(0, unitcell[0,0], 0, unitcell[2,2]),
            vmin=levels[0], vmax=levels[-1],
            colors='black', levels=levels,
            linewidths=0.5)

    # create colorbar
    divider = make_axes_locatable(ax[1])
    cax = divider.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(im, cax=cax, orientation='vertical')

    ax[0].set_title('Real part')
    ax[1].set_title('Imaginary part')

    for i in range(0,2):
        ax[i].set_aspect('equal', adjustable='box')
        ax[i].set_xlabel('x-coordinate [Å]')
        ax[i].set_ylabel('z-coordinate [Å]')
    plt.tight_layout()

The output of this script shows that the imaginary part has been made negligible::

    Real part:  1.0000011453787523
    Imaginary part:  5.30889949255125e-16

as can also be readily seen from the plot

.. figure:: ../_static/img/wavecar/wavecar01.png

Limitations of contour plots
----------------------------

Contour plots are great for showing the internal structure of a molecular orbital, yet
the quality and usefulness of such plots greatly depends on how the projection is
made. To illustrate an important limitation of contour plots, we construct the contour
plots of the first six valence molecular orbitals of CO using the script as provided
below.

.. code:: python

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

Execution of this script yields the following figure

.. figure:: ../_static/img/wavecar/co_contour_plots.png

For MO1, MO2, and MO5, the procedure works well, yet for MO3 and MO4, we would expect
very symmetrical results as these two MOs correspond to a degenerate set (the 1π MOs or CO).
Despite the presence of this symmetry, we do observe that MO4 has a lower intensity on the
:math:`xz` plane as compared to MO3. As will become clear from the isosurfaces as shown
below, these differences are caused by the specific orientation of these two MOs.
Because they form a degenerate set (i.e., they have the same eigenvalue), we are allowed to
mix these two orbitals among each other corresponding to an arbitrary rotation around the
C-O bonding axis. Depending on the orientation received from the calculation, we might
get an excellent contour plot for one and a poor one for the other. It remains up to the
user to properly conduct the contourplot projection to get the most out of these pictures.

Creating isosurfaces
--------------------

.. caution::

    Automatic isosurface creation via Blender is only supported on Windows
    and is an **experimental feature**.

In the following example, we will be using :code:`Wavecar` in conjunction with
:code:`BlenderRender` to automatically generate the molecular orbitals of the CO
molecule.

.. code :: python

    import os
    import numpy as np
    from quantumsculpt import Wavecar,BlenderRender

    ROOT = os.path.dirname(__file__)

    # path to WAVECAR and CONTCAR files
    filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'WAVECAR')
    contcar = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'CONTCAR')

    # set output folder and create it if it does not yet exists
    output = os.path.join(ROOT, '..', '..', 'output')
    if not os.path.exists(output):
        os.mkdir(output)

    # load WAVECAR
    wf = Wavecar(filename, lgamma=False)

    # construct BlenderRender object
    br = BlenderRender()

    # render all MOs
    br.render_kohn_sham_state(wf=wf, outpath=ROOT, mo_indices=np.arange(0,wf.get_nbands()),
                            camera='x', contcar=contcar, camera_scale=8, ispin=1,
                            prefix='CO')

Execution of the script above yields 10 :code:`.png` files containing the isosurfaces for the
molecular orbitals of CO as collected in the image below. Note that only the first 5 
orbitals are occupied and because of the frozen core approximation
the core molecular orbitals are not calculated.

.. image:: ../_static/img/orbitals/co_isosurfaces.jpg
   :width: 600

.. tip::

    Using the package :code:`imagemagick`, we can easily collect all :code:`png` files and
    assemble them into one image with the following one-liner

    .. code:: bash

        montage -geometry +5+5 -tile 5x2 CO_{0001..0010}.png co_orbitals.jpg

.. important::

    The unoccupied molecular orbitals do not contribute to the electron density and
    are in that sense more an artifact of the calculation than something that should be
    interpreted with extreme scrutiny.