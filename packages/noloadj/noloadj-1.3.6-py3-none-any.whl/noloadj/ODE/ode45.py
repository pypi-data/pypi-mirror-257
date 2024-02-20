import jax.numpy as np
from jax.lax import *
from jax import custom_jvp,jvp
from functools import partial


def odeint45(f,x0,vect_t,*P,T=0.,h0=1e-5,tol=1.48e-8):
    '''
    Solves an ODE system described by f with Runge-Kutta 45 algorithm.
    :param f: a class that describes the ODE system
    :param x0: initial state vector
    :param vect_t: time vector on which the ODE system must be solved
    :param P: optimization inputs
    :param T: operating period of the system (facultative)
    :param h0: initial step size
    :param tol: tolerance for optimal step size computation
    :return: a matrix xf with state vector values across time, a matrix yf
        with output vector values across time, and a matrix states with
        configurations across time for periodic systems.
    '''
    return _odeint45(f,h0,tol,x0,vect_t,T,*P)


def rk_step(x_prev, t_prev, h_prev,f,*P):
    '''
    An iteration of the Runge-Kutta 45 algorithm
    :param x_prev: the state vector at the previous iteration
    :param t_prev: the time at the previous iteration
    :param h_prev: step size at the previous iteration
    :param f: a class that describes the ODE system
    :param P: optimization inputs
    :return: the state vector at the present iteration x_now, its estimation
        x_now_est the time t_now at the present iteration.
    '''
    k1=f.derivative(x_prev, t_prev,*P)
    k2 = f.derivative(x_prev + h_prev*0.2 * k1, t_prev + 0.2 * h_prev,*P)
    k3 = f.derivative(x_prev + h_prev*(3 * k1 + 9 *k2)/40,t_prev+3*h_prev/10,*P)
    k4 = f.derivative(x_prev + h_prev*(44 *k1/45-56 * k2 / 15+32*k3/9),t_prev +
           4 * h_prev / 5,*P)
    k5 = f.derivative(x_prev + h_prev*(19372 * k1 / 6561 - 25360 * k2 / 2187 +
            64448 * k3 / 6561- 212 * k4 / 729),
           t_prev + 8 * h_prev / 9,*P)
    k6 = f.derivative(x_prev + h_prev*(9017 * k1 /3168-355*k2 /33+46732*k3/5247+
            49 * k4 / 176 - 5103 * k5 / 18656),t_prev + h_prev,*P)
    k7 = f.derivative(x_prev + h_prev*(35 * k1 / 384 + 500 * k3 / 1113 +
            125 * k4 / 192 -2187 * k5 / 6784 + 11 * k6 / 84),t_prev + h_prev,*P)

    x_now = x_prev + h_prev *(35 * k1 / 384 + 500 * k3 / 1113 + 125 * k4 / 192
             -2187 * k5 / 6784 + 11 * k6 / 84)
    x_now_est = x_prev + h_prev *(5179 * k1 / 57600 + 7571* k3/16695+393*k4/640
            - 92097 * k5 / 339200 + 187 * k6 / 2100 + k7 / 40)
    t_now = t_prev + h_prev
    return x_now, x_now_est, t_now


def optimal_step(x_now,x_now_est,h_prev,tol,x_prev):
    '''
    Computes the optimal step size for the next iteration.
    :param x_now: state vector at the present iteration
    :param x_now_est: estimation of the state vector x_now
    :param h_prev: step size from the present iteration
    :param tol: tolerance for optimal step size computation
    :param x_prev: state vector at the previous iteration
    :return: optimal step size for the next iteration
    '''
    e=np.sqrt(np.sum(((x_now-x_now_est)/
                      (tol+tol*np.maximum(np.abs(x_now),np.abs(x_prev))))**2))
    hopt=h_prev*(e)**(-1/5)
    h_now=np.minimum(1.5*h_prev,0.9*hopt)
    return h_now

