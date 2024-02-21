# -*- coding: UTF-8 -*-
"""
:filename: audioopy.channelvolume.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Estimate and store the RMS values of a channel.

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

import logging

from .audioframes import AudioFrames
from .basevolume import BaseVolume

# ----------------------------------------------------------------------------


class ChannelVolume(BaseVolume):
    """Estimate stats of the volume of an audio channel.

    The volume is the estimation of RMS values, sampled with a window of Xms.

    """

    def __init__(self, channel, win_len=0.01):
        """Constructor.

        :param channel: (Channel) The channel to work on.
        :param win_len: (float) Window length to estimate the volume.

        """
        super(ChannelVolume, self).__init__(win_len)
        self._channel = channel
        self._win_len = win_len

        # Remember current position
        pos = channel.tell()
        # Rewind to the beginning
        channel.rewind()

        # Constants
        nb_frames = int(win_len * channel.get_framerate())
        nb_vols = int(channel.get_duration()/win_len) + 1
        self._volumes = [0.] * nb_vols

        previous_rms = 0.
        for i in range(nb_vols):
            frames = channel.get_frames(nb_frames)
            a = AudioFrames(frames, channel.get_sampwidth(), 1)
            rms = a.rms()
            if rms > 0.:  # provide negative values of corrupted audio files
                self._volumes[i] = rms
            elif rms < 0.:
                self._volumes[i] = previous_rms
                logging.warning("Corrupted audio? The RMS shouldn't be a negative value {}".format(rms))
            previous_rms = rms

        if self._volumes[-1] == 0:
            self._volumes.pop()

        # Returns to the position where we were before
        channel.seek(pos)
        self._rms = channel.rms()

    # -----------------------------------------------------------------------

    def set_volume_value(self, index, value):
        """Set manually the rms at a given position."""
        self._volumes[index] = value

    # -----------------------------------------------------------------------

    def evaluate(self, win_len):
        """Force to re-estimate the global rms value."""

        # Remember current position
        pos = self._channel.tell()

        # Rewind to the beginning
        self._channel.rewind()

        nb_frames = int(win_len * self._channel.get_framerate())
        nb_vols = int(self._channel.get_duration()/win_len) + 1
        previous_rms = 0
        for i in range(nb_vols):
            frames = self._channel.get_frames(nb_frames)
            a = AudioFrames(frames, self._channel.get_sampwidth(), 1)
            rms = a.rms()
            if rms > 0:  # provide negative values of corrupted audio files
                self._volumes[i] = rms
            elif rms < 0:
                self._volumes[i] = previous_rms
                logging.warning("Corrupted audio? The RMS shouldn't be a negative value {:d}".format(rms))
            previous_rms = rms

        if self._volumes[-1] == 0:
            self._volumes.pop()

        # Returns to the position where we was before
        self._channel.seek(pos)

        self._rms = self._channel.rms()
        self._win_len = win_len

    # -----------------------------------------------------------------------

    def __repr__(self):
        return str(self._volumes)
