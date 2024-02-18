import numpy as np
import numpy.typing as npt
import scipy
from .constants import *

class Wavecar:
    """
    Class to parse VASP WAVECAR files

    :code:`WAVECAR` files can be read using the :code:`Wavecar` class. Upon construction 
    of a :code:`Wavecar` class, one needs to specify whether the WAVECAR is generated 
    in a gamma-point only calculation.
    """
    def __init__(self, filename:str, lgamma=False, gamma_half:str='x'):
        """
        Construct Wavecar object

        Parameters
        ----------
        filename : str
            path to file
        lgamma : bool, optional
            whether WAVECAR is generated using gamma calculation, by default False
        gamma_half : str, optional
            folding axis used in gamma calculation, by default 'x'
            
        Notes
        -----
        * One-electron wave functions can be extracted using the 
          :meth:`build_wavefunction` method.
        * One needs to specify a triplet of indices to select the desired Kohn-Sham state to extract,
          corresponding to the spin, k-point and band index. For a spin-restricted calculation using
          only a single k-point, the first two indices will be set to :code:`1`. For a spin-polarized
          calculation, the spin index can hold a value of :code:`1` or :code:`2`, for the spin-up and
          spin-down configurations, respectively.
        """
        self.__lgamma = lgamma
        self.__gamma_half = gamma_half.lower()
        self.__filename = filename
        self.__lsoc = False
        self.__read_wavecar()

    def get_recl(self) -> int:
        """
        Get number of bytes per record

        Returns
        -------
        int
            number of bytes per record
        """
        return self.__recl

    def get_nspin(self) -> int:
        """
        Get number of spin configurations

        Returns
        -------
        int
            Number of spin configurations, 1 for spin-restricted, 2 for spin-unrestricted (spin-polarized)
        """
        return self.__nspin
    
    def get_rtag(self) -> int:
        """
        Get the VASP formatting tag

        * 45200 : VASP4 with 64 bit complex
        * 45210 : VASP4 with 128 bit complex
        * 53300 : VASP5 with 32 bit floats
        * 53310 : VASP5 with 64 bit floats

        Returns
        -------
        int
            Tag specifying WAVECAR format
        """
        return self.__rtag

    def get_eigenvalue(self, ispin:int=1, ikpt:int=1, iband:int=1) -> float:
        """
        Get the Kohn-Sham eigenvalue

        Parameters
        ----------
        ispin : int, optional
            Spin index. The default is 1.
        ikpt : int, optional
            K-point index. The default is 1.
        iband : int, optional
            Band index. The default is 1.

        Returns
        -------
        float
            DESCRIPTION.

        """
        self.__check_index(ispin, ikpt, iband)
        
        return self.__bands[ispin-1, ikpt-1, iband-1]

    def get_precision(self) -> str:
        """
        Get data type of the values

        Returns
        -------
        str
            Description of the variables
        """
        if self.__prectype == np.complex64:
            return "Single precision, 64 bit complex values"
        elif self.__prectype == np.complex128:
            return "Double precision, 128 bit complex values"
        
    def get_encut(self) -> float:
        """
        Get cut-off energy

        Returns
        -------
        float
            Cut-off energy in eV
        """
        return self.__encut
    
    def get_unitcell(self) -> Array3x3[float]:
        """
        Get the unit cell

        Returns
        -------
        Array3x3[float]
            Unitcell matrix (encoded in row-space)
        """
        return self.__unitcell
    
    def get_nbands(self) -> int:
        """
        Get the number of bands

        Returns
        -------
        int
            Number of bands
        """
        return self.__nbands
    
    def get_nkpoints(self) -> int:
        """
        Get the number of k-points

        Returns
        -------
        int
            Number of k-points
        """
        return self.__nkpts
    
    def get_grid(self) -> Array3[int]:
        """
        Get the grid

        Returns
        -------
        Array3[int]
            3-vector containing grid dimensions (nz, ny, nx)
        """
        return self.__ngrid
    
    def get_occupancies(self) -> npt.NDArray[float]:
        """
        Get the Kohn-Sham state occupancies

        Returns a three-dimensional array with the occupancies per spin state,
        k-point and band.

        Returns
        -------
        npt.NDArray[float]
            Occupancies of the Kohn-Sham state per spin-state, k-point and band
        """
        return self.__occs
    
    def get_nrplanewaves(self) -> npt.NDArray[float]:
        """
        Get the number of plane waves per k-point

        Returns a one-dimensional array with the number of plane waves per k-point

        Returns
        -------
        npt.NDArray[float]
            Number of plane waves per k-point
        """
        return self.__nplws

    def get_volume(self) -> float:
        """
        Get the unitcell volume

        Corresponds to the determinant of the unitcell matrix

        Returns
        -------
        float
            Unitcell volume
        """
        return self.__omega

    def build_wavefunction(self, ispin:int=1, ikpt:int=1, iband:int=1,
                           kr_phase:bool=False, ngrid:None|Array3=None, 
                           norm:bool=True, r0=[0.0, 0.0, 0.0], order='xyz') -> npt.NDArray[np.float64]:
        """
        Build a pseudo wave function which can be used for visualization purposes

        Parameters
        ----------
        ispin : int, optional
            spin index, by default 1
        ikpt : int, optional
            k-point index, by default 1
        iband : int, optional
            band index, by default 1
        kr_phase : bool, optional
            phase value (float), by default False
        ngrid : _type_, optional
            grid dimensions, by default None
        r0 : list, optional
            Bloch-wave offset, by default [0.0, 0.0, 0.0]
        order : str, optional
            scalar field ordering ('xyz' or 'zyx'), by default 'xyz'

        Returns
        -------
        npt.NDArray[np.float64]
            three-dimensional scalarfield

        Raises
        ------
        Exception
            When unknown order description is given
            
        Notes
        -----
        * For isosurface construction with PyTessel, one needs to use :code:`order='zyx'
        * This function perform automatic normalization by which the scalar field :math:`\psi` 
          is such that :math:`|\psi|^{2}` corresponds to the **electron density** at the
          grid points ensuring that the following identity holds
          
          .. math ::
          
            N = \sum_{ijk} |\psi_{ijk}|^{2} \Delta V_{ijk} = 1
            
          where :math:`\Delta V_{ijk}` corresponds to the volume of a single grid cell as given by
          
          .. math ::
          
            \Delta V_{ijk} = \\frac{\Omega}{N_{x}N_{y}N_{z}}
        
        * The grid dimensions can be larger than the one stored in the WAVECAR. The resulting
          scalar field is automatically expanded to the larger grid. This can be useful for
          isosurface rendering.
            
        """
        psi = self.read_pseudo_wavefunction(ispin=ispin, 
                                            ikpt=ikpt, 
                                            iband=iband,
                                            norm=norm,
                                            rescale=True,
                                            kr_phase=kr_phase,
                                            ngrid=ngrid, 
                                            r0 =r0)
        
        if ngrid is None:
            ngrid = self.__ngrid
        
        # by diving by the cell volume, we get correct electron densities
        cellvolume = self.__omega / np.prod(ngrid)
        psi /= np.sqrt(cellvolume)
        
        if order == 'xyz':
            return psi
        elif order == 'zyx':
            return np.moveaxis(psi, [0,1,2], [2,1,0])
        else:
            raise Exception('Unknown order: %s. Use "xyz" or "zyx".' % order)

    def optimize_real(self, ao:npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """
        Mix real and imaginary parts of the complex-valued scalar field such that the imaginary part becomes negligble

        Parameters
        ----------
        ao : npt.NDArray[np.float64]
            wave function scalar field

        Returns
        -------
        npt.NDArray[np.float64]
            transformed wave function
        """
        
        # define objective function
        def f(angle, ao):
            phase = np.exp(-1j * angle)
            
            r = np.sum((ao * phase).real**2)
            i = np.sum((ao * phase).imag**2)
            
            return i - r

        # minimize the objective function such that the imaginary part becomes
        # negligible compared to the real part
        res = scipy.optimize.minimize(f, np.pi, args=(ao))
        
        return ao * np.exp(-1j * res.x)

    def read_pseudo_wavefunction(self, ispin:int=1, ikpt:int=1, iband:int=1,
                                 norm:bool=False, kr_phase:bool=False,
                                 rescale=True, ngrid:None|Array3=None, 
                                 r0=[0.0, 0.0, 0.0]) -> npt.NDArray[np.float64]:
        """
        Extract pseudo wave function from WAVECAR

        Parameters
        ----------
        ispin : int, optional
            spin index, by default 1
        ikpt : int, optional
            k-point index, by default 1
        iband : int, optional
            band index, by default 1
        norm : bool, optional
            whether to normalize the scalar field, by default False
        kr_phase : bool, optional
            phase factor, by default False
        rescale : bool, optional
            whether to rescale scalar field, by default True
        ngrid : None or Array3, optional
            grid dimensions, by default None
        r0 : list, optional
            Bloch-wave offset, by default [0.0, 0.0, 0.0]

        Returns
        -------
        npt.NDArray[np.float64]
            three-dimensional scalar field with the **total** electron density per grid cell
            
        Notes
        -----
        * This is an exposed lower-level function for speciality purposes. For normal use
          cases, it suffices to use :code:`build_wavefunction`.
        * :code:`norm=True` performs intermediate plane-wave normalization such that

          .. math ::
            
            \sqrt{\sum_{ijk} c_{ijk}^{2}} = 1
            
          by which
            
          .. math ::
            \sum_{ijk} | \phi_{ijk} | ^ 2 = 1
            
        * Assuming the plane-waves are normalized (see item above), :code:`rescale=True` is used such that
        
          .. math ::
            \sum_{ijk} | \psi_{ijk} | ^ 2 = 1
            
          In other words, the values of the scalar field :math:`\psi` are such that :math:`|\psi|^{2}`
          corresponds to the total electron density per grid cell. This is **not** the same as the electron density.
        
        * The grid dimensions can be larger than the one stored in the WAVECAR. The resulting
          scalar field is automatically expanded to the larger grid. This can be useful for
          isosurface rendering.
          
        """
        self.__check_index(ispin, ikpt, iband)

        # construct grid
        if ngrid is None:
            ngrid = self.__ngrid.copy() * 2
        else:
            ngrid = np.array(ngrid, dtype=int)
            assert ngrid.shape == (3,)
            assert np.alltrue(ngrid >= self.__ngrid), \
                "Minium FT grid size: (%d, %d, %d)" % \
                (self.__ngrid[0], self.__ngrid[1], self.__ngrid[2])

        # By default, the WAVECAR only stores the periodic part of the Bloch
        # wavefunction. In order to get the full Bloch wavefunction, one need to
        # multiply the periodic part with the phase: exp(i k (r + r0). Below, the
        # k-point vector and the real-space grid are both in the direct
        # coordinates.
        if kr_phase:
            phase = np.exp(1j * np.pi * 2 * np.sum(self._kvecs[ikpt-1] * \
                        (np.mgrid[0:ngrid[0], 0:ngrid[1], 0:ngrid[2]].reshape((3, np.prod(ngrid))).T / \
                        ngrid.astype(float) + np.array(r0, dtype=float)), axis=1)).reshape(ngrid)
        else:
            phase = 1.0

        if rescale:
            normfac = np.sqrt(np.prod(ngrid))
        else:
            normfac = 1.0

        # calculate reciprocal lattice vectors
        gvec = self.__gvectors(ikpt)

        # fix grid depending on whether it is a gamma point calculation
        if self.__lgamma:
            if self.__gamma_half == 'z':
                phi_k = np.zeros(
                    (ngrid[0], ngrid[1], ngrid[2]//2 + 1), dtype=np.complex128)
            else:
                phi_k = np.zeros(
                    (ngrid[0]//2 + 1, ngrid[1], ngrid[2]), dtype=np.complex128)
        else:
            phi_k = np.zeros(ngrid, dtype=np.complex128)

        gvec %= ngrid[np.newaxis, :]

        # extract linear expansion coefficients of the plane waves
        phi_k[gvec[:, 0], gvec[:, 1], gvec[:, 2]] = \
            self.__read_band_coefficients(ispin, ikpt, iband, norm)

        if self.__lgamma:
            if self.__gamma_half == 'z':
                for ii in range(ngrid[0]):
                    for jj in range(ngrid[1]):
                        fx = ii if ii < ngrid[0] // 2 + \
                            1 else ii - ngrid[0]
                        fy = jj if jj < ngrid[1] // 2 + \
                            1 else jj - ngrid[1]
                        if (fy > 0) or (fy == 0 and fx >= 0):
                            continue
                        phi_k[ii, jj, 0] = phi_k[-ii, -jj, 0].conjugate()

                # VASP add a factor of SQRT2 for G != 0 in Gamma-only VASP
                phi_k /= np.sqrt(2.)
                phi_k[0, 0, 0] *= np.sqrt(2.)

                return np.fft.irfftn(phi_k, s=ngrid) * normfac
            
            elif self.__gamma_half == 'x':
                for jj in range(ngrid[1]):
                    for kk in range(ngrid[2]):
                        fy = jj if jj < ngrid[1] // 2 + \
                            1 else jj - ngrid[1]
                        fz = kk if kk < ngrid[2] // 2 + \
                            1 else kk - ngrid[2]
                        if (fy > 0) or (fy == 0 and fz >= 0):
                            continue
                        phi_k[0, jj, kk] = phi_k[0, -jj, -kk].conjugate()

                phi_k /= np.sqrt(2.)
                phi_k[0, 0, 0] *= np.sqrt(2.)
                phi_k = np.swapaxes(phi_k, 0, 2)
                tmp = np.fft.irfftn(phi_k, s=(ngrid[2], ngrid[1], ngrid[0])) * normfac
                
                return np.swapaxes(tmp, 0, 2)
        else:
            return np.fft.ifftn(phi_k * normfac) * phase

    def __read_wavecar(self) -> None:
        """
        Parse WAVECAR file and store header information
        
        Returns
        -------
        None.
        """
        with open(self.__filename, 'rb') as f:
            self.__recl, self.__nspin, self.__rtag = \
                np.array(np.fromfile(f, dtype=np.float64, count=3),
                         dtype=np.int64)
                
            f.seek(self.__recl)
            headerdata = np.fromfile(f, dtype=np.float64, count=12)
    
        self.__parse_rtag()
        self.__nkpts = int(headerdata[0])   # Number of kpoints
        self.__nbands = int(headerdata[1])  # Number of bands
        self.__encut = float(headerdata[2]) # ENCUT value
        
        # real space supercell basis
        self.__unitcell = headerdata[3:].reshape((3, 3))
        
        # real space supercell volume
        self.__omega = np.linalg.det(self.__unitcell)
        
        # reciprocal space supercell volume
        self.__bcell = np.linalg.inv(self.__unitcell).T

        # minimum FFT grid size
        anorm = np.linalg.norm(self.__unitcell, axis=1)
        self.__cutoff = np.ceil(
            np.sqrt(self.__encut / RYTOEV) / (TPI / (anorm / AUTOA))
        )
        self.__ngrid = np.array(2 * self.__cutoff + 1, dtype=int)
        
        # create container objects
        self.__nplws = np.zeros(self.__nkpts, dtype=int)         # number of plane waves per k-point
        self.__kvecs = np.zeros((self.__nkpts, 3), dtype=float)  # k-vectors per k-point
        self.__bands = np.zeros((self.__nspin, self.__nkpts, self.__nbands), dtype=float) # bands (KS-states)
        self.__occs = np.zeros((self.__nspin, self.__nkpts, self.__nbands), dtype=float)  # occpancies

        # read Kohn-Sham eigenstates
        with open(self.__filename, 'rb') as f:
            for i in range(self.__nspin):       # loop over spin states
                for j in range(self.__nkpts):   # loop over k-points
                    rec = self.__find_record_location(i+1, j+1, 1) - 1
                    
                    f.seek(rec * self.__recl)
                    data = np.fromfile(f, dtype=np.float64, count=4+3*self.__nbands)
                    
                    if i == 0:
                        self.__nplws[j] = int(data[0])
                        self.__kvecs[j] = data[1:4]
                    
                    data = data[4:].reshape((-1, 3))
                    self.__bands[i, j, :] = data[:, 0]
                    self.__occs[i, j, :] = data[:, 2]
    
        if self.__nkpts > 1:
            tmp = np.linalg.norm(np.dot(np.diff(self.__kvecs, axis=0), self.__bcell), axis=1)
            self.__kpath = np.concatenate(([0, ], np.cumsum(tmp)))
        else:
            self.__kpath = None
        
    def __parse_rtag(self):
        # depending on record tag, set the precision of the WAVECAR
        if self.__rtag == 45200:
            self.__prectype = np.complex64
        elif self.__rtag == 45210:
            self.__prectype = np.complex128
        elif self._rtag == 53300:
            raise ValueError("VASP5 WAVECAR format, not implemented yet")
        elif self._rtag == 53310:
            raise ValueError("VASP5 WAVECAR format with double precision coefficients, not implemented yet")
        else:
            raise ValueError("Unknown TAG value: {}".format(self.__rtag))
            
    def __find_record_location(self, ispin:int=1, ikpt:int=1, iband:int=1) -> int:
        self.__check_index(ispin, ikpt, iband)
        
        rec = 2 + (ispin - 1) * self.__nkpts * (self.__nbands + 1) + \
                  (ikpt - 1) * (self.__nbands + 1) + iband
        return rec
    
    def __check_index(self, ispin:int, ikpt:int, iband:int) -> None:
        assert 1 <= ispin <= self.__nspin,  'Invalid spin index'
        assert 1 <= ikpt  <= self.__nkpts,  'Invalid kpoint index'
        assert 1 <= iband <= self.__nbands, 'Invalid band index'
        
    def __gvectors(self, ikpt:int=1, check_consistency:bool=True):
        """
        Generate the G-vectors that satisfy (G + k)**2 / 2 < ENCUT
        """
        assert 1 <= ikpt <= self.__nkpts,  'Invalid kpoint index!'

        kvec = self.__kvecs[ikpt-1]

        fx, fy, fz = [np.arange(n, dtype=int) for n in self.__ngrid]
        fx[self.__ngrid[0] // 2 + 1:] -= self.__ngrid[0]
        fy[self.__ngrid[1] // 2 + 1:] -= self.__ngrid[1]
        fz[self.__ngrid[2] // 2 + 1:] -= self.__ngrid[2]
        
        if self.__lgamma:
            if self.__gamma_half == 'x':
                fx = fx[:self.__ngrid[0] // 2 + 1]
            else:
                fz = fz[:self.__ngrid[2] // 2 + 1]

        gz, gy, gx = np.array(np.meshgrid(fz, fy, fx, indexing='ij')).reshape((3, -1))
        kgrid = np.array([gx, gy, gz], dtype=float).T
        
        if self.__lgamma:
            if self.__gamma_half == 'z':
                kgrid = kgrid[
                    (gz > 0) |
                    ((gz == 0) & (gy > 0)) |
                    ((gz == 0) & (gy == 0) & (gx >= 0))
                ]
            else:
                kgrid = kgrid[
                    (gx > 0) |
                    ((gx == 0) & (gy > 0)) |
                    ((gx == 0) & (gy == 0) & (gz >= 0))
                ]

        # calculate kinetic energy of the plane waves
        kinen = HSQDTM * np.linalg.norm(np.dot(kgrid + kvec[np.newaxis, :], \
                                                 TPI*self.__bcell), axis=1)**2
        
        # find G-vectors whose kinetics energy is less than the cut-off
        Gvec = kgrid[np.where(kinen < self.__encut)[0]]

        # Check if the calculated number of planewaves and the one recorded in the
        # WAVECAR are equal
        if check_consistency:
            if Gvec.shape[0] != self.__nplws[ikpt - 1]:
                if Gvec.shape[0] * 2 == self.__nplws[ikpt - 1]:
                    if not self._lsoc:
                        raise ValueError('''
                        It seems that you are reading a WAVECAR from a NONCOLLINEAR VASP.
                        Please set 'lsorbit = True' when loading the WAVECAR.
                        For example:

                            wfc = vaspwfc('WAVECAR', lsorbit=True)
                        ''')
                elif Gvec.shape[0] == 2 * self.__nplws[ikpt - 1] - 1:
                    if not self.__lgamma:
                        raise ValueError('''
                        It seems that you are reading a WAVECAR from a GAMMA-ONLY VASP.  Please set
                        'lgamma = True' when loading the WAVECAR.  Moreover, you may want to set
                        "gamma_half" if you are using VASP version <= 5.2.x.  For VASP <= 5.2.x, check
                        which FFT VASP uses by the following command:

                            $ grep 'use.* FFT for wave' OUTCAR

                        Then

                            # for parallel FFT, VASP <= 5.2.x
                            wfc = vaspwfc('WAVECAR', lgamma=True, gamma_half='z')

                            # for serial FFT, VASP <= 5.2.x
                            wfc = vaspwfc('WAVECAR', lgamma=True, gamma_half='x')

                        For VASP >= 5.4, WAVECAR is written with x-direction half grid regardless of
                        parallel or serial FFT.

                            # "gamma_half" default to "x" for VASP >= 5.4
                            wfc = vaspwfc('WAVECAR', lgamma=True, gamma_half='x')
                        ''')
                else:
                    raise ValueError('''
                    NO. OF PLANEWAVES NOT CONSISTENT:

                        THIS CODE -> %d
                        FROM VASP -> %d
                           NGRIDS -> %d
                    ''' % (Gvec.shape[0],
                           self.__nplws[ikpt - 1] // 2 if self.__lsoc else self.__nplws[ikpt - 1],
                           np.prod(self.__ngrid))
                    )

        return np.asarray(Gvec, dtype=int)
    
    def __read_band_coefficients(self, ispin=1, ikpt=1, iband=1, norm=False) -> npt.NDArray[np.complex64|np.complex128]:
        """
        Read the plane wave coefficients of specified Kohn-Shan state

        Parameters
        ----------
        ispin : int, optional
            spin index, by default 1
        ikpt : int, optional
            k-point index, by default 1
        iband : int, optional
            band index, by default 1
        norm : bool, optional
            whether to normalize coefficients, by default False

        Returns
        -------
        npt.NDArray[np.complex64|np.complex128]
            Array of plane-wave coefficients
        """
        self.__check_index(ispin, ikpt, iband)

        rec = self.__find_record_location(ispin, ikpt, iband)
        
        with open(self.__filename, 'rb') as f:
            f.seek(rec * self.__recl)
            nplw = self.__nplws[ikpt - 1]
            dump = np.fromfile(f, dtype=self.__prectype, count=nplw)

        cg = np.asarray(dump, dtype=self.__prectype)

        if norm:
            cg /= np.linalg.norm(cg)
        return cg