def interpolation(x_prev,y_prev,t_prev,x_now,y_now,t_now,t_new):
    '''
    Computes state and output vectors at time t_new by linear interpolation.
    :param x_prev: state vector at the previous iteration
    :param y_prev: output vector at the previous iteration
    :param t_prev: time at the previous iteration
    :param x_now: state vector at the present iteration
    :param y_now: output vector at the present iteration
    :param t_now: time at the present iteration
    :param t_new: new time for present iteration
    :return: state and output vectors x_new and y_new at t_new.
    '''
    x_new=((x_prev-x_now)*t_new+(t_prev*x_now-t_now*x_prev))/(t_prev-t_now)
    y_new=((y_prev-y_now)*t_new+(t_prev*y_now-t_now*y_prev))/(t_prev-t_now)
    return x_new,y_new

def compute_new_point(x_now,x_prev,t_prev,t_now,y_prev,y_now,
                      diff_var_threshold_value,diff_var_threshold_value_prev):
    '''
    Computes new time t_new and vectors x_new, y_new for which a state variable
    equals a threshold value.
    :param x_now: state vector at the present iteration
    :param x_prev: state vector at the previous iteration
    :param t_prev: time at the previous iteration
    :param t_now: time at the present iteration
    :param y_prev: output vector at the previous iteration
    :param y_now: output vector at the present iteration
    :param diff_var_threshold_value: differences between the output variable and
        the threshold value at the present iteration
    :param diff_var_threshold_value_prev: differences between the output variable
        and the threshold value at the previous iteration
    :return: new time t_new and vectors x_new, y_new
    '''
    t_new=(-t_prev*diff_var_threshold_value+t_now*diff_var_threshold_value_prev)/\
          (diff_var_threshold_value_prev-diff_var_threshold_value)
    h_new=t_new-t_prev
    x_new,y_new=interpolation(x_prev,y_prev,t_prev,x_now,y_now,t_now,t_new)
    return x_new,h_new,t_new,y_new

def interp_state_chgt(x_prev,y_prev,y_target,t_prev,x_now,y_now,t_now,f,i_prev,
                      h_prev,c_now):
    '''
    Tests if there is a changement of configuration of the ODE system at the
    present time.
    :param x_prev: state vector at the previous iteration
    :param y_prev: output vector at the previous iteration
    :param y_target: new output vector after changement of configuration
    :param t_prev: time at the previous iteration
    :param x_now: state vector at the present iteration
    :param y_now: output vector at the present iteration
    :param t_now: time at the present iteration
    :param f: a class that describes the ODE system
    :param i_prev: configuration of the system at the previous iteration
    :param h_prev: step size from the present iteration
    :param c_now: command of the ODE system for the present iteration
    :return: the new state vector x_now, outputs vector y_now, time t_now,
        the optimal step size for next iteration h_now.
    '''
    ind=np.where(np.array_equiv(y_now,y_target),-1,np.argmax(np.abs(y_now-
                                                                    y_target)))
    threshold_value=y_target[ind]
    diff_var_threshold_value=y_now[ind]-threshold_value
    diff_var_threshold_value_prev=y_prev[ind]-threshold_value
    condition = np.bitwise_and(np.sign(diff_var_threshold_value)!=np.sign(
            diff_var_threshold_value_prev),np.not_equal(ind,-1))
    condition=np.bitwise_and(condition,np.bitwise_not(np.allclose(
            diff_var_threshold_value_prev,0.)))
    x_now,h_now,t_now,y_now=cond(condition,lambda state:compute_new_point(
        x_now,x_prev,t_prev,t_now,y_prev,y_now,diff_var_threshold_value,
        diff_var_threshold_value_prev),lambda state:state,(x_now,h_prev,t_now,
                                                           y_now))
    if hasattr(f,'commande') and hasattr(f,'state'):
        _,x_now,y_now=f.update(x_now,y_now,t_now,c_now)
    elif not hasattr(f,'commande') and hasattr(f,'state'):
        _,x_now,y_now=f.update(x_now,y_now,t_now)
    else:
        x_now,y_now=f.update(x_now,y_now,t_now)
    return x_now,y_now,h_now,t_now

