import pyymw16
import numpy as np
from astropy.coordinates import Angle
from astropy.units import Unit


def test_dm_to_dist():
    """ Test that astropy units / angles work with dm_to_dist """
    a = pyymw16.dm_to_dist(204, -6.5, 200)
    b = pyymw16.dm_to_dist(Angle(204, unit='degree'), Angle(-6.5, unit='degree'), 200)
    c = pyymw16.dm_to_dist(204, -6.5, 200 * Unit('pc cm^-3'))
    assert a[0] == b[0] == c[0]
    assert a[1] == b[1] == c[1]

def test_dist_to_dm():
    """ Test that astropy units / angles work with dist_to_dm """
    a = pyymw16.dist_to_dm(204, -6.5, 200)
    b = pyymw16.dist_to_dm(Angle(204, unit='degree'), Angle(-6.5, unit='degree'), 200)
    c = pyymw16.dist_to_dm(204, -6.5, 200 * Unit('pc'))
    assert a[0] == b[0] == c[0]
    assert a[1] == b[1] == c[1]

def test_basic():
    """ Basic tests of YMW16 model

    Note: tested against online YMW16 interface
    http://www.atnf.csiro.au/research/pulsar/ymw16/index.php
    """

    a = pyymw16.calculate_electron_density_xyz(1,2,3)
    assert np.isclose(a, 5.220655, atol=0.0001)

    a = pyymw16.calculate_electron_density_lbr(0,0,4000)
    assert np.isclose(a,  0.388407, atol=0.0001)

    # FRB180301 value
    dm, tau = pyymw16.dist_to_dm(204, -6.5, 25000)
    assert np.isclose(dm.value, 252.0501, atol=0.01)

    # Loop through distances and check round trip
    for dist in (10., 100., 1000.):
        dm, tau = pyymw16.dist_to_dm(0, 0, dist)
        dist_out, tau = pyymw16.dm_to_dist(0, 0, dm.value)
        assert np.isclose(dist_out.value, dist, rtol=0.1)


if __name__ == "__main__":
    test_basic()
    test_dm_to_dist()
    test_dist_to_dm()
