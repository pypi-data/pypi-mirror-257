#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from functools import wraps
from typing import Callable, Optional

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

from kast.interface.qt5.service.BackgroundRunner import BackgroundRunner
from kast.interface.qt5.service.InterfaceScheduler import InterfaceScheduler


class ThreadContext:

    ExceptionHandler = Callable[[Exception], bool]

    def __init__(
        self,
        interfaceScheduler: InterfaceScheduler,
        backgroundRunner: BackgroundRunner
    ) -> None:
        self._interfaceScheduler: InterfaceScheduler = interfaceScheduler
        self._backgroundRunner: BackgroundRunner = backgroundRunner

    def foregroundTask(
        self,
        funcOpt: Optional[Callable] = None,
        *,
        forceSchedule: bool = False
    ) -> Callable:
        """
        Decorator used to make sure method runs in the interface thread.
        Decorated method's return value will be ignored!
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                def callback() -> None:
                    func(*args, **kwargs)

                if not forceSchedule and self._isMainThread():
                    callback()
                    return

                self._interfaceScheduler.schedule(callback)

            return wrapper

        return decorator if funcOpt is None \
            else decorator(funcOpt)

    def backgroundTask(
        self,
        funcOpt: Optional[Callable] = None,
        *,
        forceSpawnThread: bool = False,
        exceptionHandler: Optional[ExceptionHandler] = None
    ) -> Callable:
        """
        Decorator used to make sure method runs in a background thread.
        Decorated method's return value will be ignored!
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                def callback() -> None:
                    try:
                        func(*args, **kwargs)

                    except Exception as ex:
                        if exceptionHandler is None or not exceptionHandler(ex):
                            raise ex

                if not forceSpawnThread and not self._isMainThread():
                    callback()
                    return

                self._backgroundRunner.execute(callback)

            return wrapper

        return decorator if funcOpt is None \
            else decorator(funcOpt)

    @staticmethod
    def _isMainThread() -> bool:
        return QThread.currentThread() == QApplication.instance().thread()
