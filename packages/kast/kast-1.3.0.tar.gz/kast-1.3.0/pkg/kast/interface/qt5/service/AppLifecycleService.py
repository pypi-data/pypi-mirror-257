#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Callable


class AppLifecycleService:

    Callback = Callable[[], None]

    def __init__(self) -> None:
        self._startupCallbacks = set()
        self._shutdownCallbacks = set()

    def subscribeStartup(self, callback: Callback) -> None:
        self._startupCallbacks.add(callback)

    def subscribeShutdown(self, callback: Callback) -> None:
        self._shutdownCallbacks.add(callback)

    def notifyStartup(self) -> None:
        for callback in self._startupCallbacks:
            callback()

    def notifyShutdown(self) -> None:
        for callback in self._shutdownCallbacks:
            callback()
