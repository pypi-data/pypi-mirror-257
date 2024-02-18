#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from __future__ import annotations

from typing import TypeVar, Generic, Optional, Callable, Any, Union

T = TypeVar('T')
R = TypeVar('R')


Mapper = Callable[[T], R]
Predicate = Callable[[T], bool]
Consumer = Callable[[T], None]
Supplier = Callable[[], T]
Runnable = Callable[[], None]


class FakePropertyAssigner:
    def __getattr__(self, name: str) -> FakePropertyAssigner:
        return self

    def __set__(self, instance: Any, value: Any) -> None:
        pass


class Maybe(Generic[T]):

    def __init__(self, value: Optional[T] = None) -> None:
        self._value: Optional[T] = value

    @property
    def value(self) -> Optional[T]:
        return self._value

    def asPropertyAssigner(self) -> Union[T, FakePropertyAssigner]:
        return self._value if self._value is not None\
            else FakePropertyAssigner()

    def isEmpty(self) -> bool:
        return self._value is None

    def isPresent(self) -> bool:
        return not self.isEmpty()

    def ifEmpty(self, runnable: Runnable) -> None:
        if self.isEmpty():
            runnable()

    def ifPresent(self, consumer: Consumer[T]) -> None:
        if self.isPresent():
            consumer(self._value)

    def ifPresentOrEmpty(self, onPresent: Consumer[T], onEmpty: Runnable) -> None:
        if self.isPresent():
            onPresent(self._value)
        else:
            onEmpty()

    def orElse(self, default: T) -> T:
        return self._value if self.isPresent() else default

    def orThrow(self, supplier: Supplier[Exception]) -> T:
        if self.isEmpty():
            raise supplier()
        return self._value

    def map(self, mapper: Mapper[T, R]) -> Maybe[R]:
        return self if self.isEmpty()\
            else Maybe[R](mapper(self._value))

    def flatMap(self, mapper: Mapper[T, Maybe[R]]) -> Maybe[R]:
        return self if self.isEmpty()\
            else mapper(self._value)

    def filter(self, predicate: Predicate[T]) -> Maybe[T]:
        return self if self.isEmpty()\
            or predicate(self._value)\
                else Maybe[T]()
