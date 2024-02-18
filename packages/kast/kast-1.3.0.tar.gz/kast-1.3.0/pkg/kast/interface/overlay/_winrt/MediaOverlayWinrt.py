#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from kast.Services import Services
from kast.interface.overlay.MediaOverlayBase import MediaOverlayBase
from kast.interface.overlay._winrt.WinrtCastController import WinrtCastController
from kast.media.casting.CastState import CastState


class MediaOverlayWinrt(MediaOverlayBase):

    def __init__(self, services: Services) -> None:
        super().__init__(services=services)

        self._winrtCastController = WinrtCastController(services=services)

    def run(self) -> None:
        self._winrtCastController.reload()

    def onCastEvent(self, event: CastState) -> None:
        self._winrtCastController.reload()
