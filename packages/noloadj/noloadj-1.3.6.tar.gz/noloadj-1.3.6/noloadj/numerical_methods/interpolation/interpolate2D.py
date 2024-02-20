import jax.numpy as np
from jax.lax import *
from jax import custom_jvp,jvp
from functools import partial

@partial(custom_jvp,nondiff_argnums=(0,1,2))
def interpolate2D(arrayX1,arrayX2,arrayY,b,l):
    numberOfInputX1=len(arrayX1)
    numberOfInputX2 = len(arrayX2)
    wt = np.array(
        [[1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
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

    x1l,x1u,x2l,x2u = 0.0,0.0,0.0,0.0
    ya = np.zeros(4)
    y1a = np.zeros(4)
    y2a = np.zeros(4)
    y12a = np.zeros(4)
    err, j, k = 0, -1, -1

    def while_cond(state):
        b,j=state
        return b >= arrayX1[j + 1]
    def while_func(state):
        b,j=state
        return b,j+1
    _,j = while_loop(while_cond, while_func, (b,j))

    def while_cond1(state):
        l,k=state
        return l >= arrayX2[k + 1]
    def while_func1(state):
        l,k=state
        return l,k+1
    _,k = while_loop(while_cond1, while_func1, (l,k))

    condition = np.bitwise_or(np.bitwise_or(j == -1, j == numberOfInputX1 - 1),
                              np.bitwise_or(k == -1, k == numberOfInputX2 - 1))

    def true_fn(state):
        x1l, x1u, x2l, x2u, ya, err = state
        err = 1
        return x1l, x1u, x2l, x2u, ya, err

    def false_fn(state):
        x1l, x1u, x2l, x2u, ya, err = state
        x1l = arrayX1[j]
        x1u = arrayX1[j + 1]
        x2l = arrayX2[k]
        x2u = arrayX2[k + 1]
        ya = ya.at[0].set(arrayY[k][j])
        ya = ya.at[1].set(arrayY[k][j + 1])
        ya = ya.at[2].set(arrayY[k + 1][j + 1])
        ya = ya.at[3].set(arrayY[k + 1][j])
        return x1l, x1u, x2l, x2u, ya, err

    x1l, x1u, x2l, x2u, ya, err = cond(condition, true_fn, false_fn,
                                       (x1l, x1u, x2l, x2u, ya, err))

    y1a = y1a.at[0].set(np.where(j == 0, 0.,
                                 (arrayY[k][j + 1] - arrayY[k][j - 1]) / (
                                             arrayX1[j + 1] - arrayX1[j - 1])))
    y1a = y1a.at[3].set(np.where(j == 0, 0., (
                arrayY[k + 1][j + 1] - arrayY[k + 1][j - 1]) / (
                                             arrayX1[j + 1] - arrayX1[j - 1])))

    y1a = y1a.at[1].set(np.where(j == numberOfInputX1 - 2, 0.,
                                 (arrayY[k][j + 2] - arrayY[k][j]) / (
                                             arrayX1[j + 2] - arrayX1[j])))
    y1a = y1a.at[2].set(np.where(j == numberOfInputX1 - 2, 0.,
                                 (arrayY[k + 1][j + 2] - arrayY[k + 1][j]) / (
                                             arrayX1[j + 2] - arrayX1[j])))

    y2a = y2a.at[0].set(np.where(k == 0, 0.,
                                 (arrayY[k + 1][j] - arrayY[k - 1][j]) / (
                                             arrayX2[k + 1] - arrayX2[k - 1])))
    y2a = y2a.at[1].set(np.where(k == 0, 0., (
                arrayY[k + 1][j + 1] - arrayY[k - 1][j + 1]) / (
                                             arrayX2[k + 1] - arrayX2[k - 1])))

    y2a = y2a.at[2].set(np.where(k == numberOfInputX2 - 2, 0.,
                                 (arrayY[k + 2][j + 1] - arrayY[k][j + 1]) / (
                                             arrayX2[k + 2] - arrayX2[k])))
    y2a = y2a.at[3].set(np.where(k == numberOfInputX2 - 2, 0.,
                                 (arrayY[k + 2][j] - arrayY[k][j]) / (
                                             arrayX2[k + 2] - arrayX2[k])))

    y12a = y12a.at[0].set(np.where(np.bitwise_or(j == 0, k == 0), 0., (
                arrayY[k + 1][j + 1] - arrayY[k - 1][j + 1] - arrayY[k + 1][
            j - 1] + arrayY[k - 1][j - 1]) / ((arrayX1[j + 1] - arrayX1[
        j - 1]) * (arrayX2[k + 1] - arrayX2[k - 1]))))

    y12a = y12a.at[1].set(
        np.where(np.bitwise_or(j == numberOfInputX1 - 2, k == 0), 0., (
                    arrayY[k + 1][j + 2] - arrayY[k - 1][j + 2] - arrayY[k + 1][
                j] + arrayY[k - 1][j]) / ((arrayX1[j + 2] - arrayX1[j]) * (
                    arrayX2[k + 1] - arrayX2[k - 1]))))

    y12a = y12a.at[2].set(np.where(
        np.bitwise_or(j == numberOfInputX1 - 2, k == numberOfInputX2 - 2), 0., (
                    arrayY[k + 2][j + 2] - arrayY[k][j + 2] - arrayY[k + 2][j] +
                    arrayY[k][j]) / ((arrayX1[j + 2] - arrayX1[j]) * (
                    arrayX2[k + 2] - arrayX2[k]))))

    y12a = y12a.at[3].set(
        np.where(np.bitwise_or(j == 0, k == numberOfInputX2 - 2), 0., (
                    arrayY[k + 2][j + 1] - arrayY[k][j + 1] - arrayY[k + 2][
                j - 1] + arrayY[k][j - 1]) / (
                             (arrayX1[j + 1] - arrayX1[j - 1]) * (
                                 arrayX2[k + 2] - arrayX2[k]))))


    ansy = 0.0
    err = 0
    c = np.zeros((4,4))
    c1 = np.zeros(16)
    x = np.zeros(16)
    d1 = x1u - x1l
    d2 = x2u - x2l
    d1d2 = d1 * d2

    for i in range(4):
        x = x.at[i].set(ya[i])
        x = x.at[i + 4].set(y1a[i] * d1)
        x = x.at[i + 8].set(y2a[i] * d2)
        x = x.at[i + 12].set(y12a[i] * d1d2)

    for i in range(16):
        xx = np.dot(wt[i], x)
        c1 = c1.at[i].set(xx)
    l1 = -1

    for i in range(4):
        for j in range(4):
            l1 = l1 + 1
            c=c.at[i,j].set(c1[l1])

    condition = np.bitwise_or(x1u == x1l, x2u == x2l)

    def true_fn(state):
        err, ansy = state
        err = 1
        return err, ansy

    def false_fn(state):
        err, ansy = state
        t = (b - x1l) / (x1u - x1l)
        u = (l - x2l) / (x2u - x2l)
        for i in range(3, -1, -1):
            ansy = t * ansy + c[i][3] * u * u * u + c[i][2] * u * u + c[i][
                1] * u + c[i][0]
        return err, ansy

    err, ansy = cond(condition, true_fn, false_fn, (err, ansy))

    return ansy


@interpolate2D.defjvp
def interpolate2d_jvp(arrayX1,arrayX2,arrayY,primals,tangents):
    b,l=primals
    db,dl=tangents
    numberOfInputX1 = len(arrayX1)
    numberOfInputX2 = len(arrayX2)
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

    x1l, x1u, x2l, x2u = 0.0, 0.0, 0.0, 0.0
    ya = np.zeros(4)
    y1a = np.zeros(4)
    y2a = np.zeros(4)
    y12a = np.zeros(4)
    err, j, k = 0, -1, -1

    def while_cond(state):
        b, j = state
        return b >= arrayX1[j + 1]

    def while_func(state):
        b, j = state
        return b, j + 1

    _, j = while_loop(while_cond, while_func, (b, j))

    def while_cond1(state):
        l, k = state
        return l >= arrayX2[k + 1]

    def while_func1(state):
        l, k = state
        return l, k + 1

    _, k = while_loop(while_cond1, while_func1, (l, k))

    condition = np.bitwise_or(np.bitwise_or(j == -1, j == numberOfInputX1 - 1),
                              np.bitwise_or(k == -1, k == numberOfInputX2 - 1))

    def true_fn(state):
        x1l, x1u, x2l, x2u, ya, err = state
        err = 1
        return x1l, x1u, x2l, x2u, ya, err

    def false_fn(state):
        x1l, x1u, x2l, x2u, ya, err = state
        x1l = arrayX1[j]
        x1u = arrayX1[j + 1]
        x2l = arrayX2[k]
        x2u = arrayX2[k + 1]
        ya = ya.at[0].set(arrayY[k][j])
        ya = ya.at[1].set(arrayY[k][j + 1])
        ya = ya.at[2].set(arrayY[k + 1][j + 1])
        ya = ya.at[3].set(arrayY[k + 1][j])
        return x1l, x1u, x2l, x2u, ya, err

    x1l, x1u, x2l, x2u, ya, err = cond(condition, true_fn, false_fn,
                                       (x1l, x1u, x2l, x2u, ya, err))

    y1a = y1a.at[0].set(np.where(j == 0, 0.,
                                 (arrayY[k][j + 1] - arrayY[k][j - 1]) / (
                                         arrayX1[j + 1] - arrayX1[j - 1])))
    y1a = y1a.at[3].set(np.where(j == 0, 0., (
            arrayY[k + 1][j + 1] - arrayY[k + 1][j - 1]) / (
                                         arrayX1[j + 1] - arrayX1[j - 1])))

    y1a = y1a.at[1].set(np.where(j == numberOfInputX1 - 2, 0.,
                                 (arrayY[k][j + 2] - arrayY[k][j]) / (
                                         arrayX1[j + 2] - arrayX1[j])))
    y1a = y1a.at[2].set(np.where(j == numberOfInputX1 - 2, 0.,
                                 (arrayY[k + 1][j + 2] - arrayY[k + 1][j]) / (
                                         arrayX1[j + 2] - arrayX1[j])))

    y2a = y2a.at[0].set(np.where(k == 0, 0.,
                                 (arrayY[k + 1][j] - arrayY[k - 1][j]) / (
                                         arrayX2[k + 1] - arrayX2[k - 1])))
    y2a = y2a.at[1].set(np.where(k == 0, 0., (
            arrayY[k + 1][j + 1] - arrayY[k - 1][j + 1]) / (
                                         arrayX2[k + 1] - arrayX2[k - 1])))

    y2a = y2a.at[2].set(np.where(k == numberOfInputX2 - 2, 0.,
                                 (arrayY[k + 2][j + 1] - arrayY[k][j + 1]) / (
                                         arrayX2[k + 2] - arrayX2[k])))
    y2a = y2a.at[3].set(np.where(k == numberOfInputX2 - 2, 0.,
                                 (arrayY[k + 2][j] - arrayY[k][j]) / (
                                         arrayX2[k + 2] - arrayX2[k])))

    y12a = y12a.at[0].set(np.where(np.bitwise_or(j == 0, k == 0), 0., (
            arrayY[k + 1][j + 1] - arrayY[k - 1][j + 1] - arrayY[k + 1][
        j - 1] + arrayY[k - 1][j - 1]) / ((arrayX1[j + 1] - arrayX1[
        j - 1]) * (arrayX2[k + 1] - arrayX2[k - 1]))))

    y12a = y12a.at[1].set(
        np.where(np.bitwise_or(j == numberOfInputX1 - 2, k == 0), 0., (
                arrayY[k + 1][j + 2] - arrayY[k - 1][j + 2] - arrayY[k + 1][
            j] + arrayY[k - 1][j]) / ((arrayX1[j + 2] - arrayX1[j]) * (
                arrayX2[k + 1] - arrayX2[k - 1]))))

    y12a = y12a.at[2].set(np.where(
        np.bitwise_or(j == numberOfInputX1 - 2, k == numberOfInputX2 - 2), 0., (
            arrayY[ k + 2][j + 2] -arrayY[k][j + 2] - arrayY[k + 2][j] +arrayY[
            k][j]) / ((arrayX1[j + 2] -arrayX1[j]) * (arrayX2[ k + 2] -
            arrayX2[k]))))

    y12a = y12a.at[3].set(
        np.where(np.bitwise_or(j == 0, k == numberOfInputX2 - 2), 0., (
                arrayY[k + 2][j + 1] - arrayY[k][j + 1] - arrayY[k + 2][
            j - 1] + arrayY[k][j - 1]) / (
                         (arrayX1[j + 1] - arrayX1[j - 1]) * (
                         arrayX2[k + 2] - arrayX2[k]))))

    ansy = 0.0
    ansy1 = 0.0
    ansy2 = 0.0
    err = 0
    c = np.zeros((4,4))
    c1 = np.zeros(16)
    x = np.zeros(16)
    d1 = x1u - x1l
    d2 = x2u - x2l
    d1d2 = d1 * d2

    for i in range(4):
        x = x.at[i].set(ya[i])
        x = x.at[i + 4].set(y1a[i] * d1)
        x = x.at[i + 8].set(y2a[i] * d2)
        x = x.at[i + 12].set(y12a[i] * d1d2)

    for i in range(16):
        xx = np.dot(wt[i], x)
        c1 = c1.at[i].set(xx)

    l1 = -1
    for i in range(4):
        for j in range(4):
            l1 = l1 + 1
            c=c.at[i,j].set(c1[l1])

    condition = np.bitwise_or(x1u == x1l, x2u == x2l)

    def true_fn(state):
        err, ansy,ansy1,ansy2 = state
        err = 1
        return err, ansy,ansy1,ansy2

    def false_fn(state):
        err, ansy,ansy1,ansy2 = state
        t = (b - x1l) / (x1u - x1l)
        u = (l - x2l) / (x2u - x2l)
        for i in range(3, -1, -1):
            ansy = t * ansy + c[i][3] * u * u * u + c[i][2] * u * u + c[i][
                1] * u + c[i][0]
            ansy1 = u * ansy1 + 3.0 * c[3][i] * t * t + 2.0 * c[2][i] * t + \
                    c[1][i]
            ansy2 = t * ansy2 + 3.0 * c[i][3] * u * u + 2.0 * c[i][2] * u + \
                    c[i][1]
        ansy1 = ansy1 / (x1u - x1l)
        ansy2 = ansy2 / (x2u - x2l)
        return err, ansy,ansy1,ansy2

    err,ansy,ansy1,ansy2=cond(condition,true_fn,false_fn,(err,ansy,ansy1,ansy2))

    return ansy,ansy1*db+ansy2*dl


if __name__ == '__main__':
    Iq=np.linspace(-60.,60.,13)
    Id=np.linspace(-60.,60.,13)

    Flux=np.array([[-0.00936759,-0.009137568,-0.00925056,-0.009260159,
       -0.00880541,-0.008513355,-0.008561574,-0.008513595,-0.008807394,
       -0.009261084,-0.009244172,-0.009127824,-0.009358793],
      [0.002425953,0.002711467,0.002643147,0.002574105,0.002629419,0.002804502,
       0.002776581,0.002805116,0.002629193,0.002572187,0.002647032,0.00271644,
       0.002429907],
      [0.012450222,0.012924463,0.013198778,0.013693866,0.013928963,0.014197782,
       0.014231743,0.014198133,0.013929756,0.013693002,0.013197671,0.012926871,
       0.012456589],
      [0.021710196,0.022589178,0.023509056,0.024318524,0.024968138,0.025349264,
        0.025465012,0.025348991,0.024969062,0.024318484,0.023505713,0.022585049,
        0.021705225],
      [0.030413199,0.03185054,0.03348364,0.03466354,0.035629444,0.036272091,
        0.036453664,0.03627199,0.035629707,0.034663717,0.033478889,0.031849873,
        0.030412909],
      [0.038996204,0.040772462,0.04291516,0.044746952,0.045969456,0.04696552,
        0.047234733,0.046965524	,0.045969001,0.044747363,0.042917148,
        0.040768193,0.038995787],
      [0.046637605,0.048909493,0.051495095,0.054004898,0.055937554,0.057250521,
        0.057751081,0.057250674,0.055937228,0.054004752,0.051494442,0.048909265,
        0.046641159],
      [0.052904324,0.05567639,0.058488035,0.061284236,0.063922871,0.065864582,
        0.066976852	,0.065864852,0.063921535,0.061283565,0.058488303,
        0.055677537,0.052906423],
      [0.058822228,0.061770741,0.064689964,0.067696432,0.070605533,0.072665297,
        0.073602932,0.072667309,0.070608571,0.067697678,0.064691444,0.061771625,
        0.058821659],
      [0.064172317,0.067216276,0.070330744,0.073500193,0.076247708,0.078086052,
        0.078906567,0.078087913,0.07625046	,0.07350537,0.070333525,0.067216593,
        0.064173218],
      [0.06911543,0.072263911,0.07547482,	0.07837175,	0.080867628,0.082648269,
        0.083446074,0.082650267,0.080870219,0.078376475,0.075478778,0.072264501,
        0.069114397],
      [0.073746666,0.076894948,0.079717995,0.082426704,0.084781266,0.086583136,
        0.087254323,0.086584429,0.084783784,0.082431441,0.079723539,0.076898369,
        0.073746518],
      [0.077986598,0.080718175,0.083309856,0.085912595,0.088147893,0.089934449,
        0.090478678,0.089934702,0.088147785,0.08591446,0.083315747,0.080726387,
        0.077989953]])

    #Interpolation2D
    res=interpolate2D(Iq,Id,Flux,-40.,-40.)
    print(res)
    #custom_jvp
    dI=np.zeros(13)
    dF=np.zeros((13,13))
    _,dres=jvp(interpolate2D,(Iq,Id,Flux,-40.,-40.),(dI,dI,dF,1.0,1.0))
    print(dres)

    # differences finies
    res_Id=interpolate2D(Iq,Id,Flux,-40.,-39.999)
    res_Iq=interpolate2D(Iq,Id,Flux,-39.999,-40.)
    res_jvp=(res_Iq-res)/0.001+(res_Id-res)/0.001
    print(res_jvp)