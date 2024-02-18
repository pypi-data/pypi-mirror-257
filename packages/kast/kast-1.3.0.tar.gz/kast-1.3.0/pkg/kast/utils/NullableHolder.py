#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar

T = TypeVar('T')


class NullableHolder(Generic[T]):

    def __init__(
        self,
        value: Optional[T] = None,
        asValue: bool = False,
        defaultResult: Optional[Any] = None
    ) -> None:
        self._value: Optional[T] = value
        self._asValue: bool = asValue
        self._defaultResult: Optional[Any] = defaultResult if defaultResult else self

    def __call__(self, *args, **kwargs) -> Any:
        return self._defaultResult

    def __getattribute__(self, name: str) -> Any:
        if name.startswith('_') or not self._asValue:
            return super().__getattribute__(name)

        if self._value is None:
            return self._defaultResult

        value = getattr(self._value, name)
        print(f'{name=}, {value=}')
        return getattr(self._value, name)

    @property
    def value(self) -> Optional[T]:
        return self._value

    def isNone(self) -> bool:
        return self._value is None

    def isNotNone(self) -> bool:
        return self._value is not None

    def asValue(self, withDefaultResult: Optional[Any] = None) -> T:
        return NullableHolder(value=self._value, asValue=True, defaultResult=withDefaultResult)
