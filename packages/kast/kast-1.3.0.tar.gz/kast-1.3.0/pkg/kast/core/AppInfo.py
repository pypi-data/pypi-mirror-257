#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from pathlib import Path

from kast import __app_name__, __author__, __email__, __package_name__, __version__
from kast.utils.ResourceProvider import ResourceProvider


class AppInfo:

    def __init__(self, resourceProvider: ResourceProvider) -> None:
        self._resourceProvider = resourceProvider

    @property
    def author(self) -> str:
        return __author__

    @property
    def email(self) -> str:
        return __email__

    @property
    def package(self) -> str:
        return __package_name__

    @property
    def appName(self) -> str:
        return __app_name__

    @property
    def appVersion(self) -> str:
        return __version__

    @property
    def desktopFileName(self) -> str:
        return f'{__package_name__}.desktop'

    @property
    def appIconPath(self) -> Path:
        return self._resourceProvider.getResourcePath('appicon.png')
