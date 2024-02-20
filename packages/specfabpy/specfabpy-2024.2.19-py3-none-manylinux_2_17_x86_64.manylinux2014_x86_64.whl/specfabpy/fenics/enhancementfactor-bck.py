#!/usr/bin/python3
# Nicholas M. Rathmann <rathmann@nbi.ku.dk>, 2021-2023

"""
FEniCS interface for calculating bulk enhancement factors given CPO field
"""

import numpy as np
from dolfin import *
from ..specfabpy import specfabpy as sf__ # sf private copy 
from .common import *

import copy, sys, time, code # code.interact(local=locals())

class EnhancementFactor():

    def __init__(self, mesh, L, modelplane='xz'):

        ### Setup

        self.mesh = mesh
        self.L = L        
        self.modelplane = modelplane
        self.USE_REDUCED = True # use reduced representation of fabric state vector 
        
        self.sf = sf__
        self.lm, self.nlm_len_full = self.sf.init(self.L)
        self.nlm_len = self.sf.get_rnlm_len() if self.USE_REDUCED else self.nlm_len_full # use reduced or full form?
        
        ### Function spaces
        
        # Store CPO information element-wise: node located at element center, CPO constant over element
        eletype, eleorder = 'DG', 0 
        self.Rele = FiniteElement(eletype, self.mesh.ufl_cell(), eleorder)
        self.R  = FunctionSpace(self.mesh, self.Rele) # for scalars 
        self.R3 = VectorFunctionSpace(self.mesh, eletype, eleorder, dim=3) # for vectors
        self.numdofs = Function(self.R).vector().local_size()   

        self.R2 = VectorFunctionSpace(self.mesh, eletype, eleorder, dim=2) # for 2d vectors
        self.R2_assigner = FunctionAssigner(self.R2, [self.R, self.R]) 
        self.R3_assigner = FunctionAssigner(self.R3, [self.R, self.R, self.R]) # for constructing vectors from their components
        

    def V2R(self, wV):
        wV_sub = wV.split()
        wR_sub = [project(wV_sub[ii], self.R) for ii in range(self.nlm_len)] 
        return wR_sub
        
        
    def wR(self, w):
        if   self.modelplane=='xy': return self.V2R(w.sub(0)), self.V2R(w.sub(1)) # wr_R, wi_R
        elif self.modelplane=='xz': return self.V2R(w), [project(Constant(0), self.R)]*self.nlm_len # wr_R, 0
        
       
    def nlm_nodal(self, w):
        wr_R, wi_R = self.wR(w)
        rnlm = np.array([ wr_R[ii].vector()[:] + 1j*wi_R[ii].vector()[:] for ii in range(self.nlm_len) ])
        nlm = np.array([ self.sf.rnlm_to_nlm(rnlm[:,nn], self.nlm_len_full) for nn in range(self.numdofs) ])
        return nlm # nlm[node,coef]

 
    def get_nlm(self, w, x,y):
        wr_R, wi_R = self.wR(w)
        rnlm = np.array([ wr_R[ii].vector()[:] + 1j*wi_R[ii].vector()[:] for ii in range(self.nlm_len) ])
        return self.sf.rnlm_to_nlm(rnlm, self.nlm_len_full)
        
        
    def set_ei_(self, ei):
        ei_  = np.zeros((self.numdofs, 3, 3)) # (node, i-th vector, xyz component)
        for ii in range(3): 
            ei_[:,ii,:] = np.tile(ei[ii], (self.numdofs,1))
            
#        code.interact(local=locals())
        return ei_            
        
        
    def np2func(self, ei_, Eij_):

        # CPO eigenvectors 
#        ei  = [Function(self.R3) for _ in range(3)] # ei = (e1,e2,e3)
#        eij = Function(self.R)
#        for ii in range(3): 
#            eix,eiy,eiz = ei[ii].split()

#            eij.vector()[:] = ei_[:,ii,0] 
#            ass = FunctionAssigner(eix.function_space(), self.R)
#            ass.assign(eix, eij)

