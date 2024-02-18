import scipy.signal
import scipy.optimize
import numpy as np

def find_peaks(energies, dos):
    res = scipy.signal.find_peaks(dos, height=np.average(dos))
    x = np.array(res[1]['peak_heights'], dtype=energies.dtype)
    y = energies[res[0]]
    
    return x,y

def fit_gaussians(energies, dos, mus):
    p0 = np.zeros((len(mus), 3))
    for i,mu in enumerate(mus):
        p0[i,:] = [np.average(dos),mu,0.1]
    
    res = scipy.optimize.curve_fit(multigauss, energies, dos, p0.flatten())

    coeff = res[0].reshape([-1,3])
    gaussians = []
    for i in range(len(mus)):
        gaussians.append({
            'N' : coeff[i,0],
            'mu' : coeff[i,1],
            'sigma' : coeff[i,2]
        })
        
    return {'gaussians': gaussians, 'curve': multigauss(energies, res[0])}

def multigauss(x, *args):
    coeff = np.array(args).reshape([-1,3])
    res = np.zeros_like(x)
    for i in range(len(coeff)):
        res += __gaussian(x, *coeff[i,:])
        
    return res
        
def __gaussian(x, n, mu, sigma):
    return n / (sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * (x-mu)**2/(2*sigma**2))