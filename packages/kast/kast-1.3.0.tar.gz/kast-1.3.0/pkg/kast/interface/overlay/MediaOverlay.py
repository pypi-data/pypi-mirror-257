#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Type

from kast.interface.overlay.MediaOverlayBase import MediaOverlayBase
from kast.utils.OsInfo import OsInfo, OsName


def _getImpl() -> Type[MediaOverlayBase]:
    if OsInfo.name == OsName.Linux:
        from ._mpris.MediaOverlayMpris import MediaOverlayMpris
        return MediaOverlayMpris

    if OsInfo.name == OsName.Windows:
        from ._winrt.MediaOverlayWinrt import MediaOverlayWinrt
        return MediaOverlayWinrt

    return MediaOverlayBase


MediaOverlay = _getImpl()
