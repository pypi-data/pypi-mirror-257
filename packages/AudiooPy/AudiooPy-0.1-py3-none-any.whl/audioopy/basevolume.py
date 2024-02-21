"""
:filename: audioopy.basevolume.py
:author:  Brigitte Bigi
:contact: contact@sppas.org
:summary: Base class to work with volume values (rms of the samples).

.. _This file is part of AudiooPy:
..
    ---------------------------------------------------------------------

    Copyright (C) 2024 Brigitte Bigi
    Laboratoire Parole et Langage, Aix-en-Provence, France

    Use of this software is governed by the GNU Public License, version 3.

    AudiooPy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    AudiooPy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with AudiooPy. If not, see <https://www.gnu.org/licenses/>.

    This banner notice must not be removed.

    ---------------------------------------------------------------------

The volume is the estimation of RMS values, sampled with a window of 10ms.

"""

import math

# ---------------------------------------------------------------------------


class BaseVolume(object):
    """A base class to estimate the volume.

    """
    def __init__(self, win_len=0.01):
        """Create a BaseVolume instance.

        :param win_len: (float) Size of the window (in seconds)

        """
        self._volumes = list()
        self._rms = 0.
        self._winlen = float(win_len)

    # -----------------------------------------------------------------------

    def get_winlen(self):
        """Return the windows length used to estimate the volume values.
        
        :returns: (float) Duration in seconds.

        """
        return self._winlen

    # -----------------------------------------------------------------------

    def volume(self):
        """Return the global volume value (rms).
        
        :return: (float)

        """
        return self._rms

    # -----------------------------------------------------------------------

    def volume_at(self, index):
        """Return the value of the volume at a given index.
        
        :return: (float)

        """
        return self._volumes[index]

    # -----------------------------------------------------------------------

    def volumes(self):
        """Return the list of volume values (rms).
        
        :return: (list of float)

        """
        return self._volumes

    # -----------------------------------------------------------------------

    def len(self):
        """Return the number of RMS values that were estimated.
        
        :return: (int)

        """
        return len(self._volumes)

    # -----------------------------------------------------------------------

    def min(self):
        """Return the minimum of RMS values.
        
        :return: (float) Return the min rms or 0. if no values.

        """
        if len(self._volumes) == 0:
            return 0.
        return min(self._volumes)

    # -----------------------------------------------------------------------

    def max(self):
        """Return the maximum of RMS values.
        
        :return: (float) Return the max rms or 0. if no values.

        """
        if len(self._volumes) == 0:
            return 0.
        return max(self._volumes)

    # -----------------------------------------------------------------------

    def mean(self):
        """Return the mean of RMS values.
        
        :return: (float) Return the mean rms or 0. if no values.

        """
        if len(self._volumes) == 0:
            return 0.
        return math.fsum(self._volumes) / len(self._volumes)

    # -----------------------------------------------------------------------

    def median(self):
        """Return the median of RMS values.
        
        :return: (float) Return the median rms or 0. if no values.

        """
        if len(self._volumes) == 0:
            return 0.

        middle = len(self._volumes) // 2
        if len(self._volumes) % 2:
            return self._volumes[middle]

        newlist = sorted(self._volumes)
        return float(newlist[middle] + newlist[middle - 1]) / 2.

    # -----------------------------------------------------------------------

    def variance(self):
        """Return the variance of RMS values.
        
        :return: (float) Return the variance or 0. if no values.

        """
        if len(self._volumes) == 0:
            return 0.

        rms_mean = self.mean()
        return math.fsum(pow(i-rms_mean, 2) for i in self._volumes) / (len(self._volumes))

    # -----------------------------------------------------------------------

    def stdev(self):
        """Return the standard deviation of RMS values.
        
        :return: (float) Return the stdev or 0. if no values.

        """
        if len(self._volumes) == 0:
            return 0.
        return math.sqrt(self.variance())

    # -----------------------------------------------------------------------

    def coefvariation(self):
        """Return the coefficient of variation of RMS values.
         
        :return: (float) coefficient of variation given as a percentage.

        """
        percent_mean = self.mean() * 100.
        if round(percent_mean, 2) == 0.:
            return 0.
        return self.stdev() / percent_mean

    # -----------------------------------------------------------------------

    def zscores(self):
        """Return the z-scores of RMS values.

        The z-score determines the relative location of a data value.
        
        :return: (list of float)

        """
        if len(self._volumes) == 0:
            return 0.

        all_scores = [0.] * len(self._volumes)
        mean = self.mean()
        stdev = self.stdev()
        for i, rms_value in enumerate(self._volumes):
            all_scores[i] = (rms_value - mean) / stdev

        return all_scores

    # -----------------------------------------------------------------------

    def stderr(self):
        """Calculate the standard error of the RMS values.

        :return: (float)

        """
        if len(self._volumes) == 0:
            return 0.
        return self.stdev() / float(math.sqrt(len(self._volumes)))

    # -----------------------------------------------------------------------

    def __len__(self):
        return len(self._volumes)

    def __iter__(self):
        for x in self._volumes:
            yield x

    def __getitem__(self, i):
        return self._volumes[i]
