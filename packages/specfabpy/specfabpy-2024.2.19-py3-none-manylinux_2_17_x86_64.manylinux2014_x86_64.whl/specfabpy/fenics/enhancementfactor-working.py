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

        self.R_prj = self.R
        self.R3_prj = self.R3
        self.numdofs_prj = self.numdofs

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
    
        fabric = self
        fabric.w = w
    
        Nnodes = fabric.numdofs_prj
        x1, x2, x3 = np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])

        ### numpy arrays used to stored specfab values, to be subsequently inserted into the fenics functions
        ai_           = np.zeros((3,Nnodes))
        m1_, m2_, m3_ = np.zeros((3,Nnodes)), np.zeros((3,Nnodes)), np.zeros((3,Nnodes))
        Eij_  = np.zeros((6,Nnodes))
        
        ### Project nlm onto R_prj subspace, needed for Stokes solver
#        vr_Vsub, vi_Vsub = fabric.w.sub(0).split(), fabric.w.sub(1).split() # in V function *subspace* -- don't deepcopy for dolfin-adjoint overloads to work
#        vr_Rsub = [project(vr_Vsub[ii], fabric.R_prj) for ii in range(self.nlm_len)] # in sought after R_prj function space
#        vi_Rsub = [project(vi_Vsub[ii], fabric.R_prj) for ii in range(self.nlm_len)]

        vr_Rsub, vi_Rsub = self.wR(w)

        ### Fill numpy structures
        for nn in np.arange(Nnodes): 
        
            # Extract nlm for the nn'th node
            nlm = np.array([ vr_Rsub[ii].vector()[nn] + 1j*vi_Rsub[ii].vector()[nn] for ii in np.arange(self.nlm_len) ])
            if self.USE_REDUCED: nlm = self.sf.rnlm_to_nlm(nlm, self.nlm_len_full) # reduced form
            
            # Calculate fabric eigen basis and eigen values using specfab
#            m1_[:,nn], m2_[:,nn], m3_[:,nn], ai_[:,nn] = self.sf.frame(nlm, 'e') # fabric eigen basis 
            m1_[:,nn], m2_[:,nn], m3_[:,nn] = eigenframe(nlm, self.modelplane, self.sf)[0].T # principal directions of a^(2)

#            m1,m2,m3 = eigenframe(nlm_[nn,:], self.modelplane, self.sf)[0].T # principal directions of a^(2)

            # Calculate directional enhancement factors using specfab
            Eij_[:,nn]   = self.sf.Eij_tranisotropic(nlm, m1_[:,nn], m2_[:,nn], m3_[:,nn], Eij_grain,alpha,n_grain) # 3x3 tensor, eigenenhancements
        
        ### Ensure enhancements are strictly positive
        # The enhancement factor model is based on the calibration of three grain parameters (in the homogenization scheme) against deformation tests made on transversely isotropic fabrics from ice cores.
        # For other fabrics, when strong enough, the calibration might slightly fail, leading to Eij values, otherwise suppose to be near zero, to be become slightly negative.
         # We therefore overwrite such values with near zero ones for the correct behaviour.
        Eij_[Eij_ < 0]     = 1e-3
        
        ### Functions to be set
        # Scalars
        E11,E22,E33 = Function(fabric.R_prj),Function(fabric.R_prj),Function(fabric.R_prj) # eigenenhancements: directional enhancement factors in *fabric eigen basis* (m1,m2,m3)
        E23,E31,E12 = Function(fabric.R_prj),Function(fabric.R_prj),Function(fabric.R_prj) # ...
        #
        E11.vector()[:], E22.vector()[:], E33.vector()[:] = Eij_[0,:], Eij_[1,:], Eij_[2,:]
        E23.vector()[:], E31.vector()[:], E12.vector()[:] = Eij_[4,:], Eij_[3,:], Eij_[5,:]
        # Vectors
        m1,m2,m3    = Function(fabric.R3_prj),Function(fabric.R3_prj),Function(fabric.R3_prj)
        m1x,m1y,m1z = Function(fabric.R_prj),Function(fabric.R_prj),Function(fabric.R_prj)
        m2x,m2y,m2z = Function(fabric.R_prj),Function(fabric.R_prj),Function(fabric.R_prj)
        m3x,m3y,m3z = Function(fabric.R_prj),Function(fabric.R_prj),Function(fabric.R_prj)
        #        
        m1x.vector()[:], m1y.vector()[:], m1z.vector()[:] = m1_[0,:], m1_[1,:], m1_[2,:]
        m2x.vector()[:], m2y.vector()[:], m2z.vector()[:] = m2_[0,:], m2_[1,:], m2_[2,:]
        m3x.vector()[:], m3y.vector()[:], m3z.vector()[:] = m3_[0,:], m3_[1,:], m3_[2,:]
        assigner = FunctionAssigner(fabric.R3_prj, [fabric.R_prj, fabric.R_prj, fabric.R_prj])
        assigner.assign(m1, [m1x, m1y, m1z])
        assigner.assign(m2, [m2x, m2y, m2z])
        assigner.assign(m3, [m3x, m3y, m3z])
        
        ### Set results
        # Required by rheology
        self.m1, self.m2, self.m3 = m1, m2, m3 # <c^2> eigen vectors (presumed fabric symmetry directions for rheology)
        self.E11,self.E22,self.E33,self.E23,self.E31,self.E12 = E11,E22,E33,E23,E31,E12 # directional enhancement factors along mi
    
        return (self.m1, self.m2, self.m3), (self.E11,self.E22,self.E33,self.E23,self.E31,self.E12)
        
    
    def Eij_orthotropic(nlm,blm, Eij_grain,alpha,n_grain, ei=()):
        pass

