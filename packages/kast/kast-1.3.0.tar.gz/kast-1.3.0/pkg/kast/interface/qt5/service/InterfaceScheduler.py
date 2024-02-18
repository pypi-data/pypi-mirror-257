#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Callable
from queue import Empty, Full, Queue
from typing import Optional

from PyQt5.QtCore import QTimer
from tunit import Milliseconds, Seconds

from kast.utils.log.Loggable import Loggable


class InterfaceScheduler(Loggable):

    Callback = Callable[[], None]

    EVENT_INTERVAL = Milliseconds(500)
    QUEUE_TIMEOUT = Milliseconds(10)

    def __init__(self) -> None:
        self._queue = Queue()
        self._timer = QTimer()
        self._timer.setInterval(int(self.EVENT_INTERVAL))
        self._timer.timeout.connect(self._process)
        self._timer.start()

    def schedule(self, callback: Callback) -> None:
        try:
            self._queue.put(item=callback, block=True, timeout=self.QUEUE_TIMEOUT.toRawUnit(unit=Seconds))
        except Full:
            raise RuntimeError(f"Could not schedule interface task! Queue size: {self._queue.qsize()}")

    def _process(self) -> None:
        callback = self._tryPopTask()
        if callback:
            callback()
            self._queue.task_done()

    def _tryPopTask(self) -> Optional[Callback]:
        try:
            return self._queue.get(block=True, timeout=self.QUEUE_TIMEOUT.toRawUnit(unit=Seconds))
        except Empty:
            return None
