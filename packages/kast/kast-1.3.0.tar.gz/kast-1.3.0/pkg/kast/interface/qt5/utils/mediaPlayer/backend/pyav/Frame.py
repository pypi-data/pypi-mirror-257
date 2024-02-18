#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from dataclasses import dataclass
from typing import Union

from PyQt5.QtMultimedia import QVideoFrame
from numpy import ndarray
from tunit import Milliseconds


@dataclass
class VideoFrame:
    timePos: Milliseconds
    frame: QVideoFrame


@dataclass
class AudioFrame:
    timePos: Milliseconds
    data: ndarray


Frame = Union[VideoFrame, AudioFrame]
