import numpy as np
import matplotlib.pyplot as plt

class DensityOfStates:
    def __init__(self, filename:str):
        """
        Default constructor

        Parameters
        ----------
        filename : str
            path to DOSCAR.lobster file
        """
        self.__filename = filename
        self.__atomdos = []        
        self.__loadfile(filename)
    
    def get_nr_atoms(self) -> int:
        """
        Get the number of atoms

        Returns
        -------
        int
            number of atoms
        """
        return self.__nratoms
    
    def get_npts(self) -> int:
        """
        Get the number of data points

        Returns
        -------
        int
            Number of data points
        """
        return self.__npts
    
    def get_spin_state(self) -> str:
        return self.__spin
    
    def get_energies(self) -> np.ndarray[np.float32]:
        """
        Get the energies

        Returns
        -------
        np.ndarray[np.float32]
            Array of energies
        """
        return self.__energies
    
    def get_energy_interval(self) -> float:
        """
        Get the energy interval

        Returns
        -------
        float
            Energy interval
        """
        return (self.__energies[-1] - self.__energies[0]) / float(self.__npts-1)
    
    def get_total_dos(self) -> dict:
        """
        Get the total DOS

        Returns
        -------
        dict
            Dictionary with density of states
            
        Notes
        -----
        Depending on whether a spin-restricted or spin-unrestricted calculation
        is performed, the dictionary contains 3 or 5 keys. For a spin-restricted
        calculation, the keys are :code:`energies`, :code:`states`, and
        :code:`istates`. For a spin-unrestricted calculation, the keys are
        :code:`energies`, :code:`states_up`, :code:`states_down`, :code:`istates_up`,
        :code:`istates_down`.
        """
        if self.__totaldos.shape[1] == 3:
            return {
                'energies': self.__totaldos[:,0],
                'states': self.__totaldos[:,1],
                'istates': self.__totaldos[:,2]
            }
        else:
            return {
                'energies': self.__totaldos[:,0],
                'states_up': self.__totaldos[:,1],
                'states_down': self.__totaldos[:,2],
                'istates_up': self.__totaldos[:,3],
                'istates_down': self.__totaldos[:,4],
                'states': self.__totaldos[:,1] + self.__totaldos[:,2],
                'istates': self.__totaldos[:,3] + self.__totaldos[:,4]
            }
        
    def get_dos_atom(self, atomid:int) -> dict:
        """
        Get the density of states for a particular atom

        Parameters
        ----------
        atomid : int
            atom index

        Returns
        -------
        dict
            Density of states for a particular atom
            
        Notes
        -----
        The dictionary contains multiple keys, depending on the type of
        calculation that was performed to generate the DOS. The keys are
        constructed such that they indicate which part of the DOS is
        provided, e.g. whether they pertain to a specific `lm`-projection.
        """
        if atomid > self.__nratoms:
            raise Exception('Index exceeds maximum: %i > %i' % (atomid, self.__nratoms))
        
        if atomid < 1:
            raise Exception('Index needs to be larger than 0')
        
        return self.__atomdos[atomid-1]
    
    def quickplot_total(self) -> None:
        """
        Generate a quick plot of the total density of states
        
        This function is designed to be used inside a IDE such as Spyder.
        """
        plt.figure(dpi=144, figsize=(2,8))
        plt.plot(self.__totaldos[:,1] if self.__spin == 'restricted' else
                 np.sum(self.__totaldos[:,1:2], axis=1),
                 self.__totaldos[:,0])
        plt.xlabel('# states [-]')
        plt.ylabel('Energy $E - E_{f}$ [eV]')
        plt.grid(linestyle='--', color='black', alpha=0.5)
        plt.show()
        plt.close()
    
    def __loadfile(self, filename):
        # grab relevant header data before proceeding to all data
        with open(filename, 'r') as f:
            self.__lines = f.readlines()                
            self.__nratoms = int(self.__lines[0].split()[0])
            self.__npts = int(self.__lines[5].split()[2])
            f.close()
            
        # grab overall density of states
        self.__totaldos = np.loadtxt(filename, dtype=np.float32, skiprows=6, max_rows=self.__npts)
        self.__energies = self.__totaldos[:,0]
        if self.__totaldos.shape[1] == 3:
            self.__spin = 'restricted'
        else:
            self.__spin = 'unrestricted'
        
        # grab the DOS per atom
        for i in range(0,self.__nratoms):
            # create container for the atomic dos
            data = {
                    'states' : [],
                    'atomid': i+1,
                    'atomnumber': -1,
            }
            
            # start line index
            lineidx = (i+1) * (self.__npts+1) + 5
            header = self.__lines[lineidx].split(';')
            data['atomnumber'] = int(header[1].split('=')[1])
            data['labels'] = header[-1].strip().split()
            values = np.loadtxt(filename, dtype=np.float32, skiprows=lineidx+1, max_rows=self.__npts)
            for j,label in enumerate(data['labels']):
                if self.__spin == 'restricted':
                    data['states'].append({
                        'label': label,
                        'states': values[:,j+1]
                    })
                else:
                    data['states'].append({
                        'label': label,
                        'states_up': values[:,(j*2)+1],
                        'states_down': values[:,(j*2)+2],
                        'states': np.sum(values[:,(j*2)+1:(j*2)+3], axis=1),
                    })
                    
            # store atomic dos into array
            self.__atomdos.append(data)
            