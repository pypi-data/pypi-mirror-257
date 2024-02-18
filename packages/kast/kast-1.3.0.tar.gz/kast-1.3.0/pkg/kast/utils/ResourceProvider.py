#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from pathlib import Path
from types import ModuleType
from typing import Union


class ResourceProvider:

    def __init__(self, package: ModuleType, assetsDirName: str = 'assets') -> None:
        self.assetsDir = Path(package.__file__).parent / assetsDirName

    def getResourcePath(self, assetRelativePath: Union[Path, str]) -> Path:
        return self.assetsDir / assetRelativePath
