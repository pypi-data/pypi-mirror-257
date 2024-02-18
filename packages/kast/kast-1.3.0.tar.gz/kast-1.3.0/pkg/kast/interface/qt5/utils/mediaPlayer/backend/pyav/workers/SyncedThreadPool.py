#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from threading import Barrier, BrokenBarrierError, Event, Thread
from typing import Callable, List, Optional

from tunit import Seconds

from kast.interface.qt5.utils.mediaPlayer.backend.pyav.workers.IWorker import IWorker
from kast.interface.qt5.utils.mediaPlayer.backend.pyav.core.MPConstant import MPConstant
from kast.utils.log.Loggable import Loggable

Workers = List[IWorker]
CleanupCallback = Callable[[], None]
Predicate = Callable[[], bool]
ExceptionHandler = Callable[[str, Exception], bool]


class SyncedThreadPool(Loggable):

    def __init__(
        self,
        workers: Workers,
        runWorkersCondition: Predicate,
        cleanupCallback: Optional[CleanupCallback] = None,
        exceptionHandler: Optional[ExceptionHandler] = None,
        shutdownEvent: Optional[Event] = None
    ) -> None:
        self._shutdownEvent = shutdownEvent if shutdownEvent is not None else Event()
        self._workers: Workers = workers
        self._syncBarrier: Barrier = Barrier(parties=len(self._workers), action=self._cleanup)
        self._runWorkersCondition = runWorkersCondition
        self._cleanupCallback = cleanupCallback
        self._exceptionHandler = exceptionHandler

        self._threadPool: List[Thread] = []

    def start(self) -> None:
        if not self._threadPool:
            self._shutdownEvent.clear()
            self._syncBarrier.reset()

            for worker in self._workers:
                self._threadPool.append(Thread(
                    target=self._threadRunner,
                    args=(worker,),
                    name=worker.name,
                    daemon=True
                ))

            for thread in self._threadPool:
                thread.start()

    def stop(self) -> None:
        if self._threadPool:
            self._shutdownEvent.set()
            self._syncBarrier.abort()
            for thread in self._threadPool:
                thread.join()
            self._threadPool = []

    def _cleanup(self) -> None:
        if self._cleanupCallback is not None:
            self._cleanupCallback()

        for worker in self._workers:
            worker.cleanup()

    def _threadRunner(self, worker: IWorker) -> None:
        while not self._shutdownEvent.wait(timeout=MPConstant.SLEEP_WHEN_IDLE.toRawUnit(unit=Seconds)):
            try:
                if self._runWorkersCondition():
                    self._syncBarrier.wait()

                    self._workerLoop(worker=worker)

            except BrokenBarrierError:
                pass

            except Exception as ex:
                if self._exceptionHandler is None or not self._exceptionHandler(worker.__class__.__name__, ex):
                    raise ex

    def _workerLoop(self, worker: IWorker) -> None:
        self.log.info(f"{worker.__class__.__name__} started.")
        try:
            worker.run()

        finally:
            self.log.info(f"{worker.__class__.__name__} stopped.")
