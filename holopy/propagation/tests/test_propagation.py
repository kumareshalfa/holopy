# Copyright 2011-2016, Vinothan N. Manoharan, Thomas G. Dimiduk,
# Rebecca W. Perry, Jerome Fung, Ryan McGorty, Anna Wang, Solomon Barkley
#
# This file is part of HoloPy.
#
# HoloPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HoloPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HoloPy.  If not, see <http://www.gnu.org/licenses/>.


import numpy as np
from ...core import detector_grid
from ...scattering import Mie, Sphere, calc_field
from .. import propagate
from ...core.tests.common import assert_obj_close, verify, get_example_data

def test_propagate_e_field():
    e = calc_field(detector_grid(100,.1), Sphere(1.59, .5, (5, 5, 5)), illum_wavelen=.66, medium_index=1.33, illum_polarization=(1,0), theory=Mie(False))
    prop_e = propagate(e, 10)
    verify(prop_e, 'propagate_e_field')

def test_reconstruction():
    im = get_example_data('image0003')
    rec = propagate(im, 4e-6)
    verify(rec, 'recon_single')

    rec = propagate(im, [4e-6, 7e-6, 10e-6])
    verify(rec, 'recon_multiple')

def test_propagate_0_distance():
    im = get_example_data('image0003')
    rec = propagate(im, 0)
    # propagating no distance should leave the image unchanged
    assert_obj_close(im, rec)

    rec = propagate(im, [0, 3e-6])
    verify(rec, 'recon_multiple_with_0')
