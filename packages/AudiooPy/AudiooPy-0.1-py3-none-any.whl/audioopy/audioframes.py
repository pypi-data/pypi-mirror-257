# -*- coding: UTF-8 -*-
"""
:filename: audioframes.py
:authors:  Nicolas Chazeau, Brigitte Bigi
:contact:  contact@sppas.org
:summary:  Manipulate frames of an Audio()

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

"""

import audioop
import struct
import math

from .audioopyexc import SampleWidthError
from .audioopyexc import ChannelIndexError

# ---------------------------------------------------------------------------


class AudioFrames(object):
    """A utility class for audio frames.

    Initially based on audioop (2011-2023), this class is self-implemented
    in 02-2024 due to PEP 594 (dead batteries). Actually, 'audioop' is one
    of the 19 removed libraries with no proposed alternative.

    :Example:
    >>> frames = b'\x01\x00\x02\x00\x03\x00\x04\x00'
    >>> a = AudioFrames(frames, sampwidth=2, nchannels=1)
    >>> a.rms()
    3
    >>> a.minmax()
    (1,5)

    Supported sample width is only either 1 (8bits) or 2 (16bits) or 4 (32bits).
    
    Note that operations such as rms() or mul() make no distinction between
    mono and stereo fragments, i.e. all samples are treated equal. If this is
    a problem the stereo fragment should be split into two mono fragments first
    and recombined later.

    """
    def __init__(self, frames=b"", sampwidth=2, nchannels=1):
        """Create an instance.

        :param frames: (str) input frames
        :param sampwidth: (int) sample width of the frames (1, 2 or 4)
        :param nchannels: (int) number of channels in the samples

        """
        # Check the type and if values are appropriate
        # frames = str(frames)
        sampwidth = int(sampwidth)
        if sampwidth not in [1, 2, 4]:
            raise SampleWidthError(sampwidth)
        nchannels = int(nchannels)
        if nchannels < 1:
            raise ChannelIndexError(nchannels)

        # Set data
        self._frames = frames
        self._sampwidth = sampwidth
        self._nchannels = nchannels

    # -----------------------------------------------------------------------

    def get_frames(self):
        return self._frames

    def get_nchannels(self):
        return self._nchannels

    def get_sampwidth(self):
        return self._sampwidth

    # -----------------------------------------------------------------------

    def get_sample(self, i):
        """Return the value of given sample index.

        :param i: (int) index of the sample to get value
        :return: (int) value

        """
        # Deprecated: return audioop.getsample(self._frames, self._sampwidth, int(i))
        start = i * self._sampwidth
        if self._sampwidth == 2:
            return struct.unpack("<%uh" % 1, self._frames[start:start+2])[0]
        elif self._sampwidth == 1:
            return struct.unpack("%uB" % 1, self._frames[start:start + 1])[0]
        elif self._sampwidth == 4:
            return struct.unpack("<%ul" % 1, self._frames[start:start+4])[0]
        raise SampleWidthError(self._sampwidth)

    # -----------------------------------------------------------------------

    def minmax(self):
        """Return the minimum and maximum values of all samples in the frames.

        :return: (int, int) Min and max amplitude values, or (0,0) if empty frames.

        """
        if len(self._frames) > 0:
            # Deprecated: return audioop.minmax(self._frames, self._sampwidth)
            val_min = self.get_maxval(self._sampwidth)
            val_max = self.get_minval(self._sampwidth)
            for i in range(len(self._frames) // self._sampwidth):
                val = self.get_sample(i)
                if val > val_max:
                    val_max = val
                if val < val_min:
                    val_min = val
            return val_min, val_max
        return 0, 0

    # -----------------------------------------------------------------------

    def min(self):
        """Return the minimum of the values of all samples in the frames."""
        # Deprecated: return audioop.minmax(self._frames, self._sampwidth)[0]
        return self.minmax()[0]

    # -----------------------------------------------------------------------

    def max(self):
        """Return the maximum of the values of all samples in the frames."""
        # Deprecated: return audioop.minmax(self._frames, self._sampwidth)[1]
        return self.minmax()[1]

    # -----------------------------------------------------------------------

    def absmax(self):
        """Return the maximum of the *absolute value* of all samples in the frames."""
        # Deprecated: return audioop.max(self._frames, self._sampwidth)
        val_min, val_max = self.minmax()
        return max(abs(val_min), abs(val_max))

    # -----------------------------------------------------------------------

    def avg(self):
        """Return the average over all samples in the frames.

        :return: (float) Average value rounded to 2 digits.

        """
        # Deprecated: return audioop.avg(self._frames, self._sampwidth)
        if len(self._frames) == 0:
            return 0
        samples_sum = 0.
        nb_samples = len(self._frames) / self._sampwidth
        for i in range(int(nb_samples)):
            samples_sum += self.get_sample(i)

        return round(samples_sum / nb_samples, 2)

    # -----------------------------------------------------------------------

    def rms(self):
        """Return the root-mean-square of the frames.

        :return: (float) sqrt(sum(S_i^2) / n) rounded to 2 digits

        """
        if len(self._frames) == 0:
            return 0.

        # Deprecated: return audioop.rms(self._frames, self._sampwidth)
        square_sum = 0.
        nb_samples = len(self._frames) / self._sampwidth
        for i in range(int(nb_samples)):
            val = self.get_sample(i)
            square_sum += (val*val)

        return round(math.sqrt(square_sum / nb_samples), 2)

    # -----------------------------------------------------------------------

    def resample(self, rate, new_rate=16000):
        """Return re-sampled frames.

        :param rate: (int) The original sample rate of the audio frames
        :param new_rate: (int) The desired sample rate to resample the audio frames to
        :return: (str) The resampled audio frames.

        """
        return audioop.ratecv(self._frames, self._sampwidth, self._nchannels, rate, new_rate, None)[0]

    # -----------------------------------------------------------------------

    def change_sampwidth(self, new_sampwidth):
        """Return frames with the given number of bytes.

        :param new_sampwidth: (int) new sample width of the frames.
            (1 for 8 bits, 2 for 16 bits, 4 for 32 bits)
        :return: (str) converted frames

        """
        if new_sampwidth not in [1, 2, 4]:
            raise SampleWidthError(new_sampwidth)
        return audioop.lin2lin(self._frames, self._sampwidth, new_sampwidth)

    # -----------------------------------------------------------------------

    def bias(self, value):
        """Return frames that is the original fragment with a bias added to each sample.

        Samples wrap around in case of overflow.

        :param value: (int) the bias which will be applied to each sample.
        :return: (str) converted frames

        """
        value = int(value)
        return audioop.bias(self._frames, self._sampwidth, value)

    # -----------------------------------------------------------------------

    def mul(self, factor):
        """Return frames for which all samples are multiplied by factor.

        Samples are truncated in case of overflow.

        :param factor: (float) the factor which will be applied to each sample.
        :return: (str) converted frames

        """
        factor = float(factor)
        return audioop.mul(self._frames, self._sampwidth, factor)

    # -----------------------------------------------------------------------

    def cross(self):
        """Return the number of zero crossings in frames.

        :return: (int) Number of zero crossing or -1 if empty frames

        """
        return audioop.cross(self._frames, self._sampwidth)

    # -----------------------------------------------------------------------

    def clipping_rate(self, factor):
        """Return the clipping rate of the frames.

        :param factor: (float) An interval to be more precise on clipping rate.
        It will consider that all frames outside the interval are clipped.
        Factor has to be between 0 and 1.
        :return: (float) the clipping rate

        """
        if self._sampwidth == 4:
            data = struct.unpack("<%ul" % (len(self._frames) / 4), self._frames)
        elif self._sampwidth == 2:
            data = struct.unpack("<%uh" % (len(self._frames) / 2), self._frames)
        else:
            data = struct.unpack("%uB" % len(self._frames), self._frames)
            data = [s - 128 for s in data]

        max_val = int(AudioFrames.get_maxval(self._sampwidth) * float(factor))
        min_val = int(AudioFrames.get_minval(self._sampwidth) * float(factor))

        nb_clipping = 0
        for d in data:
            if d >= max_val or d <= min_val:
                nb_clipping += 1

        return float(nb_clipping) / len(data)

    # -----------------------------------------------------------------------

    @staticmethod
    def get_maxval(size, signed=True):
        """Return the max value for a given sampwidth.

        :param size: (int) the sampwidth
        :param signed: (bool) if the values will be signed or not
        :return: (int) the max value

        """
        if signed and size == 1:
            return 0x7f
        elif size == 1:
            return 0xff
        elif signed and size == 2:
            return 0x7fff
        elif size == 2:
            return 0xffff
        elif signed and size == 4:
            return 0x7fffffff
        elif size == 4:
            return 0xffffffff

        raise SampleWidthError(size)

    # -----------------------------------------------------------------------

    @staticmethod
    def get_minval(size, signed=True):
        """Return the min value for a given sampwidth.

        :param size: (int) the sampwidth
        :param signed: (bool) if the values will be signed or not
        :return: (int) the min value

        """
        if not signed:
            return 0
        elif size == 1:
            return -0x80
        elif size == 2:
            return -0x8000
        elif size == 4:
            return -0x80000000

        raise SampleWidthError(size)
