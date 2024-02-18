#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import atexit
import sys
from logging import Handler
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from typing import Dict, List, Union

_DEFAULT_RESPECT_HANDLER_LEVEL: bool = False


class NonBlockingLogHandler(QueueHandler):
    def __init__(
        self,
        *handlers: Handler,
        respect_handler_level: bool = _DEFAULT_RESPECT_HANDLER_LEVEL
    ) -> None:
        super().__init__(Queue())

        self._listener = QueueListener(self.queue, *handlers, respect_handler_level=respect_handler_level)
        self._listener.start()
        atexit.register(self._listener.stop)


class DictCfgNonBlockingLogHandler(NonBlockingLogHandler):
    def __init__(
        self,
        allHandlers: Dict[str, Handler],  # TODO: Remove when support dropped for: Python < 3.12
        handlers: List[Union[str, Handler]],  # TODO: Update to 'List[Handler]' when support dropped for: Python < 3.12
        respect_handler_level: bool = _DEFAULT_RESPECT_HANDLER_LEVEL
    ) -> None:
        if sys.version_info < (3, 12):  # TODO: Remove when support dropped for: Python < 3.12
            handlers = [allHandlers[handlerName] for handlerName in handlers]
        super().__init__(*handlers, respect_handler_level=respect_handler_level)
