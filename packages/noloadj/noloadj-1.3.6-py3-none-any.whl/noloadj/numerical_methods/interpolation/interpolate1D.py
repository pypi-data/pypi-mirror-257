import jax.numpy as np
from jax.lax import *
from jax import custom_jvp,jvp
from functools import partial

@partial(custom_jvp,nondiff_argnums=(0,1))
def interpolate1D(inputX,inputY,b):
    numberOfInputX=len(inputX)
    wt = np.array([
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
        [-3., 0., 0., 3., 0., 0., 0., 0., -2., 0., 0., -1., 0., 0., 0., 0.],
        [2., 0., 0., -2., 0., 0., 0., 0., 1., 0., 0., 1., 0., 0., 0., 0.],
        [0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0.],
        [0., 0., 0., 0., -3., 0., 0., 3., 0., 0., 0., 0., -2., 0., 0., -1.],
        [0., 0., 0., 0., 2., 0., 0., -2., 0., 0., 0., 0., 1., 0., 0., 1.],
        [-3., 3., 0., 0., -2., -1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., -3., 3., 0., 0., -2., -1., 0., 0.],
        [9., -9., 9., -9., 6., 3., -3., -6., 6., -6., -3., 3., 4., 2., 1., 2.],
        [-6., 6., -6., 6., -4., -2., 2., 4., -3., 3., 3., -3., -2.,-1.,-1.,-2.],
        [2., -2., 0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 2., -2., 0., 0., 1., 1., 0., 0.],
        [-6., 6., -6., 6., -3., -3., 3., 3., -4., 4., 2., -2.,-2.,-2.,-1.,-1.],
        [4., -4., 4., -4., 2., 2., -2., -2., 2., -2., -2., 2., 1., 1., 1., 1.]])

    x1l, x1u = 0.0, 0.0
    ya = np.zeros(4)
    y1a = np.zeros(4)
    err, j, k = 0, -1, -1

    def while_cond(state):
        b,j=state
        return b >= inputX[j + 1]
    def while_func(state):
        b,j=state
        return b,j+1
    _,j = while_loop(while_cond, while_func, (b,j))

    condition = np.bitwise_or(j == -1, j == numberOfInputX - 1)

    def true_fn(state):
        x1l, x1u, err, ya = state
        err = 1
        return x1l, x1u, err, ya

    def false_fn(state):
        x1l, x1u, err, ya = state
        x1l = inputX[j]
        x1u = inputX[j + 1]
        ya = ya.at[0].set(inputY[j])
        ya = ya.at[1].set(inputY[j + 1])
        return x1l, x1u, err, ya

    x1l, x1u, err, ya = cond(condition, true_fn, false_fn, (x1l, x1u, err, ya))

    y1a = y1a.at[0].set(np.where(j == 0, 0., inputY[j + 1] - inputY[j - 1]) / (
                inputX[j + 1] - inputX[j - 1]))

    y1a = y1a.at[1].set(np.where(j == numberOfInputX - 2, 0.,
                                 (inputY[j + 2] - inputY[j]) / (
                                             inputX[j + 2] - inputX[j])))

    ansy = 0.0
    u = 0.0
    err = 0
    c1 = np.zeros(16)
    x = np.zeros(16)
    c = np.zeros((4,4))

    for i in range(4):
        x = x.at[i].set(ya[i])
        x = x.at[i + 4].set(y1a[i] * (x1u - x1l))

    for i in range(16):
        xx = np.dot(wt[i], x)
        c1 = c1.at[i].set(xx)
    l = -1
    for i in range(4):
        for j in range(4):
            l = l + 1
            c = c.at[i, j].set(c1[l])
    condition = x1u == x1l

    def true_fn(state):
        err, ansy = state
        err = 1
        return err, ansy

    def false_fn(state):
        err, ansy = state
        t = (b - x1l) / (x1u - x1l)
        for i in range(3, -1, -1):
            ansy = t * ansy + c[i][1] * u * u * u + c[i][2] * u * u + c[i][
                1] * u + c[i][0]
        return err, ansy

    err, ansy = cond(condition, true_fn, false_fn, (err, ansy))
    return ansy


