#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from pathlib import Path
from typing import List, Optional

from PyQt5.QtWidgets import QComboBox, QFileDialog, QStyle, QWidget

from kast.core.settings.SettingsKeys import SettingsKeys
from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.service.UiEvent import Progress, UiEvent, UiState
from kast.interface.qt5.utils.dialogs import dialogWarning
from kast.interface.qt5.view.VideoSettingsView import Ui_VideoSettingsView
from kast.interface.qt5.viewModel.ViewModelBase import ViewBase, ViewModelBase
from kast.media.processing.MetaData import MetaData, StreamInfo
from kast.media.processing.SubtitlesSourceList import SubtitlesSourceList
from kast.media.processing.Transcoder import TranscodeParams
from kast.utils.log.Loggable import Loggable


class View(ViewBase, QWidget, Ui_VideoSettingsView):
    pass


class VideoSettingsViewModel(ViewModelBase, Loggable):

    def __init__(self, parent: QWidget, uiServices: UiServices) -> None:
        self._view = View(parent=parent)
        super().__init__(uiServices=uiServices, view=self._view)
        self.uiServices.uiEventObserver.register(self, self._onUiEvent)

        self._view.buttonDeviceRefresh.setIcon(self._view.style().standardIcon(QStyle.SP_BrowserReload))
        self._view.buttonVideoOpen.setIcon(self._view.style().standardIcon(QStyle.SP_DirOpenIcon))
        self._view.buttonSubtitlesAdd.setIcon(self._view.style().standardIcon(QStyle.SP_DirOpenIcon))

        self._view.buttonDeviceRefresh.clicked.connect(self._signalDevicesRefresh)
        self._view.buttonVideoOpen.clicked.connect(self._signalVideoOpen)
        self._view.buttonSubtitlesAdd.clicked.connect(self._signalSubtitlesAdd)
        self._view.buttonStream.clicked.connect(self._signalStream)

        self._metaData = MetaData()
        self._subtitlesSourceList = SubtitlesSourceList()
        self._lastTranscodeParams: Optional[TranscodeParams] = None

        self._fillSubtitlesComboBox()

    def _onUiEvent(self, uiEvent: UiEvent) -> None:
        viewEnabled = uiEvent.state == UiState.Idle
        self._view.setEnabled(viewEnabled)

        self._view.setVisible(uiEvent.state != UiState.Streaming)

    def _signalDevicesRefresh(self) -> None:
        self.uiServices.uiStateService.dispatch(UiEvent(state=UiState.DeviceSearch, progress=Progress(complete=False)))

        @self.uiServices.threadContext.foregroundTask
        def onDeviceSearchComplete(deviceNames: List[str]) -> None:
            self._view.comboBoxDevice.clear()
            self._view.comboBoxDevice.addItems(deviceNames)

            if not deviceNames:
                message = "No devices could be found!"
                "\n(Make sure this PC and your cast device are in the same network.)"
                dialogWarning(message=message)

            self.uiServices.uiStateService.dispatch(UiEvent(state=UiState.Idle))

        @self.uiServices.threadContext.backgroundTask
        def searchDevices() -> None:
            devicesList = self.services.castController.searchDevices()
            onDeviceSearchComplete(deviceNames=devicesList)

        searchDevices()

    def _signalVideoOpen(self) -> None:
        filePath = QFileDialog.getOpenFileName(
            self._view,
            "Open Video",
            str(self._getPreviousMediaBrowsePath()),
            "Videos (*.mp4 *.mkv *.webm *.avi)"
        )[0]
        if not filePath:
            return

        self._view.lineEditVideo.setText(filePath)

        def videoOpenedCallback(metaData: MetaData) -> None:
            self._fillAudioComboBox(streams=metaData.audioStreams)
            self._fillSubtitlesComboBox(streams=metaData.subtitleStreams)

        self.uiServices.mediaControlService.openVideo(Path(filePath), videoOpenedCallback)

    def _signalSubtitlesAdd(self) -> None:
        filePath = QFileDialog.getOpenFileName(
            self._view,
            "Open Subtitles",
            str(self._getPreviousMediaBrowsePath()),
            "Subtitles (*.srt *.sub *.ass *.ssa *.txt *.vtt)"
        )[0]
        if not filePath:
            return

        filePath = Path(filePath)

        self.uiServices.mediaControlService.addSubtitles(filePath)

        self._view.comboBoxSubtitles.addItem(filePath.name)
        self._view.comboBoxSubtitles.setCurrentIndex(self._view.comboBoxSubtitles.count() - 1)

    def _signalStream(self) -> None:
        errors = []

        deviceName = self._view.comboBoxDevice.currentText()
        (not deviceName) and errors.append("No cast device has been selected!")

        videoFilePath = str(self._view.lineEditVideo.text())
        (not videoFilePath) and errors.append("No video file has been selected!")

        if errors:
            errors = ["Could not start streaming! Preconditions that failed:"] + errors
            dialogWarning(message='\n - '.join(errors))
            return

        self.uiServices.mediaControlService.startStream(
            deviceName=deviceName,
            audioStreamId=self._getSelectedAudioStreamId(),
            subtitlesId=self._getSelectedSubtitlesId()
        )

    def _getPreviousMediaBrowsePath(self) -> Path:
        return self.services.settingsFacade.get(key=SettingsKeys.BrowseMediaPath)

    def _getSelectedAudioStreamId(self) -> int:
        return self._view.comboBoxAudio.currentIndex()  # TODO: Should we care if it fails (-1)?

    def _getSelectedSubtitlesId(self) -> Optional[int]:
        selectedSubtitles = self._view.comboBoxSubtitles.currentIndex()
        return (selectedSubtitles - 1) if selectedSubtitles > 0 else None

    def _fillDeviceComboBox(self, items: List[str]) -> None:
        self._fillComboBox(self._view.comboBoxDevice, items)

    def _fillAudioComboBox(self, streams: List[StreamInfo]) -> None:
        self._fillComboBox(self._view.comboBoxAudio, self._getStreamNames(streams))

    def _fillSubtitlesComboBox(self, streams: List[StreamInfo] = None) -> None:
        streams = streams if streams else []
        self._fillComboBox(self._view.comboBoxSubtitles, ['No Subtitles'] + self._getStreamNames(streams))

    @staticmethod
    def _getStreamNames(streams: List[StreamInfo]) -> List[str]:
        return [' - '.join(filter(lambda item: item is not None, [f'Stream {index}', stream.language, stream.title])) for index, stream in enumerate(streams)]

    @staticmethod
    def _fillComboBox(comboBox: QComboBox, items: List[str] = None) -> None:
        comboBox.clear()
        items and comboBox.addItems(items)
