#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_server.base import Microseconds

import tunit


def castTimeToMprisTime(value: tunit.Milliseconds) -> Microseconds:
    return int(tunit.Microseconds(value))


def mprisTimeToCastTime(value: Microseconds) -> tunit.Milliseconds:
    return tunit.Milliseconds(tunit.Microseconds(value))