def next_step_simulation(x_prev,t_prev,y_prev,i_prev,c_prev,h_prev,f,tol,T,*P):
    '''
    Computes the state vector, output vector and time at the present iteration.
    :param x_prev: the state vector at the previous iteration
    :param t_prev: the time at the previous iteration
    :param y_prev: the output at the previous iteration
    :param i_prev: configuration of the system at the previous iteration
    :param c_prev: command of the system at the previous iteration
    :param h_prev: step size from the present iteration
    :param f: a class that describes the ODE system
    :param tol: tolerance for optimal step size computation
    :param T: operating period of the system (facultative)
    :param P: optimization inputs
    :return: the state vector x_now, outputs vector y_now, time t_now,
        configuration i_now, commande c_now at the present iteration,
        the optimal step size for next iteration h_now.
    '''
    if hasattr(f,'state'):
        f.state=i_prev
    if hasattr(f,'initialize'):
        P=f.initialize(*P)
    x_now,x_now_est,t_now=rk_step(x_prev,t_prev,h_prev,f,*P)
    if hasattr(f,'computeotherX'):
        x_now=f.computeotherX(x_now,t_now,*P)
        x_now_est=f.computeotherX(x_now_est,t_now,*P)
    y_now=f.output(x_now,t_now,*P)
    h_now,c_now,tpdi=0.,0,0.
    if hasattr(f,'update') and hasattr(f,'state'):
        if hasattr(f,'commande'):
            tpdi,c_now=f.commande(t_now,T)
            i_now,_,y_target=f.update(x_now,y_now,t_now,c_now)
        else:
            c_now=c_prev
            i_now,_,y_target=f.update(x_now,y_now,t_now)
        x_now,y_now,h_now,t_now=cond(np.bitwise_not(np.allclose(i_prev,i_now)),
            lambda state:interp_state_chgt(x_prev,y_prev,y_target,t_prev,x_now,
            y_now,t_now,f,i_prev,h_prev,c_now), lambda state:state,(x_now,y_now,
            h_now,t_now))

        y_now=f.output(x_now,t_now,*P)
        h_now= optimal_step(x_now,x_now_est, h_prev, tol,x_prev)
        if hasattr(f,'commande'):
            h_now=np.minimum(tpdi-t_now,h_now)
        h_now=np.where(np.bitwise_not(np.allclose(i_prev,i_now)),1e-9,h_now) # pour accelerer code
    else:
        i_now=i_prev
        c_now=c_now
    if hasattr(f,'update') and not hasattr(f,'state'):
        _,y_target=f.update(x_now,y_now,t_now)
        x_now,y_now,h_now,t_now=interp_state_chgt(x_prev,y_prev,y_target,t_prev,
                                    x_now,y_now,t_now,f,i_prev,h_prev,c_now)
        y_now=f.output(x_now,t_now,*P)
        h_now = optimal_step(x_now, x_now_est, h_prev, tol,x_prev)
    elif not hasattr(f,'state') and not hasattr(f,'update'):
        h_now = optimal_step(x_now, x_now_est, h_prev, tol,x_prev)
    return x_now,t_now,y_now,h_now,i_now,c_now

