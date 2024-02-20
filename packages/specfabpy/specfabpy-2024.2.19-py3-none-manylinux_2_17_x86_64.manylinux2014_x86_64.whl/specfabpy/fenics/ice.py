#!/usr/bin/python3
# Nicholas M. Rathmann <rathmann@nbi.ku.dk>, 2022-2024

import copy, sys, time, code # code.interact(local=locals())
 
import numpy as np
from dolfin import *

from .. import constants as sfconst
from .CPO import *
from .enhancementfactor import *

class IceFabric(CPO):

    def __init__(self, mesh, boundaries, ds, n, L=8, nu_realspace=1e-3, nu_multiplier=1, modelplane='xz', \
                        Eij_grain=(1,1), alpha=0, n_grain=1, \
                        Cij=sfconst.ice['elastic']['Bennett1968'], rho=sfconst.ice['density']): 

        super().__init__(mesh, boundaries, ds, n, L, nu_multiplier=nu_multiplier, nu_realspace=nu_realspace, modelplane=modelplane) # initializes with isotropic fabric
        self.initialize(wr=None) # isotropic
        self.set_BCs([], [], []) # no BCs

        self.grain_params = (Eij_grain, alpha, n_grain)
        self.Lame_grain = self.sf.Cij_to_Lame_tranisotropic(Cij) 
        self.rho = rho

        self.enhancementfactor = EnhancementFactor(mesh, L, modelplane=modelplane)
        self.update_Eij()
                
        
    def get_state(self, *args, **kwargs): 
        return self.get_nlm(*args, **kwargs) # alias
        
        
    def evolve(self, *args, **kwargs):
        super().evolve(*args, **kwargs)
        self.update_Eij()

    def solvesteady(self, u, **kwargs):
        super().evolve(u, 1, steadystate=True, **kwargs)

    def update_Eij(self):
        self.mi, self.Eij, self.ai = self.enhancementfactor.Eij_tranisotropic(self.w, *self.grain_params, ei_arg=())
        self.xi, self.Exij, _      = self.enhancementfactor.Eij_tranisotropic(self.w, *self.grain_params, ei_arg=np.eye(3))
        # ... unpack
        self.m1, self.m2, self.m3 = self.mi # <c^2> eigenvectors (presumed fabric and rheological symmetry directions)
        self.E11, self.E22, self.E33, self.E23, self.E31, self.E12 = self.Eij  # eigenenhancements
        self.Exx, self.Eyy, self.Ezz, self.Eyz, self.Exz, self.Exy = self.Exij # Cartesian enhancements
        self.a1, self.a2, self.a3 = self.ai # <c^2> eigenvalues (fabric eigenvalues)
        
            
    def get_elastic_velocities(self, x,y, theta,phi, alpha=1):
        nlm = self.get_state(x,y)
        vS1, vS2, vP = sf__.Vi_elastic_tranisotropic(nlm, alpha,self.Lame_grain,self.rho, theta,phi) # calculate elastic phase velocities using specfab
        return (vP, vS1, vS2)

