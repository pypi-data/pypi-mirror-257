#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from queue import Empty, Full, Queue
from typing import Generic, Optional, TypeVar

from tunit import Seconds, TimeUnit

T = TypeVar('T')


class ClosedException(Exception):
    pass


class FifoBuffer(Generic[T]):

    def __init__(self, maxsize: int = 0) -> None:
        self._buffer: Queue = Queue(maxsize=maxsize)
        self._isClosed = False

    @property
    def isClosed(self) -> bool:
        return self._isClosed

    @property
    def isFull(self) -> bool:
        return self.isClosed or self._buffer.full()

    def clear(self) -> None:
        with self._buffer.mutex:
            self._buffer.queue.clear()
            self._isClosed = False

    def close(self) -> None:
        self._isClosed = True

    def resize(self, maxsize: int) -> None:
        self._buffer = Queue(maxsize=maxsize)
        self._isClosed = False

    def tryGet(self, timeout: Optional[TimeUnit] = None) -> Optional[T]:
        try:
            return self._buffer.get(block=True, timeout=self._parseOptionalTimeout(timeout))

        except Empty:
            return None

    def tryPut(self, item: T, timeout: Optional[TimeUnit] = None) -> bool:
        if self.isClosed:
            raise ClosedException("Cannot put elements in closed buffer!")

        try:
            self._buffer.put(item=item, block=True, timeout=self._parseOptionalTimeout(timeout))
            return True

        except Full:
            return False

    def _parseOptionalTimeout(self, timeout: Optional[TimeUnit]) -> Optional[float]:
        return timeout.toRawUnit(unit=Seconds) if timeout is not None else None
