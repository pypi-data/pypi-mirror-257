#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from PyQt5.QtCore import QObject, pyqtBoundSignal, pyqtSignal

from kast.interface.qt5.utils.mediaPlayer.MediaPlayerState import MediaPlayerState


class MediaPlayerSignals(QObject):
    signalOnStateChange: pyqtBoundSignal = pyqtSignal(MediaPlayerState)
    signalOnDurationChange: pyqtBoundSignal = pyqtSignal(int)  # ms
    signalOnPositionChange: pyqtBoundSignal = pyqtSignal(int)  # ms
    signalOnVolumeMutedChange: pyqtBoundSignal = pyqtSignal(bool)
    signalOnVolumeLevelChange: pyqtBoundSignal = pyqtSignal(float)
