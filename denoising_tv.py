# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 11:34:27 2015

@author: JonasAdler
"""

# External
import numpy as np

# Internal
import odl


def TVdenoise2D(x, la, mu, iterations=1):
    diff = odl.DiscreteGradient(x.space)

    dimension = diff.range.size

    f = x.copy()

    b = diff.range.zero()
    d = diff.range.zero()
    tmp = diff.domain.zero()

    scale = 1 / diff.domain.grid.cell_volume
    for i in odl.util.ProgressRange("denoising", iterations):
        x = (f * mu + (diff.adjoint(diff(x)) + scale*x + diff.adjoint(d-b)) * la)/(mu+2*la)

        d = diff(x) + b

        for i in range(dimension):
            # tmp = d/abs(d)
            d[i].ufunc.sign(tmp)

            # d = sign(diff(x)+b) * max(|diff(x)+b|-la^-1,0)
            d[i].ufunc.absolute(out=d[i])
            d[i].ufunc.add(-1.0/la, out=d[i])
            d[i].ufunc.maximum(0.0, out=d[i])
            d[i] *= tmp

        b = b + diff(x) - d

        x.show()

n = 100

d = odl.uniform_discr([-1, -1], [1, 1], [n, n])

phantom = odl.util.shepp_logan(d)
phantom.ufunc.add(np.random.rand(n*n)*0.2, out=phantom)
phantom.show()

la = 0.01
mu = 500.0

TVdenoise2D(phantom.copy(), la, mu, 50)
phantom.show()