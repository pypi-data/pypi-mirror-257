.. _installation:
.. index:: Installation

Installation
============



:program:`QuantumSculpt` is available via an Anaconda package as well as a PyPi package. Because
:program:`QuantumSculpt` is a pure-Python program, it runs natively on Windows, Linux and MacOS.
Pick your favorite package manager and install :program:`QuantumSculpt` using one of the commands
as listed below.

Anaconda
--------

.. image:: https://anaconda.org/ifilot/quantumsculpt/badges/version.svg
   :target: https://anaconda.org/ifilot/quantumsculpt

.. code:: bash

    conda install -c ifilot quantumsculpt

PyPi
----

.. image:: https://img.shields.io/pypi/v/quantumsculpt?color=green
   :target: https://pypi.org/project/quantumsculpt/

.. code:: bash

    pip install quantumsculpt

Check installation
------------------

To check that :program:`QuantumSculpt` is correctly installed, runs

.. code:: python

    import quantumsculpt as qs
    print(qs.__version__)