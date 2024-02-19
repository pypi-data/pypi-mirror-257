# https://jmlr.csail.mit.edu/papers/volume9/shafer08a/shafer08a.pdf
# https://nbviewer.org/github/gpeyre/numerical-tours/blob/master/python/ml_11_conformal_prediction.ipynb
# https://github.com/vincentblot28/conformalized_gp
# Conformal prediction CP computes confidence "intervals" associated to any black box prediction method, without assuming any prior model on the sample in the dataset.
# It computes the interval as quantile of runs of the method over the points in the dataset.

import numpy as np
import matplotlib.pyplot as plt


def phi(x):
    # vector feature generator
    return np.concatenate((x * 0 + 1, x, x ** 2, x ** 3), axis=1)


n = 200
X0 = 8 * (np.random.rand(n, 1) - .5) + .5
# True coefficients for each feature
w0 = np.array([0, -5, 0, 1])
#
Y0 = phi(X0) @ w0 + np.random.randn(n) * 7


def hat_w(X, Y):
    return np.linalg.pinv(phi(X)) @ Y


def hat_y(x, w):
    return phi(x) @ w


plt.plot(X0, Y0, '.')
plt.plot(X0, hat_y(X0, hat_w(X0, Y0)), 'r.')
plt.show()


def S(x, y, w):
    """
    S(x,y|X,Y) \triangleq |y-\hat y(x|X,Y)|.
    Parameters
    ----------
    x
    y
    w

    Returns
    -------

    """
    "conformance function S(x,y | X,Y)"
    return np.abs(y - hat_y(x, w))

# Light colors denoting low the conformance function output, i.e., large errors
plt.scatter(X0, Y0, c=S(X0, Y0, hat_w(X0, Y0)), s=15, vmax=10)
plt.plot(X0, hat_y(X0, hat_w(X0, Y0)), 'r.')
plt.show()


def conformal(x, y):
    """
    The conformal prediction compute a score C(x,y|X,Y)
    which is obtained by computing the rank of conformance (S) at the point of interest

    Parameters
    ----------
    x
    y

    Returns
    -------

    """
    V = np.zeros(n)
    w = hat_w(np.append(X0, x).reshape(n + 1, 1), np.append(Y0, y))
    for i in range(n):
        V[i] = S(X0[i, :].reshape(1, 1), Y0[i], w)
    return (1 + np.sum(V <= S(np.array(x).reshape(1, 1), y, w))) / (n + 1)

""
nx = 80
ny = 70
xlist = np.linspace(min(X0), max(X0), nx)
ylist = np.linspace(min(Y0), max(Y0), ny)
R = np.zeros((nx, ny))
for ix in range(nx):
    for iy in range(ny):
        R[ix, iy] = conformal(xlist[ix], ylist[iy])

CS = plt.contour(xlist.flatten(), ylist.flatten(), R.T, levels=np.linspace(0, 1, 11))
plt.plot(xlist.flatten(), hat_y(xlist, hat_w(X0, Y0)), 'k-')
plt.plot(X0, Y0, 'k.', 'MarkerSize', 15)
plt.axis([min(X0), max(X0), min(Y0), max(Y0)]);
plt.show()
