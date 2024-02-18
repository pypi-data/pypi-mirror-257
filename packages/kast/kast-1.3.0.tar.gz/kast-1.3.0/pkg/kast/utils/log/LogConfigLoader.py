#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import logging.config
from pathlib import Path
from typing import Dict

import yaml

from kast.utils.DeepUpdateableDict import DeepUpdateableDict


class LogConfigLoader:

    ReplaceMap = Dict[str, str]

    def __init__(self) -> None:
        self._config: DeepUpdateableDict = DeepUpdateableDict()

    def apply(self) -> None:
        logging.config.dictConfig(self._config)

    def loadYml(self, filePath: Path, **kwargs: ReplaceMap) -> None:
        ymlStr = self._readFile(filePath)\
            .format(**kwargs)
        config = yaml.safe_load(ymlStr)
        self._config.deepUpdate(config)

    @staticmethod
    def _readFile(filePath: Path) -> str:
        with open(filePath) as f:
            return f.read()
