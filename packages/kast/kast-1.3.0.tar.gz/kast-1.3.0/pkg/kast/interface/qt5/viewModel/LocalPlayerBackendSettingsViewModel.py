#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Dict, List

from PyQt5.QtWidgets import QRadioButton, QWidget

from kast.core.settings.SettingsKeys import SettingsKeys
from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.utils.mediaPlayer.MediaPlayerFactory import MediaPlayerBackend, MediaPlayerFactory
from kast.interface.qt5.view.LocalPlayerBackendSettingsView import Ui_LocalPlayerBackendSettingsView
from kast.interface.qt5.viewModel.ViewModelBase import ViewBase, ViewModelBase
from kast.utils.OsInfo import OsInfo, OsName


def _stripDescription(text: str) -> str:
    return '\n'.join([line.strip() for line in text.strip().split('\n')]).strip()


class View(ViewBase, QWidget, Ui_LocalPlayerBackendSettingsView):
    pass


class LocalPlayerBackendSettingsViewModel(ViewModelBase):

    _BACKEND_DESCRIPTIONS: Dict[MediaPlayerBackend, str] = {
        MediaPlayerBackend.Null: _stripDescription('''
            Mock implementation of a media player:
            -> Available on all platforms.
            -> Disables local player.
        '''),
        MediaPlayerBackend.Qt: _stripDescription('''
            Qt implementation of a media player:
            -> Available on all platforms.
            -> Planned to be phased out.
            -> On Linux based on gstreamer.
            -> On Windows based either on DirectShow or Windows Media Foundation.
        '''),
        MediaPlayerBackend.PyAV: _stripDescription('''
            Media player engine built with PyAV:
            -> Default on Linux.
            -> Available only on Linux.
            -> Still experimental.
        '''),
        MediaPlayerBackend.WinRt: _stripDescription('''
            Media player engine built with WinRT:
            -> Default on Windows.
            -> Available only on Windows.
            -> Still experimental.
        '''),
    }

    def __init__(self, parent: QWidget, uiServices: UiServices) -> None:
        self._view = View(parent=parent)
        super().__init__(uiServices=uiServices, view=self._view)

        self._selectedBackend: MediaPlayerBackend = MediaPlayerBackend(self.services.settingsFacade.get(SettingsKeys.MediaPreviewBackendEngine))

        self._setDescription()
        for backend in MediaPlayerFactory.getSupportedBackends():
            radioButton = QRadioButton(backend.name, self._view.groupBox)
            radioButton.toggled.connect(lambda checked, backend=backend: self._onBackendSelected(checked, backend))
            self._view.layoutRadioButtons.addWidget(radioButton)
            if backend == self._selectedBackend:
                radioButton.setChecked(True)

    def apply(self) -> None:
        self.services.settingsFacade.set(SettingsKeys.MediaPreviewBackendEngine, self._selectedBackend.value)

    def _onBackendSelected(self, checked: bool, backend: MediaPlayerBackend) -> None:
        if checked:
            self._selectedBackend = backend
            self._setDescription()

    def _setDescription(self) -> None:
        self._view.textEditDescription.setPlainText(self._BACKEND_DESCRIPTIONS[self._selectedBackend])