@interpolate1D.defjvp
def interpolate1D_jvp(inputX,inputY,primals,tangents):
    b,=primals
    db,=tangents
    numberOfInputX = len(inputX)
    wt = np.array([
        [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
        [-3., 0., 0., 3., 0., 0., 0., 0., -2., 0., 0., -1., 0., 0., 0., 0.],
        [2., 0., 0., -2., 0., 0., 0., 0., 1., 0., 0., 1., 0., 0., 0., 0.],
        [0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0.],
        [0., 0., 0., 0., -3., 0., 0., 3., 0., 0., 0., 0., -2., 0., 0., -1.],
        [0., 0., 0., 0., 2., 0., 0., -2., 0., 0., 0., 0., 1., 0., 0., 1.],
        [-3., 3., 0., 0., -2., -1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., -3., 3., 0., 0., -2., -1., 0., 0.],
        [9., -9., 9., -9., 6., 3., -3., -6., 6., -6., -3., 3., 4., 2., 1., 2.],
        [-6., 6., -6., 6., -4., -2., 2., 4., -3., 3., 3., -3., -2., -1., -1.,
         -2.],
        [2., -2., 0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 2., -2., 0., 0., 1., 1., 0., 0.],
        [-6., 6., -6., 6., -3., -3., 3., 3., -4., 4., 2., -2., -2., -2., -1.,
         -1.],
        [4., -4., 4., -4., 2., 2., -2., -2., 2., -2., -2., 2., 1., 1., 1., 1.]])

    x1l, x1u = 0.0, 0.0
    ya = np.zeros(4)
    y1a = np.zeros(4)
    err, j, k = 0, -1, -1

    def while_cond(state):
        b, j = state
        return b >= inputX[j + 1]

    def while_func(state):
        b, j = state
        return b, j + 1

    _, j = while_loop(while_cond, while_func, (b, j))

    condition = np.bitwise_or(j == -1, j == numberOfInputX - 1)

    def true_fn(state):
        x1l, x1u, err, ya = state
        err = 1
        return x1l, x1u, err, ya

    def false_fn(state):
        x1l, x1u, err, ya = state
        x1l = inputX[j]
        x1u = inputX[j + 1]
        ya = ya.at[0].set(inputY[j])
        ya = ya.at[1].set(inputY[j + 1])
        return x1l, x1u, err, ya

    x1l, x1u, err, ya = cond(condition, true_fn, false_fn, (x1l, x1u, err, ya))

    y1a = y1a.at[0].set(np.where(j == 0, 0., inputY[j + 1] - inputY[j - 1]) / (
            inputX[j + 1] - inputX[j - 1]))

    y1a = y1a.at[1].set(np.where(j == numberOfInputX - 2, 0.,
                                 (inputY[j + 2] - inputY[j]) / (
                                         inputX[j + 2] - inputX[j])))

    ansy = 0.0
    ansy1=0.0
    u = 0.0
    err = 0
    c1 = np.zeros(16)
    x = np.zeros(16)
    c = np.zeros((4,4))

    for i in range(4):
        x = x.at[i].set(ya[i])
        x = x.at[i + 4].set(y1a[i] * (x1u - x1l))

    for i in range(16):
        xx = np.dot(wt[i], x)
        c1 = c1.at[i].set(xx)
    l = -1
    for i in range(4):
        for j in range(4):
            l = l + 1
            c = c.at[i, j].set(c1[l])
    condition = x1u == x1l

    def true_fn(state):
        err, ansy,ansy1 = state
        err = 1
        return err, ansy,ansy1

    def false_fn(state):
        err, ansy,ansy1 = state
        t = (b - x1l) / (x1u - x1l)
        for i in range(3, -1, -1):
            ansy = t * ansy + c[i][1] * u * u * u + c[i][2] * u * u + c[i][
                1] * u + c[i][0]
            ansy1 = 3.0 * c[3][i] * t * t + 2.0 * c[2][i] * t + c[1][i]
        ansy1 = ansy1 / (x1u - x1l)
        return err, ansy,ansy1

    err,ansy,ansy1 = cond(condition, true_fn, false_fn, (err, ansy,ansy1))
    return ansy,ansy1*db


if __name__ == '__main__':
    # Interpolation1D
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([0.0, 0.8, 0.9, 0.1, -0.8, -1.0])
    res1 = interpolate1D(x, y, 1.5)
    print(res1)

    # Jacobian
    dxy = np.zeros(len(x))
    _, dres1 = jvp(interpolate1D, (x, y, 1.5), (dxy, dxy, 1.0))
    print(dres1)

    # finite differences
    res2 = interpolate1D(x, y, 1.5001)
    res_jvp = (res2 - res1) / 0.0001
    print(res_jvp)