@partial(custom_jvp,nondiff_argnums=(0,1,2))
def _odeint45(f,h0,tol,x0,vect_t,T,*P):

    def scan_fun(state,te):

        def cond_fn(state):
            x_prev,t_prev,y_prev,h_prev,i_prev,c_prev=state
            return (t_prev<te) & (h_prev>0)

        def body_fn(state):
            x_prev,t_prev,y_prev,h_prev,i_prev,c_prev=state

            x_now,t_now,y_now,h_now,i_now,c_now=next_step_simulation(x_prev,
                                t_prev,y_prev,i_prev,c_prev,h_prev,f,tol,T,*P)

            # to reach te
            h_now=np.minimum(h_now,te-t_prev)

            return x_now,t_now,y_now,h_now,i_now,c_now

        x_now,t_now,y_now,h_now,i_now,c_now = while_loop(cond_fn,body_fn,state)

        return (x_now,t_now,y_now,h_now,i_now,c_now),(x_now,y_now,i_now)

    if hasattr(f,'state'):
        i0=f.state
    else:
        i0=0
    if hasattr(f,'commande'):
        _,c0=f.commande(vect_t[0],T)
    else:
        c0=0
    tempP=None
    if hasattr(f,'initialize'):
        tempP=P
        P=f.initialize(*P)
    y0=f.output(x0,0.,*P)
    if hasattr(f,'initialize'):
        P=tempP
    vect,(xf,yf,states)=scan(scan_fun,(x0,vect_t[0],y0,h0,i0,c0),vect_t[1:])
    if hasattr(f,'state'):
        f.state=vect[4]
    xf=np.transpose(np.concatenate((x0[None], xf)))
    yf=np.transpose(np.concatenate((y0[None], yf)))
    if hasattr(f,'state'):
        if isinstance(i0,int):
            states=np.insert(states,0,i0)
        else:
            states=np.transpose(np.concatenate((i0[None], states)))
        return xf,yf,states
    else:
        return xf,yf


@_odeint45.defjvp
def _odeint45_jvp(f,h0,tol, primals, tangents):
    '''
    Solves an ODE system described by df/dP with Runge-Kutta 45 algorithm.
    :param f: a class that describes the ODE system
    :param h0: initial step size
    :param tol: tolerance for optimal step size computation
    :param primals: tuple including initial state vector, time vector, operating
        period and optimization inputs.
    :param tangents: tuple including differentials of initial state vector,
        operating period and optimization inputs.
    :return: a matrix xf with state vector values across time, and a matrix yf
        with output vector values across time, their respective derivatives
        w.r.t P (dxf and dyf), and a matrix states with configurations across
        time for periodic systems.
    '''
    x0, vect_t,T, *P = primals
    dx0, _,_, *dP = tangents
    nPdP = len(P)

    if hasattr(f,'state'):
        xf,dxf,yf,dyf,states=odeint45_etendu(f,nPdP,h0,tol,x0,x0,vect_t,T,*P,*dP)
        return (xf,yf,states),(dxf,dyf,states)
    else:
        xf,dxf,yf,dyf = odeint45_etendu(f,nPdP,h0,tol,x0,dx0,vect_t,T,*P,*dP)
        return (xf,yf),(dxf,dyf)

def f_grads(x,dx, t, f,nPdP, *P_and_dP):
    '''
    Computes the derivatives of state vector w.r.t P.
    :param x: state vector values
    :param dx: differential of state vector
    :param t: time at present iteration
    :param f: a class that describes the ODE system
    :param nPdP: length of optimization inputs
    :param P_and_dP: optimization inputs values and differentials
    :return: the derivatives of state vector w.r.t P.
    '''
    P, dP = P_and_dP[:nPdP], P_and_dP[nPdP:]
    res, dres = jvp(f.derivative, (x, t, *P), (dx,0., *dP))
    return dres

