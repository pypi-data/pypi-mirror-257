#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import os
import sys

from PyQt5 import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from kast.Services import Services
from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.viewModel.MainWindowViewModel import MainWindowViewModel
from kast.utils.log.Loggable import Loggable
from kast.utils.OsInfo import OsInfo, OsName


class KastQtApp(Loggable):

    def __init__(self, services: Services) -> None:
        self._setupQt()
        self._app = QApplication(sys.argv)
        self._uiServices = UiServices(services)

        self._app.setWindowIcon(QIcon(str(services.appInfo.appIconPath)))
        self._setupPlatform()

        self._mainWindowViewModel = MainWindowViewModel(uiServices=self._uiServices)

        QTimer.singleShot(0, self._onStartup)
        self._app.aboutToQuit.connect(self._onShutdown)

    def run(self) -> int:
        self.log.info(f"PyQt: {Qt.PYQT_VERSION_STR}, Qt: {Qt.QT_VERSION_STR}")
        return self._app.exec()

    def exit(self, returnCode: int = 0) -> None:
        self._app.closeAllWindows()
        self._app.exit(returnCode)

    def _onStartup(self) -> None:
        self.log.info("User interface startup.")
        self._uiServices.appLifecycleService.notifyStartup()

    def _onShutdown(self) -> None:
        self.log.info("User interface shutdown.")
        self._uiServices.appLifecycleService.notifyShutdown()

    def _setupPlatform(self) -> None:
        """Platform specific setup. Should be run after QApplication creation."""
        if OsInfo.name == OsName.Linux:
            self._app.setDesktopFileName(self._uiServices.services.appInfo.desktopFileName)

    @staticmethod
    def _setupQt() -> None:
        """Qt framework setup. Should be run before QApplication creation."""

        # On windows default backend for media support is 'directshow'.
        # Which does not provide support for proprietary codecs like 'h264'.
        # We could change to 'windowsmediafoundation' backend instead.
        # Unfortunately this setup will only work for Qt>=5.15.5.
        # Workaround for older versions is to install a codec pack.
        if OsInfo.name == OsName.Windows:
            os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'