#            eij.vector()[:] = ei_[:,ii,1] 
#            ass = FunctionAssigner(eiy.function_space(), self.R)
#            ass.assign(eiy, eij)
#            
#            eij.vector()[:] = ei_[:,ii,2] 
#            ass = FunctionAssigner(eiz.function_space(), self.R)
#            ass.assign(eiz, eij)


#        ei  = [Function(self.R3) for _ in range(3)] # ei = (e1,e2,e3)
#        for ii in range(3): 
#            eix = [Function(self.R) for _ in range(3)]
#            eix[0].vector()[:] = ei_[:,ii,0] # x component of ei
#            eix[1].vector()[:] = ei_[:,ii,1] # y
#            eix[2].vector()[:] = ei_[:,ii,2] # z
#            self.R3_assigner.assign(ei[ii], eix) # assign component fields to ei vector field

        ei  = [Function(self.R3) for _ in range(3)] # ei = (e1,e2,e3)
        eij = Function(self.R)
        for ii in range(3): # vector i
#            eix = [Function(self.R) for _ in range(3)]
#            eix[0].vector()[:] = ei_[:,ii,0] # x component of ei
#            eix[1].vector()[:] = ei_[:,ii,1] # y
#            eix[2].vector()[:] = ei_[:,ii,2] # z
#            assign(ei[ii], as_vector((eix[0], eix[1], eix[2])) )
            for jj in range(3): # component j
                eij.vector()[:] = ei_[:,ii,jj]
#                assign(ei[ii].sub(jj).collapse(), eij)
                ass = FunctionAssigner(ei[ii].sub(jj).collapse(), self.R)

        # Tuple of eigenenhancements w.r.t. ei
        Eij = [Function(self.R)  for _ in range(6)] # Eij = (E11,E22,E33,E23,E13,E12)
        for kk in range(6): 
            Eij[kk].vector()[:] = Eij_[:,kk]
        
        return ei, Eij
        
        
    def Eij_tranisotropic(self, w, Eij_grain,alpha,n_grain, ei=()):
    
        """
        Bulk enhancement factors w.r.t. ei=(e1,e2,e3) axes for *transversely isotropic* grains.
        If ei=(), then CPO (a^(2)) eigenvectors are assumed ei=(m1,m2,m3) => Eij are the eigenenhancements.
        """
    
        if n_grain != 1: raise ValueError('only n_grain = 1 (linear viscous) is supported')
        if not(0 <= alpha <= 1): raise ValueError('alpha should be between 0 and 1')
   
#        nlm_ = np.zeros((self.numdofs, self.nlm_len_full), dtype=np.complex64) # (node, nlm component)
        Eij_ = np.zeros((self.numdofs, 6))    # (node, Eij component)
        ei_  = np.zeros((self.numdofs, 3, 3)) # (node, i-th vector, xyz component)
        
#        nlm_[:,:] = self.nlm_nodal(w) # determine nlm, mi, Eij per node
        if len(ei) == 3: ei_[:,:,:] = self.set_ei_(ei) # set prescribed ei frame
                
#        # Determine ei and Eij per node
#                        
#        for nn in np.arange(self.numdofs): 

#            if len(ei) == 0:
##                m1,m2,m3 = eigenframe(nlm_[nn,:], self.modelplane, self.sf)[0].T # principal directions of a^(2)
#                m1,m2,m3 = np.eye(3)
#                ei_[nn,0,:] = m1 
#                ei_[nn,1,:] = m2 
#                ei_[nn,2,:] = m3 
#                if nn==51: code.interact(local=locals())

#            Eij_[nn,:] = self.sf.Eij_tranisotropic(nlm_[nn,:], ei_[nn,0,:], ei_[nn,1,:], ei_[nn,2,:], Eij_grain, alpha, n_grain)
#            
#        """
#        The enhancement-factor model depends on effective (homogenized) grain parameters, calibrated against deformation tests.
#        For CPOs far from the calibration states, negative values may occur where Eij should tend to zero if truncation L is not large enough.
#        """
#        Eij_[Eij_ < 0] = 1e-2 # Set negative E_ij to a very small value (flow inhibiting)
        
        ei, Eij = self.np2func(ei_, Eij_) 
        
        return ei, Eij
    
    
    def Eij_orthotropic(nlm,blm, Eij_grain,alpha,n_grain, ei=()):
        pass

