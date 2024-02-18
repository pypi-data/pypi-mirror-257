import re
import numpy as np
import matplotlib.pyplot as plt

class CrystalOrbitalHamiltonPopulation:
    
    def __init__(self, filename:str):
        """
        Default constructor

        Parameters
        ----------
        filename : str
            path to COHPCAR.lobster file
        """
        self.__filename = filename
        self.__loadfile(filename)
    
    def __str__(self) -> str:
        """
        Produce string of object

        Returns
        -------
        str
            String of object
        """
        res = 'Filename: %s\n' % self.__filename
        res += 'Data items:\n'
        for d in self.__dataitems:
            res += '    %s: %s\n' % (d['type'], d['label'])
        res += 'Energy interval: (%6.4f, %6.4f)\n' % (self.__energies[0], self.__energies[-1])
        res += 'Number of data points: %i\n' % self.__npts
        return res
    
    def get_dataitems(self) -> list[dict]:
        """
        Get all data items

        Returns
        -------
        list[dict]
            List of data items
        """
        return self.__dataitems
    
    def get_dataitem(self, idx:int) -> dict:
        """
        Get a single data item

        Parameters
        ----------
        idx : int
            data item id

        Returns
        -------
        dict
            Single data item
        """
        return self.__dataitems[idx]
    
    def get_average_cohp(self) -> dict:
        """
        Get the averaged COHP data item

        Returns
        -------
        dict
            Averaged COHP data item
        """
        return self.__dataitems[0]
    
    def get_spin_state(self) -> str:
        """
        Return whether the calculation was spin-polarized or not

        Returns
        -------
        str
            String containing information on the spin-configuration
        """
        return self.__spin
    
    def get_energies(self) -> np.ndarray:
        """
        Get the energies

        Returns
        -------
        np.ndarray
            Array of energies
        """
        return self.__energies
    
    def get_npts(self) -> int:
        """
        Get the number of sampling points

        Returns
        -------
        int
            Number of sampling points
        """
        return self.__npts
    
    def plot_average(self):
        plt.figure(dpi=144, figsize=(2,8))
        plt.plot(self.__dataitems[0]['cohp'],
                 self.__energies)
        plt.plot(self.__dataitems[0]['icohp'],
                 self.__energies,
                 '--')
        plt.xlabel('# COHP [-]')
        plt.ylabel('Energy $E - E_{f}$ [eV]')
        plt.grid(linestyle='--', color='black', alpha=0.5)
        plt.show()
        plt.close()
    
    def get_average(self) -> np.ndarray:
        """
        Get the averaged COHP

        Returns:
            np.ndarray: averaged COHP values
        """
        return self.__dataitems[0]['cohp']
    
    def __loadfile(self, filename):
        # grab relevant header data before proceeding to all data
        with open(filename, 'r') as f:
            lines = []
            for i in range(0,2):
                lines.append(f.readline())
            spin = int(lines[1].split()[1])
            if spin == 1:
                self.__spin = 'restricted'    
            elif spin == 2:
                self.__spin = 'unrestricted'    
            else:
                raise 'Unknown spin configuration: %i' % spin
            
            self.__nritems = int(lines[1].split()[0])
            self.__npts = int(lines[1].split()[2])
            
            for i in range(0, self.__nritems):
                lines.append(f.readline())
            
        # loop over items
        pattern1 = re.compile(r'No.([0-9]+):([A-Za-z]{1,2})([0-9]+)\[([0-9][spdf]_?[a-z^2]*)\]->([A-Za-z]{1,2})([0-9]+)\[([0-9][spdf]_?[a-z-^2]*)\].*')
        pattern2 = re.compile(r'No.([0-9]+):([A-Za-z]{1,2})([0-9]+)->([A-Za-z]{1,2})([0-9]+).*')
        
        items = []
        items.append({
            'type' : 'average',
            'label': 'Average',
        })
        
        for i in range(0, self.__nritems-1):
            m = re.match(pattern1, lines[3+i])
            if m:
                items.append({
                    'type' : 'orbitalwise',
                    'interaction_id' : int(m.group(1)),
                    'element1' : m.group(2),
                    'atomid1' : int(m.group(3)),
                    'orbital1' : m.group(4),
                    'element2' : m.group(5),
                    'atomid2' : int(m.group(6)),
                    'orbital2' : m.group(7),
                    'label': '%s%i[%s]->%s%i[%s]' % (m.group(2), 
                                                     int(m.group(3)),
                                                     m.group(4),
                                                     m.group(5), 
                                                     int(m.group(6)),
                                                     m.group(7))
                })
            else:
                m = re.match(pattern2, lines[3+i])
                if m:
                    items.append({
                        'type' : 'total',
                        'interaction_id' : int(m.group(1)),
                        'element1' : m.group(2),
                        'atomid1' : int(m.group(3)),
                        'element2' : m.group(4),
                        'atomid2' : int(m.group(5)),
                        'label': '%s%i->%s%i' % (m.group(2), 
                                                 int(m.group(3)),
                                                 m.group(4), 
                                                 int(m.group(5)))
                    })
                else:
                    raise Exception('Cannot parse line: %s' % lines[3+i])
        self.__dataitems = items
        
        # grab all data
        rawdata = np.loadtxt(filename, dtype=np.float32, skiprows=2+self.__nritems, max_rows=self.__npts)
        
        # assign data to items
        self.__energies = rawdata[:,0]
        for i in range(0, self.__nritems):
            if self.__spin == 'unrestricted':
                self.__dataitems[i]['cohp_up'] = rawdata[:,i*2+1]
                self.__dataitems[i]['icohp_up'] = rawdata[:,i*2+2]
                self.__dataitems[i]['cohp_down'] = rawdata[:,(i+self.__nritems)*2+1]
                self.__dataitems[i]['icohp_down'] = rawdata[:,(i+self.__nritems)*2+2]
                self.__dataitems[i]['cohp'] = self.__dataitems[i]['cohp_up'] + self.__dataitems[i]['cohp_down']
                self.__dataitems[i]['icohp'] = self.__dataitems[i]['icohp_up'] + self.__dataitems[i]['icohp_down']
            else:
                self.__dataitems[i]['cohp'] = rawdata[:,i*2+1]
                self.__dataitems[i]['icohp'] = rawdata[:,i*2+2]
                
            
        
            