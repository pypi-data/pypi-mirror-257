from utils import*
import importlib as imp
import wallpp.plane_group as pg   ;imp.reload(pg)
import nearBragg.nearBragg as nb ;imp.reload(nb)
plt.close('all')
path='../../multislice/docs_fig/multi2D/'
opts='I'

# Problem
keV   = 200        # wavelength 200keV
Nx    = 10          # Transverse unit cells
Nz    = 20         #
# ndeg  = 2**8       # number of pixels
pptype,ax,bz,angle,Za = 'p1',10,5,90,  2
pattern = np.array([[5,2.5,Za]])
eps = 1
opt='p'
method = 'D'


q0s = np.linspace(0,1,401)
nbG = nb.NearBragg(pattern.T,ax,bz,keV=keV,Nx=Nx,Nz=Nz,eps=eps,
    method=method,q0s=q0s,iZv=20)
nb0 = nb.NearBragg(pattern.T,ax,bz,keV=keV,Nx=Nx,Nz=Nz,eps=eps,
    method='G',q0s=q0s,iZv=100)
nbG.F_show(qopt=0,lw=2)
fig,ax = dsp.stddisp([nbG.q0s,nbG.I,'bo-'],opt='')
dsp.stddisp([nb0.q0s,nb0.I,'ro--'],ax=ax)

if method=='P':
    z = bz*np.arange(Nz+1)/10
    sig_e = nbG.sig_e
    le = ax*bz/sig_e/10
    Pcoh = np.exp(-z/le)
    Pkin = (z/le)*np.exp(-z/le)
    Pdyn = 1-Pcoh-Pkin


    cs = dsp.getCs('Spectral',3)
    plts  = [[z,I,cs[i],'%d' %i] for i,I in enumerate(nbG.I)]
    plts += [[z,Pcoh,[cs[0],'--'],''],[z,Pkin,[cs[1],'--'],''],[z,Pdyn,[cs[2],'--'],'']]
    plts += [[z,nbG.I.sum(axis=0),'k:']]
    dsp.stddisp(plts,labs=['$z(nm)$','$Proba$'],lw=2,
        opt=opt,name=path+'NBproba.svg')


# iZ = slice(1,-1,100)
# nz = z[iZ].shape[0]
# cs = dsp.getCs('jet',nz)
# plts  = [[q0s,S,cs[i],'z=%dnm' %z[iZ][i]] for i,S in enumerate(nbG.S[iZ,:,2])]
# dsp.stddisp(plts,labs=['$q(\AA^{-1})$','Double scattering area$(\AA)$'],lw=2,
#     opt=opt,name=path+'NBdouble.svg')
#
# cs = dsp.getCs('jet',nz)
# plts  = [[q0s,S,cs[i],'z=%dnm' %z[iZ][i]] for i,S in enumerate(nbG.S[iZ,:,1])]
# dsp.stddisp(plts,labs=['$q(\AA^{-1})$','Single scattering area$(\AA)$'],lw=2,
#     opt=opt,name=path+'NBsingle.svg')
