#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from dataclasses import dataclass
from typing import Optional


@dataclass
class FpsReport:
    mediaFps: Optional[int] = None
    backendFps: Optional[int] = None
    frontendFps: Optional[int] = None
