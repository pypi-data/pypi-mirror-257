#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from kast.Services import Services
from kast.interface.qt5.service.AppLifecycleService import AppLifecycleService
from kast.interface.qt5.service.BackgroundRunner import BackgroundRunner
from kast.interface.qt5.service.InterfaceScheduler import InterfaceScheduler
from kast.interface.qt5.service.MediaControlService import MediaControlService
from kast.interface.qt5.service.ThreadContext import ThreadContext
from kast.interface.qt5.service.UiEventObserver import UiEventObserver
from kast.interface.qt5.service.UiStateService import UiStateService


class UiServices:

    def __init__(self, services: Services) -> None:
        self.services = services
        self.appLifecycleService = AppLifecycleService()
        self.interfaceScheduler = InterfaceScheduler()
        self.backgroundRunner = BackgroundRunner(interfaceScheduler=self.interfaceScheduler)
        self.threadContext = ThreadContext(
            interfaceScheduler=self.interfaceScheduler,
            backgroundRunner=self.backgroundRunner
        )
        self.uiEventObserver = UiEventObserver()
        self.uiStateService = UiStateService(
            threadContext=self.threadContext,
            uiEventObserver=self.uiEventObserver,
            castEventObserver=self.services.castEventObserver
        )
        self.mediaControlService = MediaControlService(
            services=services,
            threadContext=self.threadContext,
            uiStateService=self.uiStateService
        )