def rk45_step_der(x_prev, t_prev, dx_prev,h_prev,f,nPdP,*P_and_dP):
    '''
    An iteration of the Runge-Kutta 45 algorithm for the ODE system described
    by df/dP.
    :param x_prev: the state vector at the previous iteration
    :param t_prev: the time at the previous iteration
    :param dx_prev: the differential of state vector at the previous iteration
    :param h: constant step size
    :param h_prev: step size for the present iteration
    :param f: a class that describes the ODE system.
    :param nPdP: length of optimization inputs
    :param P_and_dP: optimization inputs values and differentials
    :return: dx/dp and x at the present iteration.
    '''
    P=P_and_dP[:nPdP]
    k1=f.derivative(x_prev, t_prev,*P)
    k2 = f.derivative(x_prev + h_prev*0.2 * k1, t_prev + 0.2 * h_prev,*P)
    k3=f.derivative(x_prev + h_prev*(3 * k1 +9*k2)/40,t_prev + 3 *h_prev /10,*P)
    k4 = f.derivative(x_prev + h_prev*(44 * k1 / 45 - 56 * k2 / 15 + 32 * k3/9),
                      t_prev + 4 * h_prev / 5,*P)
    k5 = f.derivative(x_prev + h_prev*(19372 * k1 / 6561 - 25360 * k2 / 2187 +
            64448 * k3 / 6561- 212 * k4 / 729),t_prev + 8 * h_prev / 9,*P)

    dk1 = f_grads(x_prev, dx_prev, t_prev,f,nPdP, *P_and_dP)
    dk2 = f_grads(x_prev+ h_prev*0.2 * k1, dx_prev + h_prev * 0.2 * dk1,t_prev +
                0.2 * h_prev ,f,nPdP, *P_and_dP)
    dk3 = f_grads(x_prev+ h_prev*(3 * k1 + 9 * k2) / 40,dx_prev+h_prev *(3 * dk1
                + 9 * dk2) / 40,t_prev+3 * h_prev / 10,f,nPdP, *P_and_dP)
    dk4 = f_grads(x_prev+ h_prev*(44 * k1 / 45 - 56 * k2 / 15 + 32 * k3 / 9),
                dx_prev +h_prev*(44 * dk1 / 45 - 56 * dk2 /15+32*dk3/9),
                t_prev + 4 * h_prev / 5,f,nPdP,*P_and_dP)
    dk5 = f_grads(x_prev+ h_prev*(19372 * k1 / 6561 - 25360 * k2 / 2187 +
            64448 * k3 / 6561- 212 * k4 / 729), dx_prev + h_prev *
        (19372 * dk1 / 6561 - 25360*dk2/2187+ 64448 * dk3 / 6561 - 212 * dk4
            / 729),t_prev + 8 * h_prev / 9,f,nPdP, *P_and_dP)
    dk6 = f_grads(x_prev+ h_prev*(9017 * k1 / 3168 - 355* k2 / 33+46732*k3/5247+
            49 * k4 / 176 - 5103 * k5 / 18656),dx_prev+h_prev*(9017 *
            dk1 / 3168 -355 *dk2/33 +46732*dk3/5247 + 49 * dk4 / 176 - 5103 *
            dk5 / 18656),t_prev + h_prev,f,nPdP,*P_and_dP)
    dx_now = dx_prev + h_prev *(35 * dk1 / 384 + 500 * dk3 / 1113 +
            125 * dk4 / 192 - 2187 * dk5 / 6784 + 11 * dk6 / 84)
    return dx_now

def next_der_step_simulation(x_prev,t_prev,dx_prev,x_now,t_now,h_prev,f,
                             nPdP,chgt_state,Mat,dMat,*P_and_dP):
    '''
    Computes the state vector, output vector, their derivatives and time at
    the present iteration.
    :param x_prev: the state vector at the previous iteration
    :param t_prev: the time at the previous iteration
    :param dx_prev: the differentials of the state vector at the previous iteration
    :param h: constant step size
    :param x_now: state vector at the present iteration
    :param t_now: time at the present iteration
    :param h_prev: step size for the present iteration
    :param f: a class that describes the ODE system
    :param nPdP: length of optimization inputs
    :param chgt_state: bool which indicates if system changed configuration
                       the previous iteration
    :param Mat: state matrices at the present iteration
    :param dMat: derivatives of state matrices at the present iteration
    :param P_and_dP: optimization inputs values and differentials
    :return: the derivatives of state and output vectors dx_now, dy_now, and
    state matrices Mat and their derivatives at the next iteration.
    '''
    P,dP = P_and_dP[:nPdP],P_and_dP[nPdP:]
    if hasattr(f, 'initialize'):
        P,dP = cond(chgt_state,lambda state:jvp(f.initialize, (*P,), (*dP,)),
                    lambda state:state,(Mat,dMat))
        P_and_dP=P+dP
        Mat,dMat=P,dP
        nPdP=len(P)
    dx_now=rk45_step_der(x_prev,t_prev,dx_prev,h_prev,f,nPdP,*P_and_dP)
    dx_now=np.where(np.abs(dx_now)>1e12,np.sign(dx_now)*1e12,dx_now)
    if hasattr(f, 'computeotherX'):
        dx_now = jvp(f.computeotherX, (x_now,t_now,*P), (dx_now, 0., *dP))[1]
    dy_now = jvp(f.output, (x_now, t_now, *P), (dx_now, 0., *dP))[1]
    return dx_now,dy_now,Mat,dMat

