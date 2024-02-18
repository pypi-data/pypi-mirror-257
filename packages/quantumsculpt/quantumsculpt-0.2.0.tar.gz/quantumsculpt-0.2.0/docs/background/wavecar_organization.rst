.. _wavecar_organization:
.. index:: wavecarorganization

Wavecar Organization
====================

This brief document describes how VASP WAVECAR files are organized.

A WAVECAR file is organized in segment, where each segment has a fixed
size, as specified in the header.

.. tip::

    The information here is only served to describe the working of
    :program:`QuantumSculpt`. The :code:`Wavecar` class essentially encapsulates
    this information, releaving the user from having to know such details.

Header
------

Used size: 24 bytes

* Record length: 64 bit double
* Spin configuration: 64 bit double (1 or 2)
* Formatting tag: 64 bit double (e.g. 45200)

Section 0
---------

Used size: 104 bytes

* Number of k-points: 64 bit double
* Number of bands: 64 bit double
* Cut-off energy: 64 bit double
* Unitcell: 9 x 64 bit double (3x3 matrix)
* (Unknown): 64 bit double

Kohn-Sham eigenstate segments
-----------------------------

Every next segment corresponds to the Kohn-Sham (eigen)state for a specific electron
spin, k-point and band index, in that order. These segments are organized as
schematically illustrated by the listing below::

    * SPIN-DOWN (SPIN=1)
      * K-POINT-1
        * k-point header
        * BAND-1
        * BAND-2
        * ..
        * BAND-N
      * K-POINT-2
      * ..
      * K-POINT-N
    * SPIN-UP (SPIN=2)

For example, to find the segment **index** given spin, k-point and band index,
we can use the function as shown below.

.. code:: python

    def __find_record_location(self, ispin:int=1, ikpt:int=1, iband:int=1) -> int:
        self.__check_index(ispin, ikpt, iband)
        
        rec = 2 + (ispin - 1) * self.__nkpts * (self.__nbands + 1) + \
                  (ikpt - 1) * (self.__nbands + 1) + iband
        return rec
  
K-point header
**************  
      
The k-point headers contain the following data items

* Number of plane waves: 64 bit double
* K-point vector: 3 x 64 bit double (3-vector)
* Band description matrix: N x 3 matrix composed of 64 bit doubles

The band description matrix has N rows, one for each band, containing the
following items:

* Eigenvalue (Kohn-Sham energy): 64 bit double
* Unknown (maybe used for 128 bit doubles)
* Occupancy: 64 bit double

Eigenfunction coefficients
**************************

After the k-point header, N band-segments follow which contain the plane-wave
coefficients used in the linear expansion of the Kohn-Sham state. The expansion
coefficients occupy :math:`N_{\textrm{pw}}` entries where each entry size
corresponds to the precision as defined by the formatting tag. For example,
if the formatting tag is :code:`45200`, the entries correspond to 64 bit
complex values (i.e. 32 bits for the real and imaginary part) whereas if the
formatting tag is :code:`45210`, the entries correspond to 128 bit complex
values (i.e. 64 bits for the real and imaginary part).