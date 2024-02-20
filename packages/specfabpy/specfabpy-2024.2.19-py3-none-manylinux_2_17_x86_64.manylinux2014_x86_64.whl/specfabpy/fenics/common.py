#!/usr/bin/python3
# Nicholas M. Rathmann <rathmann@nbi.ku.dk>, 2021-2023

"""
Library of common routines
"""

import numpy as np
from dolfin import *

def eigenframe(nlm, modelplane, sf):

    """
    Get principal CPO frame 
    """

    a2 = sf.a2(nlm)
    eigvals, eigvecs = np.linalg.eig(a2)
    
    if modelplane is None: 
        I = np.flip(eigvals.argsort())
        
    else:
        if   modelplane=='xy': I = eigvecs[2,:].argsort() # last entry is eigenvector with largest z-value (component out of model plane)
        elif modelplane=='xz': I = eigvecs[1,:].argsort() # ... same but for y-value
        
        if eigvals[I[0]] < eigvals[I[1]]: 
            I[[0,1]] = I[[1,0]] # swap sorted indices so largest eigenvalue entry is first
    
    return eigvecs[:,I], eigvals[I], a2
    
    
def mat3d(D2, modelplane, reshape=False): 

    """
    R^3 strain-rate tensor from model-plane strain-rate tensor
    """

    if reshape: D2 = np.reshape(D2,(2,2)) # reshape if vectorized
    trace = D2[0,0] + D2[1,1]
    
    if modelplane=='xy':
        D3 = np.array([ [D2[0,0], D2[0,1], 0],\
                        [D2[1,0], D2[1,1], 0],\
                        [0,             0,  -trace] ] )  
    
    elif modelplane=='xz':  
        D3 = np.array([ [D2[0,0],      0,    D2[0,1]],\
                        [0,       -trace,    0      ],\
                        [D2[1,0],      0,    D2[1,1]] ] )  
                        
    else:
        raise ValueError('invalid modelplane "%s"'%(modelplane))
        
    return D3
