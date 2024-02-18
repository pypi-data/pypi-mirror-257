#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Optional, Union

from PyQt5.QtWidgets import QWidget

from kast.Services import Services
from kast.interface.qt5.UiServices import UiServices


class ViewBase:
    def __init__(self, parent: Optional[QWidget]) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)
        self.show()


class ViewModelBase:

    View = Union[ViewBase, QWidget]

    def __init__(self, uiServices: UiServices, view: View) -> None:
        self._uiServices = uiServices
        self.__view = view

        self._uiServices.appLifecycleService.subscribeStartup(self._onStartup)
        self._uiServices.appLifecycleService.subscribeShutdown(self._onShutdown)

    @property
    def services(self) -> Services:
        return self._uiServices.services

    @property
    def uiServices(self) -> UiServices:
        return self._uiServices

    @property
    def view(self) -> View:
        return self.__view

    def _onStartup(self) -> None:
        pass

    def _onShutdown(self) -> None:
        pass
