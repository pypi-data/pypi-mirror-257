.. _dos_analysis:
.. index:: dosanalysis

DOS analysis
============

.. note::

    All the code examples listed below reside in the :code:`examples` folder and
    act on data files which can be found in the
    :code:`samples` folder. If you cloned the repository, you should be able to
    directly use them from the :code:`examples` folder.

Getting started
---------------

:program:`QuantumSculpt` can perform analysis on DOS files via the :class:`quantumsculpt.DensityOfStates` class
and the plotting routines as part of the :code:`quantumsculpt` module.

To parse the contents of a :code:`DOSCAR.lobster` file, we execute the following

.. code:: python

    import os
    import matplotlib.pyplot as plt
    from quantumsculpt import DensityOfStates
    import quantumsculpt as qs

    # load the DOSCAR.lobster file via a DensityOfStates class
    ROOT = os.path.dirname(__file__)
    filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
    dos = DensityOfStates(filename)

The object :code:`dos` contains the complete contents of the :code:`DOSCAR.lobster` file and can be used
for retrieval of specific data as well as for visualization. For example, to retrieve the energies and
the total density of states, we can use the following

.. code:: python

    print(dos.get_nr_atoms())
    energies = dos.get_energies()
    print(energies.shape, energies[0], energies[-1])
    totaldos = dos.get_total_dos()
    print(totaldos.keys())

The output of the above code is::

    2
    (801,) -30.03755 10.01252
    dict_keys(['energies', 'states', 'istates'])

This output essentially tells us that the :code:`DOSCAR.lobster` file contains 2 atoms and has 801 data points between
the energy interval :math:`E \in (-30.03, 10.01)`. The function :meth:`quantumsculpt.DensityOfStates.get_total_dos` retrieves a dictionary
containing (once more) the energy values, the states per energy and the integrated states. One can directly
use these attributes for visualization purposes.

.. code:: python

    plt.figure(dpi=144, figsize=(4,4))
    plt.plot(totaldos['states'], energies)
    plt.xlabel('States [-]')
    plt.ylabel('Energies $E - E_{f}$ [eV]')
    plt.grid(linestyle='--', alpha=0.5)
    plt.tight_layout()

Alternatively, one can also use one of the plotting routines. These plotting routines are designed such that
they take a Matplotlib axes object as input. This allows the user to easily produce graphs potentially
containing multiple plots. For example, the function :meth:`quantumsculpt.dosplotting.plot_total_dos` can be used to construct
the total density of states for the system under study.

.. code:: python

    fig, ax = plt.subplots(1, 1, dpi=144, figsize=(4,4))
    qs.plot_total_dos(ax, 
                    dos, 
                    grid=True, 
                    ylim=(-25,5),
                    title='Total DOS CO(g)')

.. figure:: ../_static/img/dos/dos00.png

Decompositions and collections
------------------------------

Quite often, the Kohn-Sham states are projected onto spherical harmonics to produce so-called
LM-decomposed density of states. For particular projections, i.e. specific l-states, we wish
to collect the result. A salient example pertains to the identification of the σ and π states
in CO. An example code is provided below.

.. literalinclude:: ../../examples/dos/dos_decomposition.py
   :caption: examples/dos/dos_decomposition.py
   :language: python
   :linenos:

.. figure:: ../_static/img/dos/dos01.png

Collections are captured by an array of dictionaries containing four mandatory keys:

* :code:`set`: which orbitals to collect (by default done for all atoms)
* :code:`legendlabel`: which label to use in the legend of the figure
* :code:`color`: color of the curve
* :code:`style`: which plotting style to use (:code:`filled` or :code:`integrated`)

:code:`sets` herein corresponds to a list of atom-orbital pairs. For example :code:`all-2s` means the `2s`
states for all atoms, whereas :code:`1-2p_x` would imply the :math:`2p_{x}` orbital on the first atom.
Expanding on the previous example, we can for example add two more subplots where we show the σ and π states
for the carbon and oxygen atoms separately.

.. caution::

    We use 1-based counting to refer to any of the atoms and not 0-based counting as is common in Python.
    This convention is chosen to align with the principles used in the :code:`DOSCAR.lobster` and
    :code:`COHPCAR.lobster` files.

.. literalinclude:: ../../examples/dos/dos_collection.py
   :caption: examples/dos/dos_collection.py
   :language: python
   :linenos:

.. figure:: ../_static/img/dos/dos01b.png

