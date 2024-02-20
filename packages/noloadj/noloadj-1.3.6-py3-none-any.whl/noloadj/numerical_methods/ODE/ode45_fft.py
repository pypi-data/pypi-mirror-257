from noloadj.numerical_methods.ODE.ode45 import *
from noloadj.numerical_methods.ODE.ode45 import _odeint45

def odeint45_fft(f,x0,vect_t,*P,M,T=0.,h0=1e-5,tol=1.48e-8):
    '''
    Solves an ODE system described by f with Runge-Kutta 45 algorithm, and
    compute its fast Fourier Transform (FFT).
    :param f: a class that describes the ODE system
    :param x0: initial state vector
    :param vect_t: time vector on which the ODE system must be solved
    :param P: optimization inputs
    :param M: number of points to compute the FFT
    :param T: operating period of the system (facultative)
    :param h0: initial step size
    :param tol: tolerance for optimal step size computation
    :return: a matrix xf with state vector values across time, a matrix yf with
    output vector values across time, and their respective FFT module and phase
    '''
    return _odeint45_fft(f,h0,tol,M,x0,vect_t,T,*P)


@partial(custom_jvp,nondiff_argnums=(0,1,2,3))
def _odeint45_fft(f,h0,tol,M,x0,vect_t,T,*P):
    if hasattr(f,'update'):
        xf,yf,_=_odeint45(f,h0,tol,x0,vect_t,T,*P)
    else:
        xf,yf=_odeint45(f,h0,tol,x0,vect_t,T,*P)

    xfft=np.fft.fft(xf,M)*2/M # fft de x avec normalisation
    xfft=xfft.at[:,0].divide(2)
    yfft=np.fft.fft(yf,M)*2/M # fft de y avec normalisation
    yfft=yfft.at[:,0].divide(2)
    moduleX,phaseX=np.abs(xfft),np.angle(xfft) # amplitude et phase de la fft de x
    moduleY,phaseY=np.abs(yfft),np.angle(yfft) # amplitude et phase de la fft de y

    return xf,moduleX[:,0:M//2],phaseX[:,0:M//2],yf,moduleY[:,0:M//2],\
           phaseY[:,0:M//2]# on retire les frequences negatives


@_odeint45_fft.defjvp
def _odeint45_fft_jvp(f,h0,tol,M, primals, tangents):
    '''
    Solves an ODE system described by df/dP with Runge-Kutta 45 algorithm, and
    computes the derivatives of its FFT.
    :param f: a class that describes the ODE system
    :param h0: initial step size
    :param tol: tolerance for optimal step size computation
    :param M: number of points to compute the FFT
    :param primals: tuple including initial state vector, time vector, operating
        period and optimization inputs.
    :param tangents: tuple including differentials of initial state vector,
        operating period and optimization inputs.
    :return: a matrix xf with state vector values across time, a matrix yf with
    output vector values across time, and their respective FFT module and phase,
    and their derivatives w.r.t optimization inputs.
    '''
    x0, vect_t,T, *P = primals
    dx0, _,_, *dP = tangents
    nPdP = len(P)

    xf,dxf,modX,phX,dmodX,dphX,yf,dyf,modY,phY,dmodY,dphY=\
        odeint45_fft_etendu(f,nPdP, h0,tol,M, x0,dx0,vect_t,T, *P, *dP)
    return (xf,modX,phX,yf,modY,phY),(dxf,dmodX,dphX,dyf,dmodY,dphY)


def odeint45_fft_etendu(f,nPdP,h0,tol,M,x0,dx0,vect_t,T,*P_and_dP):
    P,dP = P_and_dP[:nPdP],P_and_dP[nPdP:]
    if hasattr(f,'update'):
        xf,dxf,yf,dyf,_=odeint45_etendu(f,nPdP,h0,tol,x0,dx0,vect_t,T, *P, *dP)
    else:
        xf,dxf,yf,dyf=odeint45_etendu(f,nPdP,h0,tol,x0,dx0,vect_t,T, *P, *dP)

    xfft=np.fft.fft(xf,M)*2/M  # fft de x avec normalisation
    dxfft=np.fft.fft(dxf,M)*2/M
    xfft,dxfft=xfft.at[:,0].divide(2),dxfft.at[:,0].divide(2)
    yfft=np.fft.fft(yf,M)*2/M  # fft de x avec normalisation
    dyfft=np.fft.fft(dyf,M)*2/M
    yfft,dyfft=yfft.at[:,0].divide(2),dyfft.at[:,0].divide(2)
    moduleX,phaseX=np.abs(xfft),np.angle(xfft)  # amplitude et phase de la fft de x
    dmoduleX,dphaseX=np.abs(dxfft),np.angle(xfft)
    moduleY,phaseY=np.abs(yfft),np.angle(yfft)  # amplitude et phase de la fft de x
    dmoduleY,dphaseY=np.abs(dyfft),np.angle(yfft)

    return xf,dxf,moduleX[:,0:M//2],phaseX[:,0:M//2],dmoduleX[:,0:M//2],\
           dphaseX[:,0:M//2],yf,dyf,moduleY[:,0:M//2],phaseY[:,0:M//2],\
           dmoduleY[:,0:M//2],dphaseY[:,0:M//2]



