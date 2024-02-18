#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import threading
from typing import Optional, Tuple

from mpris_server.server import Server as MprisServer

from kast.Services import Services
from kast.interface.overlay.MediaOverlayBase import MediaOverlayBase
from kast.interface.overlay._mpris.MprisCastController import MprisCastController
from kast.interface.overlay._mpris.MprisEventListener import MprisEventListener
from kast.media.casting.CastState import CastState
from kast.utils.log.Loggable import Loggable


class MediaOverlayMpris(MediaOverlayBase, Loggable):

    def __init__(self, services: Services) -> None:
        super().__init__(services=services)

        self._services: Services = services

        self._mprisCastController = MprisCastController(services=services)

        self._mprisServer: Optional[MprisServer] = None
        self._mprisEventListener: Optional[MprisEventListener] = None

        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        if self._thread is None:
            self._reset(init=True)
            self._thread = threading.Thread(target=self._run, daemon=True, name=self.__class__.__name__)
            self._thread.start()

    def stop(self) -> None:
        if self._thread is not None:
            self._mprisServer._loop.quit()  # TODO: Maybe there will be a better option in the future?
            self._reset()
            self._thread.join()

    def onCastEvent(self, event: CastState) -> None:
        listener = self._mprisEventListener
        if listener is not None:
            listener.reload()

    def _run(self) -> None:
        self.log.info(f"{self.__class__.__name__} started.")
        try:
            self._mprisServer.loop()

        finally:
            self.log.info(f"{self.__class__.__name__} stopped.")

    def _reset(self, init: bool = False) -> None:
        self._mprisServer, self._mprisEventListener = self._getServerAndListener(init=init)

    def _getServerAndListener(self, init: bool) -> Tuple[Optional[MprisServer], Optional[MprisEventListener]]:
        if not init:
            return None, None

        mprisServer = MprisServer(name=self._services.appInfo.appName, adapter=self._mprisCastController)
        mprisServer.publish()
        mprisEventListener = MprisEventListener(mprisServer=mprisServer)
        return mprisServer, mprisEventListener
