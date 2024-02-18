#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QWidget

from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.view.SettingsView import Ui_SettingsView
from kast.interface.qt5.viewModel.LocalPlayerBackendSettingsViewModel import LocalPlayerBackendSettingsViewModel
from kast.interface.qt5.viewModel.ViewModelBase import ViewBase, ViewModelBase


class View(ViewBase, QDialog, Ui_SettingsView):
    pass


class SettingsViewModel(ViewModelBase):

    def __init__(self, parent: QWidget, uiServices: UiServices) -> None:
        self._view = View(parent=parent)
        super().__init__(uiServices=uiServices, view=self._view)
        self._view.hide()

        self._previewBackendSection = LocalPlayerBackendSettingsViewModel(parent=self._view, uiServices=uiServices)

        self._view.tabWidget.addTab(self._previewBackendSection.view, "Local Player Backend")

        self._view.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self._onAccepted)
        self._view.accepted.connect(self._onAccepted)

    def _onAccepted(self) -> None:
        self._previewBackendSection.apply()
