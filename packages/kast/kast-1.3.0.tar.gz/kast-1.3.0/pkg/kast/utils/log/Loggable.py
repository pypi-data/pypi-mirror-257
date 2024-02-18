#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import logging


class Loggable:

    class _LoggerProvider:
        def __get__(self, instance, owner) -> logging.Logger:
            logFormat = f"{owner.__name__}:({hex(id(self))})"
            return logging.getLogger(logFormat)

    log = _LoggerProvider()
