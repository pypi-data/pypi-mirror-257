#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from kast.Services import Services
from kast.media.casting.CastState import CastState
from kast.utils.log.Loggable import Loggable


class MediaOverlayBase(Loggable):

    def __init__(self, services: Services) -> None:
        services.castEventObserver.register(self, self.onCastEvent)

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def onCastEvent(self, event: CastState) -> None:
        pass
