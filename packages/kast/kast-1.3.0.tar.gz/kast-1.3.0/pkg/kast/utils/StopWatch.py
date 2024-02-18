#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import time
from typing import Optional

from tunit import Milliseconds, Seconds


class StopWatch:

    def __init__(self) -> None:
        self._startStamp: Optional[float] = None
        self._accTime: Milliseconds = Milliseconds()

    @property
    def isRunning(self) -> bool:
        return self._startStamp is not None

    @property
    def isPaused(self) -> bool:
        return self._startStamp is None and self._accTime != 0

    @property
    def isStopped(self) -> bool:
        return self._startStamp is None and self._accTime == 0

    @property
    def elapsed(self) -> Milliseconds:
        return self._accTime + self._calcSegmentElapsed()

    def start(self) -> None:
        if not self.isRunning:
            self._startStamp = time.perf_counter()

    def pause(self) -> None:
        if self.isRunning:
            self._accTime += self._calcSegmentElapsed()
            self._startStamp = None

    def stop(self) -> None:
        self._accTime = Milliseconds()
        self._startStamp = None

    def _calcSegmentElapsed(self) -> Milliseconds:
        value = 0 if not self.isRunning \
            else time.perf_counter() - self._startStamp
        return Milliseconds.fromRawUnit(unit=Seconds, value=value)
