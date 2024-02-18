.. _cohp_and_dos_analysis:
.. index:: cohpanddosanalysis

Combining COHP and DOS analysis
===============================

Here, we provide an example how one can combine a DOS and COHP analysis
to study the electronic structure of CO on a catalyst material. In this
example, we will focus on CO adsorbed on the Co(0001) surface, which is
a fairly simple model system.

Python script
-------------

.. note::

    * A copy of the script can be found in the :code:`examples`
      folder on the Gitlab repository.
    * The script below is a fairly long script, but it is (hopefully)
      properly documented. Please study it carefully with help of the
      explanation text listed below.

.. literalinclude:: ../../examples/dos_and_cohp/co_Co0001.py
   :caption: examples/dos_and_cohp/co_Co0001.py
   :language: python
   :linenos:

The script as shown above is organized in as follows

* DOS and COHP for gasphase CO
    * Loading of :code:`DOSCAR.lobster` and :code:`COHPCAR.lobster` (lines 18-21)
    * Automatic fitting of the DOS of gaseous CO to establish integration bins (lines 23-29) [:ref:`explanation <peak_integration_via_fitting>`]
    * Building of integration bins (lines 31-35)
    * Creation of DOS and COHP figures (lines 37-115) [:ref:`explanation <peak_integration_via_fitting>`]
    * Performing integration on bins (lines 117-139) [:ref:`explanation <dos_peak_integration>`]
* DOS and COHP for adsorbed CO
    * Loading of :code:`DOSCAR.lobster` and :code:`COHPCAR.lobster` (lines 146-149)
    * Manually specifying the integration bins (lines 152-157) [:ref:`explanation <manual_peak_integration>`]
    * Creation of DOS and COHP figures (lines 160-268)
    * Performing integration on bins (lines 270-282) [:ref:`explanation <dos_peak_integration>`]
* Adjusting DOS and COHP plots (lines 285-294)
* Producing bargraphs of all interactions (lines 300-418)

Result
------

Execution of the above script yields the following two figures.

.. figure:: ../_static/img/dos_and_cohp/dos_and_cohp_plots.png
    
    Figure 1: Density of states and COHP of gaseous and adsorbed CO.

.. figure:: ../_static/img/dos_and_cohp/dos_and_cohp_bargraphs.png
    
    Figure 2: Integrated DOS and COHP, categorized per molecular orbital.

Interpretation
--------------

The density of states of CO can be interpreted by means of considering its canonical
molecular orbitals. Upon adsorption of CO, these canonical molecular orbitals interact
with the d-orbitals of the Co(0001) surface, leading to orbital hybridization.

In Figure 1, the DOS and COHP plots for gaseous and adsorbed CO are shown. Comparison
between the DOS of gaseous CO and its adsorbed configuration reveals that orbital
hybridization leads to peak broadening and energy shifting. To quantitatively describe
this process, the total number of states (i.e. number of electrons) per feature is 
calculated as well as the corresponding total COHP character. The features are
indicated by dashed lines, corresponding to the integration domains.

The result of the integration is shown in Figure 2. From this figure, it can be seen
that CO adsorption leads to a larger accumulation of charge on the CO molecule. This
charge tends to occupy the previously unoccupied orbitals of gaseous CO, which are
anti-bonding in nature. Thus, the total COHP character **increases** indicative for a
destabilization of the C-O bond. Based on this result, it can be rationalized why the
C-O dissociation barrier will be lower over Co(0001) as compared to the gas-phase
dissociation.