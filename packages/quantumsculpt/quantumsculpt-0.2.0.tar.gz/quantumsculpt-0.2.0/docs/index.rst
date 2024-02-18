QuantumSculpt: Electronic structure analysis
============================================

.. image:: https://anaconda.org/ifilot/quantumsculpt/badges/version.svg
   :target: https://anaconda.org/ifilot/quantumsculpt
.. image:: https://img.shields.io/pypi/v/quantumsculpt?color=green
   :target: https://pypi.org/project/quantumsculpt/
.. image:: https://gitlab.tue.nl/inorganic-materials-chemistry/quantumsculpt/badges/master/pipeline.svg
   :target: https://gitlab.tue.nl/inorganic-materials-chemistry/quantumsculpt/-/commits/master
.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

------------

:program:`QuantumSculpt` is a bundle of Python scripts to analyze the electronic
structure of systems calculated using `VASP <https://www.vasp.at/>`_. QuantumSculpt
is designed to operate on `VASP WAVECAR <https://www.vasp.at/wiki/index.php/WAVECAR>`_ files 
and on the output files of `Lobster <http://www.cohp.de/>`_, specifically DOS and COHP
type of files.

.. grid:: 3

    .. grid-item-card::
      :link: wavefunction_analysis
      :link-type: ref

      **WAVECAR analysis**
      ^^^^^^^^^^^^^^^^^^^^
      Extract one-electron pseudo-wavefunctions and
      build isosurfaces.

    .. grid-item-card::
      :link: dos_analysis
      :link-type: ref

      **DOS analysis**
      ^^^^^^^^^^^^^^^^
      Decompose, collect and visualize density of states.

    .. grid-item-card::
      :link: cohp_analysis
      :link-type: ref

      **COHP analysis**
      ^^^^^^^^^^^^^^^^^
      Analyze and organize crystal orbital hamilton population analysis data.

.. grid:: 3

    .. grid-item-card::
      :link: installation
      :link-type: ref

      **Installation**
      ^^^^^^^^^^^^^^^^
      How to install QuantumSculpt on your computer.

    .. grid-item-card::
      :link: background
      :link-type: ref

      **Background**
      ^^^^^^^^^^^^^^^^
      Background on how QuantumSculpt works and parses the files.

    .. grid-item-card::
      :link: api
      :link-type: ref

      **API**
      ^^^^^^^^^^^^^^^^^
      Analyze and organize crystal orbital hamilton population analysis data.

.. seealso::

  `PyTessel <https://pytessel.imc-tue.nl/>`_ for the generation of isosurfaces from scalar fields.

:program:`QuantumSculpt` has been developed at the Eindhoven University of Technology,
Netherlands. :program:`QuantumSculpt` and its development are hosted on `github
<https://gitlab.tue.nl/inorganic-materials-chemistry/quantumsculpt>`_.  Bugs and feature
requests are ideally submitted via the `gitlab issue tracker
<https://gitlab.tue.nl/inorganic-materials-chemistry/quantumsculpt/-/issues>`_.

.. toctree::
   :maxdepth: 2

   installation
   user_guide/index
   background/index
   api/index