.. _dos_peak_integration:

Defining collections
********************

To efficiently build collections, there exist the convenience function 
:meth:`quantumsculpt.dosplotting.dos_generate_sets`
This function takes two lists as input, one for the
atom ids and one for the atomic orbitals. The function effectively construct a single list with
all possible combinations between atoms and orbitals. An example is illustrated below

.. code:: python

    import quantumsculpt as qs
    res = qs.dos_generate_sets([1,2], ['2s','2p_x'])

which results in::

    ['1-2p_x', '1-2s', '2-2p_x', '2-2s']

The function automatically filters out any duplicates in the list.

.. caution::

    Note that there also exists a similar function for COHP collections, although there the
    atoms are defined by a different syntax, i.e. using :code:`C1` or :code:`Co53` instead
    of :code:`1` or :code:`53`, respectively. The reason for this difference is because
    :code:`DOSCAR.lobster` and :code:`COHPCAR.lobster` internally use a different notation
    to refer to the atoms.

Peak integration
----------------

Another common use case is that one wants to determine the number of states under
a given peak or feature. This can be done either manually or semi-automatically.
First, one needs to determine the start and end point of the peaks. This can be
done visually or via peak detection and curve fitting. We explain both methods here.

.. _manual_peak_integration:

Manually
********

Manual characterization of peaks or features is as simple as specifying the starting
and ending position of the peaks and collecting this as a list of tuples. An example
is shown below.

.. literalinclude:: ../../examples/dos/dos_manual_integration.py
   :caption: examples/dos/dos_manual_integration.py
   :language: python
   :linenos:

.. figure:: ../_static/img/dos/dos02.png

By means of the argument :code:`bins` in the plot functions, we can place horizontal dashed bars to indicate
the peak feature. Next, using the function :meth:`quantumsculpt.dosplotting.integrate_dos_bins`, we can integrate the curve 
under the peaks. The result of the integration is::

     -  (-23, -21) : 
        * ['all-2s', 'all-2p_x']
        1.999998
        * ['all-2p_y', 'all-2p_z']
        0.000000
    -  (-6, -5) : 
        * ['all-2s', 'all-2p_x']
        1.995910
        * ['all-2p_y', 'all-2p_z']
        0.000000
    -  (-3.8, -2.1) : 
        * ['all-2s', 'all-2p_x']
        0.000000
        * ['all-2p_y', 'all-2p_z']
        3.999998
    -  (-1, 1) : 
        * ['all-2s', 'all-2p_x']
        1.999999
        * ['all-2p_y', 'all-2p_z']
        0.000000

.. _peak_integration_via_fitting:

Curve fitting
*************

For DOS plots that are not overly complicated, we can also use semi-automatic peak recognition.
This is two-fold technique wherein first the peaks are being recognized after which the whole
DOS is fitted using a series of Gaussians located at the peak centers. The process is shown
in the example below.

.. literalinclude:: ../../examples/dos/dos_curve_fitting.py
   :caption: examples/dos/dos_curve_fitting.py
   :language: python
   :linenos:

.. figure:: ../_static/img/dos/dos03.png

Using automatic feature identification, we find the following number of states per feature::

     -  [-22.626335623790915, -21.4200722585416] : 
        * ['all-2s', 'all-2p_x']
        1.999819
        * ['all-2p_y', 'all-2p_z']
        0.000000
    -  [-6.129236176698422, -4.922973408465538] : 
        * ['all-2s', 'all-2p_x']
        1.999913
        * ['all-2p_y', 'all-2p_z']
        0.000000
    -  [-3.396237044370418, -2.1899713645634704] : 
        * ['all-2s', 'all-2p_x']
        0.000000
        * ['all-2p_y', 'all-2p_z']
        3.999693
    -  [-0.6319410487346064, 0.5743319400054774] : 
        * ['all-2s', 'all-2p_x']
        1.999886
        * ['all-2p_y', 'all-2p_z']
        0.000000
    -  [8.511941126548892, 9.7186835158897] : 
        * ['all-2s', 'all-2p_x']
        0.097054
        * ['all-2p_y', 'all-2p_z']
        3.999635

.. note ::

    The width of the peaks remains a bit of tuning on the side of the user. Normally, you would
    expect that :math:`\mu \pm 3\sigma` would constitute about 99.73% of the peak area, but in
    the example above, we needed to use :math:`\mu \pm 5\sigma`.