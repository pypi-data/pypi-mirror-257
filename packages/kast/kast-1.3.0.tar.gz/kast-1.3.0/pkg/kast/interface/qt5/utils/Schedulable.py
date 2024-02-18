#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Optional

from kast.interface.qt5.service.ThreadContext import ThreadContext


class NonSchedulableException(Exception):
    pass


class ISchedulable(ABC):

    @property
    @abstractmethod
    def threadContext(self) -> ThreadContext:
        """Should return ThreadContext instance for this schedulable."""

    @abstractmethod
    def backgroundExceptionHandler(self, ex: Exception) -> bool:
        """Common background task error handler for this schedulable."""


class Schedulable(ISchedulable):

    _DecoratorProvider = Callable[[ISchedulable], Callable]

    def __init__(self, threadContext: ThreadContext) -> None:
        self.__threadContext: ThreadContext = threadContext

    @property
    def threadContext(self) -> ThreadContext:
        return self.__threadContext

    def backgroundExceptionHandler(self, ex: Exception) -> bool:
        return False

    @classmethod
    def foregroundTask(
        cls,
        funcOpt: Optional[Callable] = None,
        *,
        forceSchedule: bool = False
    ) -> Callable:
        """
        Decorator used to make sure method runs in the interface thread.
        Decorated method's return value will be ignored!
        Works only with ISchedulable derived class methods.
        """
        def decoratorProvider(schedulable: ISchedulable) -> Callable:
            return schedulable.threadContext.foregroundTask(forceSchedule=forceSchedule)

        return cls._taskDecorator(funcOpt=funcOpt, decoratorProvider=decoratorProvider)

    @classmethod
    def backgroundTask(
        cls,
        funcOpt: Optional[Callable] = None,
        *,
        forceSpawnThread: bool = False
    ) -> Callable:
        """
        Decorator used to make sure method runs in a background thread.
        Decorated method's return value will be ignored!
        Works only with ISchedulable derived class methods.
        """
        def decoratorProvider(schedulable: ISchedulable) -> Callable:
            return schedulable.threadContext.backgroundTask(
                forceSpawnThread=forceSpawnThread,
                exceptionHandler=schedulable.backgroundExceptionHandler
            )

        return cls._taskDecorator(funcOpt=funcOpt, decoratorProvider=decoratorProvider)

    @classmethod
    def _taskDecorator(
        cls,
        funcOpt: Optional[Callable],
        *,
        decoratorProvider: _DecoratorProvider
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(obj: Any, *args, **kwargs) -> None:
                cls._verifySchedulable(obj)

                @decoratorProvider(obj)
                def callback() -> None:
                    func(obj, *args, **kwargs)

                callback()

            return wrapper

        return decorator if funcOpt is None \
            else decorator(funcOpt)

    @staticmethod
    def _verifySchedulable(obj: Any) -> None:
        if not isinstance(obj, ISchedulable):
            raise NonSchedulableException("Non-schedulable object cannot use thread context decorators on it's methods!")
