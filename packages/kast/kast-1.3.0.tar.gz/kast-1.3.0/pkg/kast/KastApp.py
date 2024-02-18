#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import platform
import signal
import sys
import types

import setproctitle

from kast.Services import Services
from kast.interface.overlay.MediaOverlay import MediaOverlay
from kast.interface.qt5.KastQtApp import KastQtApp
from kast.utils.OsInfo import OsInfo, OsName
from kast.utils.log.LogConfigLoader import LogConfigLoader
from kast.utils.log.Loggable import Loggable


class KastApp(Loggable):

    def __init__(self, debug: bool = False) -> None:
        self._debug = debug
        self._services = Services()
        self._osMediaOverlay = MediaOverlay(services=self._services)
        self._desktopApp = KastQtApp(services=self._services)

    def run(self) -> int:
        setproctitle.setproctitle(self._services.appInfo.appName)

        self._initLogger()
        self._initDebugCapabilities()

        signal.signal(signal.SIGTERM, self._onSignal)
        signal.signal(signal.SIGINT, self._onSignal)

        try:
            self.log.info("Application start!")
            self.log.info(f"Platform name: {platform.platform()}")
            self.log.info(f"Detected OS: {OsInfo.name.value}")
            self.log.info(f"Python: {sys.version}")
            self.log.info(f"Interpreter path: '{sys.executable}'")
            self.log.info(f"Application: {self._services.appInfo.appName} ({self._services.appInfo.appVersion})")
            self.log.info(f"Persistent storage path: '{self._services.persistentStorage.path}'")
            self.log.info(f"Temporary storage path: '{self._services.temporaryStorage.path}'")

            self._services.temporaryStorage.cleanupArtifacts()

            self._services.mediaServer.mediaContent.thumbnailFile = self._services.appInfo.appIconPath
            self._services.mediaServer.start()
            self._osMediaOverlay.start()
            return self._desktopApp.run()

        except Exception as ex:
            self.log.exception(ex)
            return 1

        finally:
            self._onExit()

    def _onSignal(self, signum: int, frame: types.FrameType) -> None:
        self.log.info(f"Caught signal: {signal.Signals(signum).name}")
        self._desktopApp.exit(1)

    def _onExit(self) -> None:
        self._services.castController.quit()
        self._services.mediaServer.stop()
        self._osMediaOverlay.stop()
        self.log.info("Application shutdown!")

    def _initDebugCapabilities(self) -> None:
        if not self._debug:
            return
        if OsInfo.name == OsName.Linux:
            try:
                import namedthreads
                namedthreads.patch()
            except Exception as ex:
                self.log.exception('Exporting thread names to OS failed!', ex)

    def _initLogger(self) -> None:
        logConfigLoader = LogConfigLoader()
        logConfigLoader.loadYml(
            self._services.resourceProvider.getResourcePath('log-config.yml'),
            logFilePath=self._services.persistentStorage.path / f'{self._services.appInfo.package}.log'
        )
        if self._debug:
            logConfigLoader.loadYml(self._services.resourceProvider.getResourcePath('log-config-debug.yml'))
        logConfigLoader.apply()
