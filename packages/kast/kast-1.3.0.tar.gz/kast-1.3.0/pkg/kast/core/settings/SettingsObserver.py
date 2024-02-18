#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Dict, Set

from .SettingsSubscription import SettingsSubscription


class SettingsObserver:

    Callback = SettingsSubscription.NotifyCallback

    def __init__(self) -> None:
        self._callbacks: Dict[str, Set[SettingsObserver.Callback]] = {}

    def subscribe(self, key: str, callback: Callback) -> SettingsSubscription:
        self._getCallbacks(key=key, init=True).add(callback)
        return SettingsSubscription(key=key, notifyCallback=callback, unsubscribeCallback=self.unsubscribe)

    def unsubscribe(self, key: str, callback: Callback) -> None:
        self._getCallbacks(key=key).remove(callback)

    def notify(self, key: str, value: str) -> None:
        for callback in self._getCallbacks(key=key):
            callback(value)

    def _getCallbacks(self, key: str, init: bool = False) -> Set[Callback]:
        callbacks = self._callbacks.get(key)
        if callbacks is None:
            callbacks = set()

            if init is True:
                self._callbacks[key] = callbacks

        return callbacks
