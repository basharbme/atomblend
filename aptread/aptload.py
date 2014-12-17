# =============================================================================
# (C) Copyright 2014
# Australian Centre for Microscopy & Microanalysis
# The University of Sydney
# =============================================================================
# File:   aptload.py
# Date:   2014-07-01
# Author: Varvara Efremova
#
# Description:
# APT pos/rng loader class
# =============================================================================

from __future__ import print_function

import numpy as np

from . import posload as pl
from . import rngload as rl

# Helper functions
def _unique_rows(a):
    # Returns unique rows in numpy 2D array
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

# Exceptions
class APTReadError(Exception): pass
class InvalidRngError(Exception): pass
class InvalidIndexError(Exception): pass

class ReadAPTData():
    """
    ReadAPTData

    Read in complete pos and range info from input data files
    """

    def __init__(self, pospath, rngpath):
        try:
            self._pos = pl.POS(pospath)
        except pl.ReadError:
            raise APTReadError('Error opening pos file %s' % pospath)
            return
        try:
            self._rng = rl.RNG(rngpath)
        except rl.ReadError:
            raise APTReadError('Error opening rng file %s' % rngpath)
            return

        self.pospath = pospath
        self.rngpath = rngpath

        # Generate atom/range information array
        self.info = self._genarray()
        print("ARRAY", self.info[0:10])

    def __len__(self):
        return len(self._pos.xyz)

    def _genarray(self):
        # Generate array of atom/range info for each pos.xyz point
        d = np.dtype([('rangeid', np.int32), ('atoms', np.object)])
        info = np.zeros(len(self), dtype = d)

        for i, mc in enumerate(self._pos.mc):
            info[i]['atoms'] = self._rng.atoms(mc)
            info[i]['rangeid'] = self._rng.rangeid(mc)

        return info

    @property
    def ions(self):
        return self._rng.ionlist

    @property
    def atoms(self):
        return self._rng.atomlist

    @property
    def ranges(self):
        return self._rng.rnglist

    def getrng(self, rngid):
        """ Returns all xyz points in the selected range reference.

        Arguments:
        rngind -- index of the rng in self.rnglist (int or array_like)
                  value of -1 signifies unranged point

        Returns:
        numpy 2D array of xyz points
        """

        # TODO need to complete getrng function in rngload.py

        return

    def getion(self, ion):
        """ Returns all points that match the selected ion.

        Arguments:
        ionind -- index of the ion in self.ionlist
        """

        xyz = []

        for i, mc in enumerate(self._pos.mc):
            testion = self._rng.getion(mc)
            if testion == ion:
                xyz.append(self._pos.xyz[i])

        return xyz

    def getatom(self, atom):
        """ Returns all points that match the selected atom.

        Arguments:
        atomind -- index of the atom in self.atomlist
        """

        return