def odeint45_etendu(f,nPdP,h0,tol,x0,dx0,vect_t,T,*P_and_dP):
    P,dP = P_and_dP[:nPdP],P_and_dP[nPdP:]
    dh=vect_t[1]-vect_t[0]

    def scan_fun(state, te):

        def cond_fn(state):
            x_prev,t_prev,y_prev,h_prev,i_prev2,i_prev,c_prev=state
            return (t_prev<te) & (h_prev>0)

        def body_fn(state):
            x_prev,t_prev,y_prev,h_prev,i_prev2,i_prev,c_prev=state

            x_now,t_now,y_now,h_now,i_now,c_now=next_step_simulation(x_prev,
                                t_prev,y_prev,i_prev,c_prev,h_prev,f,tol,T,*P)

            # to reach te
            h_now=np.minimum(h_now,te-t_prev)

            return x_now,t_now,y_now,h_now,i_prev,i_now,c_now

        x_prev,dx_prev,t_prev,y_prev,dy_prev,h_prev,i_prev,c_prev,Mat,dMat,\
            chgt_state=state
        x_now,t_now,y_now,h_now,i_prev,i_now,c_now = while_loop(
            cond_fn,body_fn, (x_prev,t_prev,y_prev,h_prev,i_prev,i_prev,c_prev))

        if hasattr(f,'state'):
            f.state=i_prev
        dx_now,dy_now,Mat,dMat=next_der_step_simulation(x_prev,t_prev,dx_prev,
                            x_now,t_now,dh,f,nPdP,chgt_state,Mat,dMat,*P_and_dP)
        chgt_state=np.bitwise_not(np.array_equal(i_now,i_prev))

        return (x_now,dx_now,t_now,y_now,dy_now,h_now,i_now,c_now,Mat,dMat,
                chgt_state),(x_now,dx_now,y_now,dy_now,i_now)

    for element in f.__dict__.keys(): # pour eviter erreurs de code
        if hasattr(f.__dict__[element],'primal'):
            f.__dict__[element]=f.__dict__[element].primal
    if hasattr(f,'state'):
        i0=f.state
    else:
        i0=0
    if hasattr(f,'commande'):
        _,c0=f.commande(vect_t[0],T)
    else:
        c0=0
    tempP,tempdP,Mat,dMat=None,None,0,0
    if hasattr(f,'initialize'):
        tempP,tempdP=P,dP
        P,dP=jvp(f.initialize,(*P,),(*dP,))
        Mat,dMat=P,dP
    y0=f.output(x0,0.,*P)
    dy0=jvp(f.output,(x0,0.,*P),(dx0,0.,*dP))[1]
    if hasattr(f,'initialize'):
        P,dP=tempP,tempdP
    chgt_state=False
    vect,(xf,dxf,yf,dyf,states)=scan(scan_fun,(x0,dx0,vect_t[0],y0,dy0,h0,i0,
                                               c0,Mat,dMat,chgt_state),vect_t[1:])
    if hasattr(f,'state'):
        f.state=vect[6]
    xf=np.transpose(np.concatenate((x0[None], xf)))
    yf=np.transpose(np.concatenate((y0[None], yf)))
    dxf=np.transpose(np.concatenate((dx0[None], dxf)))
    dyf = np.transpose(np.concatenate((dy0[None], dyf)))
    if hasattr(f,'state'):
        if isinstance(i0,int):
            states=np.insert(states,0,i0)
        else:
            states=np.transpose(np.concatenate((i0[None], states)))
        return xf,dxf,yf,dyf,states
    else:
        return xf,dxf,yf,dyf
