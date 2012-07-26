# Copyright 2011, Vinothan N. Manoharan, Thomas G. Dimiduk, Rebecca
# W. Perry, Jerome Fung, and Ryan McGorty
#
# This file is part of Holopy.
#
# Holopy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Holopy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Holopy.  If not, see <http://www.gnu.org/licenses/>.
"""
Common entry point for holopy io.  Dispatches to the correct load/save
functions.

.. moduleauthor:: Tom Dimiduk <tdimiduk@physics.havard.edu>
"""
import os
import serialize
import image

from ..data import Image
from ..metadata import Optics

def load_image(inf, optics = None, pixel_size = None):
    if isinstance(inf, basestring):
        inf = image._read(inf)
    if isinstance(optics, basestring):
        optics = serialize.load(optics)
        # We allowed optics yamls to be written without an !Optics tag, so for
        # that kind of optics file we get back a dict and have to turn it into
        # an Optics
        if isinstance(optics, dict):
            optics = Optics(**optics)

    return Image(inf, optics = optics, pixel_size = pixel_size)

def load(inf, pixel_size = None, optics = None):
    """
    Load data or results

    Parameters
    ----------
    inf: singe or list of basestring or files
        File to load.  If the file is a yaml file, all other arguments are
        ignored.  If inf is a list of image files or filenames they are all
        loaded as a a timeseries hologram
    optics : :class:`holopy.optics.Optics` object or string (optional)
        Optical train parameters.  If string, specifies the filename
        of an optics yaml
    bg : string (optional)
        name of background file
    bg_type : string (optional)
        set to 'subtract' or 'divide' to specify how background is removed
    channel : int (optional)
        number of channel to load for a color image (in general 0=red,
        1=green, 2=blue) 
    time_scale : float or list (optional)
        time between frames or, if list, time at each frame

    Returns
    -------
    obj: The object loaded, :class:`holopy.hologram.Hologram`, or as loaded from
        yaml

    """

    try:
        return serialize.load(inf)
    except:
        pass

    return image.load(inf, pixel_size = pixel_size, optics = optics)

def save(outf, obj):
    if isinstance(outf, basestring):
        filename, ext = os.path.splitext(outf)
        if ext in ['.tif', '.TIF', '.tiff', '.TIFF']:
            image.save_image(obj, outf)
            return
    serialize.save(outf, obj)

        
        
