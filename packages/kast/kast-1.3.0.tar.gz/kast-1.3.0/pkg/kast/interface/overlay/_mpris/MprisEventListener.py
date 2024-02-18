#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_server.events import EventAdapter
from mpris_server.server import Server as MprisServer


class MprisEventListener(EventAdapter):

    def __init__(self, mprisServer: MprisServer) -> None:
        super().__init__(
            player=mprisServer.player,
            root=mprisServer.root
        )

    def reload(self) -> None:
        self.on_volume()
        self.on_playback()
        self.on_title()
        self.on_options()
        self.on_playpause()
