#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import time

from PyQt5.QtCore import QObject, QTimer, pyqtBoundSignal, pyqtSignal
from PyQt5.QtWidgets import QStyle, QWidget
from tunit import Milliseconds, Seconds

from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.service.UiEvent import UiEvent, UiState
from kast.interface.qt5.view.MediaControlView import Ui_MediaControlView
from kast.interface.qt5.viewModel.ViewModelBase import ViewBase, ViewModelBase
from kast.media.casting.CastState import CastMediaState, CastPlayerState


class View(ViewBase, QWidget, Ui_MediaControlView):
    pass


class MediaControlViewModel(ViewModelBase):

    class Signals(QObject):
        signalOnVolumeMutedChange: pyqtBoundSignal = pyqtSignal()
        signalOnVolumeLevelChange: pyqtBoundSignal = pyqtSignal(float)

    def __init__(
        self,
        parent: QWidget,
        uiServices: UiServices
    ) -> None:
        self._view = View(parent=parent)
        super().__init__(uiServices=uiServices, view=self._view)
        self.uiServices.uiEventObserver.register(self, self._onUiEvent)

        self._signals = MediaControlViewModel.Signals(parent=self._view)

        self._view.buttonPlayPause.setIcon(self._view.style().standardIcon(QStyle.SP_MediaPlay))
        self._view.buttonStop.setIcon(self._view.style().standardIcon(QStyle.SP_MediaStop))
        self._view.buttonSeekFront.setIcon(self._view.style().standardIcon(QStyle.SP_MediaSeekForward))
        self._view.buttonSeekBack.setIcon(self._view.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self._view.buttonMuteRemote.setIcon(self._view.style().standardIcon(QStyle.SP_MediaVolume))
        self._view.buttonMuteLocal.setIcon(self._view.style().standardIcon(QStyle.SP_MediaVolume))

        self._videoPositionUpdater = QTimer()
        self._videoPositionUpdater.setInterval(int(Milliseconds(Seconds(1))))
        self._videoPositionUpdater.timeout.connect(self._signalVideoPositionUpdate)
        self._videoPositionUpdater.start()

        self._view.buttonDisconnect.clicked.connect(self._signalClickedDisconnect)
        self._view.buttonPlayPause.clicked.connect(self._signalClickedPlayPause)
        self._view.buttonStop.clicked.connect(self._signalClickedStop)
        self._view.buttonSeekFront.clicked.connect(self._signalClickedSeekForward)
        self._view.buttonSeekBack.clicked.connect(self._signalClickedSeekBackward)
        self._view.buttonMuteRemote.clicked.connect(self._signalClickedMuteRemote)
        self._view.buttonMuteLocal.clicked.connect(self._signalClickedMuteLocal)

        self._view.sliderSeek.sliderReleased.connect(self._signalSeekPosition)
        self._view.sliderVolumeRemote.sliderReleased.connect(self._signalSetVolumeRemote)
        self._view.sliderVolumeLocal.sliderReleased.connect(self._signalSetVolumeLocal)

        self._view.setVisible(False)

    @property
    def _mediaState(self) -> CastMediaState:
        return self.uiServices.uiStateService.castState.mediaState

    @property
    def signalOnVolumeMutedChange(self) -> pyqtBoundSignal:
        return self._signals.signalOnVolumeMutedChange

    @property
    def signalOnVolumeLevelChange(self) -> pyqtBoundSignal:
        return self._signals.signalOnVolumeLevelChange

    def setLocalMute(self, muted: bool) -> None:
        iconMuted = QStyle.SP_MediaVolumeMuted if muted else QStyle.SP_MediaVolume
        self._view.buttonMuteLocal.setIcon(self._view.style().standardIcon(iconMuted))

    def setLocalVolume(self, volume: float) -> None:
        self._view.sliderVolumeLocal.setValue(int(100 * volume))

    def _onUiEvent(self, uiEvent: UiEvent) -> None:
        self._view.setVisible(uiEvent.state == UiState.Streaming)

        iconPlayPause = QStyle.SP_MediaPause if self._mediaState.isPlaying() else QStyle.SP_MediaPlay
        self._view.buttonPlayPause.setIcon(self._view.style().standardIcon(iconPlayPause))

        self._updateVideoPosition(position=self._mediaState.currentTime, duration=self._mediaState.duration)

        volumeLevel = int(round(self._mediaState.volumeLevel * 100))
        self._view.sliderVolumeRemote.setSliderPosition(volumeLevel)

        iconMuted = QStyle.SP_MediaVolumeMuted if self._mediaState.volumeMuted or volumeLevel == 0 else QStyle.SP_MediaVolume
        self._view.buttonMuteRemote.setIcon(self._view.style().standardIcon(iconMuted))

    def _updateVideoPosition(self, position: Milliseconds, duration: Milliseconds) -> None:
        def formatTime(value: Milliseconds) -> str:
            return time.strftime('%H:%M:%S', time.gmtime(int(Seconds(value))))

        self._view.labelTime.setText(f"{formatTime(position)} / {formatTime(duration)}")

        if not self._view.sliderSeek.isSliderDown():
            self._view.sliderSeek.setRange(0, int(duration))
            self._view.sliderSeek.setSliderPosition(int(position))

    def _signalVideoPositionUpdate(self) -> None:
        if self._mediaState.playerState == CastPlayerState.Playing:
            self._updateVideoPosition(
                position=self._mediaState.currentTime,
                duration=self._mediaState.duration
            )

    def _signalClickedDisconnect(self) -> None:
        self.services.castController.quit()
        self.services.castController.disconnect()

    def _signalClickedPlayPause(self) -> None:
        self.uiServices.mediaControlService.playOrPause()

    def _signalClickedStop(self) -> None:
        self.uiServices.mediaControlService.stop()

    def _signalClickedSeekForward(self) -> None:
        self.uiServices.mediaControlService.seekForward()

    def _signalClickedSeekBackward(self) -> None:
        self.uiServices.mediaControlService.seekBackward()

    def _signalSeekPosition(self) -> None:
        self.uiServices.mediaControlService.seek(Milliseconds(self._view.sliderSeek.value()))

    def _signalClickedMuteRemote(self) -> None:
        self.uiServices.mediaControlService.setMute(not self._mediaState.volumeMuted)

    def _signalSetVolumeRemote(self) -> None:
        self.uiServices.mediaControlService.setVolume(self._view.sliderVolumeRemote.value()/100)

    def _signalClickedMuteLocal(self) -> None:
        self.signalOnVolumeMutedChange.emit()

    def _signalSetVolumeLocal(self) -> None:
        self.signalOnVolumeLevelChange.emit(self._view.sliderVolumeLocal.value()/100)
