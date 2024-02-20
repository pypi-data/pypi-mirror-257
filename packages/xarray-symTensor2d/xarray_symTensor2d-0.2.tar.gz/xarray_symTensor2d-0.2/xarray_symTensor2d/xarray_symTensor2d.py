import xarray as xr
import numpy as np


@xr.register_dataarray_accessor("sT")

class sT(object):
    '''
    This is a classe to work on 2d symetric Tensor of dim 3x3 in xarray environnement.
    
    Only 6 components are stored (exx,eyy,ezz,exy,exz,eyz)
    '''
    
    def __init__(self, xarray_obj):
        self._obj = xarray_obj 
    
    pass

#---------------------------------------Function-------------------------------------------
    def eqVonMises(self,lognorm=False, var='strain'):
        '''
        Compute the equivalent deforamtion of Von Mises (https://en.wikipedia.org/wiki/Infinitesimal_strain_theory)

        :param var: strain (vv=2/3) or stress (vv=3/2)
        :type typvare: str
        :return eqVM: (vv*e_ij.e_ij)**0.5
        :rtype eqVM: xr.DataArray
        '''

        if var=='strain':
            vv=2./3.
        elif var=='stress':
            vv=3./2.

        
        deq=(vv*(np.nansum(self._obj**2,axis=-1)+np.nansum(self._obj[...,3::]**2,axis=-1)))**.5
        
        
        if lognorm:
            med=np.nanmedian(deq,axis=(-1, -2))
            for i in range(len(self._obj.time)):
                if len(self._obj.dims)==4:
                    deq[i,...]=np.log(deq[i,...]/med[i])
                elif len(self._obj.dims)==5:
                    for j in range(len(self._obj.ncor)):
                        deq[j,i,...]=np.log(deq[j,i,...]/med[j,i])
            
            
        xr_deq=xr.DataArray(deq,dims=self._obj.coords.dims[0:-1])

        return xr_deq

    
    def mean(self,axis='tyy'):
        '''
        Compute the average of one componant
        
        :param axis: txx,tyy,tzz,txy,txz,tyz
        :type axis: str
        :return mean: average of this component
        :rtype mean: xr.DataArray
        '''
        
        label=['txx','tyy','tzz','txy','txz','tyz']
        
        if axis in label:
            res=np.nanmean(np.array(self._obj[...,label.index(axis)]),axis=(-1, -2))
                       
            return xr.DataArray(res,dims=self._obj.coords.dims[0])
            
        else:
            print('Error: axis not defined please select one of thos axis : txx,tyy,tzz,txy,txz,tyz')
            return
#----------------------------------------------------------      
    def to_square(self):
        '''
        return xr.DataArray as square matrix
        '''
        ss=list(self._obj.shape[0:-1])
        ss.append(3)
        ss.append(3)
        
        sq_m=np.zeros(ss)
            
        sq_m[...,0,0]=self._obj[...,0]
        sq_m[...,1,1]=self._obj[...,1]
        sq_m[...,2,2]=self._obj[...,2]

        sq_m[...,0,1]=self._obj[...,3]
        sq_m[...,1,0]=self._obj[...,3]

        sq_m[...,0,2]=self._obj[...,4]
        sq_m[...,2,0]=self._obj[...,4]

        sq_m[...,1,2]=self._obj[...,5]
        sq_m[...,2,1]=self._obj[...,5]
        
        dd=list(self._obj.coords.dims[0:-1])
        dd.append('mi')
        dd.append('mj')
        return xr.DataArray(sq_m,dims=dd)
    
#----------------------------------------------------------
    def eigh(self,absmax=False):
        '''
        Export eigen vector and eigen value
        
        :param absmax: return the absolut maximum eigenvalue and eigenvector ('a_am' a,d 'e_am')
        :type absmax: bool
        
        Return xr.Dataset where ai are the eigen value and ei are the associated eigen vector that can be used with uvecs accessor.
        '''
        
        dd=list(self._obj.coords.dims[0:-1])
                
        sq_m=self.to_square()
        eval,evec=np.linalg.eigh(sq_m)
        
        ds=xr.Dataset()
        ds['a1']=xr.DataArray(eval[...,2],dims=dd)
        ds['a2']=xr.DataArray(eval[...,1],dims=dd)
        ds['a3']=xr.DataArray(eval[...,0],dims=dd)
        
        col=np.arccos(evec[...,2,:])
        azi=np.arctan(evec[...,1,:]/evec[...,0,:])
                
        ss=list(self._obj.shape[0:-1])
        ss.append(2)
        
        e1=np.zeros(ss)
        e1[...,0]=azi[...,2]
        e1[...,1]=col[...,2]
        e2=np.zeros(ss)
        e2[...,0]=azi[...,1]
        e2[...,1]=col[...,1]
        e3=np.zeros(ss)
        e3[...,0]=azi[...,0]
        e3[...,1]=col[...,0]
        
        dd.append('uvecs')
        ds['e1']=xr.DataArray(e1,dims=dd)
        ds['e2']=xr.DataArray(e2,dims=dd)
        ds['e3']=xr.DataArray(e3,dims=dd)
        
        ds.coords['x']=self._obj.x
        ds.coords['y']=self._obj.y
        ds.coords['time']=self._obj.time
        
        if absmax:
            v=np.zeros(ds.e1.shape)
            a=np.zeros(ds.a1.shape)
            ss=ds.e1.shape

            for k in range(ss[0]):
                all_a=np.abs(np.dstack([np.array(ds.a1[k,...]),np.array(ds.a2[k,...]),np.array(ds.a3[k,...])]))
                for i in range(ss[1]):
                    for j in range(ss[2]):
                        if ~np.isnan(all_a[i,j,0]):
                            nn=np.where(all_a[i,j,:]==np.max(all_a[i,j,:]))
                            if nn[0][0]==0:
                                v[k,i,j,:]=np.array(ds.e1[k,i,j,:])
                                a[k,i,j]=np.array(ds.a1[k,i,j])
                            elif nn[0][0]==1:
                                v[k,i,j,:]=np.array(ds.e2[k,i,j,:])
                                a[k,i,j]=np.array(ds.a2[k,i,j])
                            elif nn[0][0]==2:
                                v[k,i,j,:]=np.array(ds.e3[k,i,j,:])
                                a[k,i,j]=np.array(ds.a3[k,i,j])
        
            ds['a_am']=xr.DataArray(a,dims=dd[0:-1])
            ds['e_am']=xr.DataArray(v,dims=dd)
            
        return ds
                
        

    