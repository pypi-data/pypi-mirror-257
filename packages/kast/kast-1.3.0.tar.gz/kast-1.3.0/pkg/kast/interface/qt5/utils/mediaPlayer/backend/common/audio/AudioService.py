#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import math
import time
from threading import Event, Thread
from typing import Optional

import numpy
import soundcard
from numpy import ndarray
from tunit import Milliseconds, Nanoseconds, Seconds

from kast.interface.qt5.utils.mediaPlayer.backend.common.audio.IAudioService import AudioFormat, IAudioService
from kast.utils.FifoBuffer import FifoBuffer
from kast.utils.OsInfo import OsInfo, OsName
from kast.utils.log.Loggable import Loggable


class AudioService(IAudioService, Loggable):

    PlayerCore = 'soundcard.Player'

    _IDLE_DELAY: Milliseconds = Milliseconds(20)
    _COOLDOWN_DELAY: Nanoseconds = Nanoseconds(1)
    _DEFAULT_SHOULD_PLAY: bool = False
    _DEFAULT_LATENCY: float = 0.0

    def __init__(
        self,
        appName: str = 'Python'
    ) -> None:
        self._frameBuffer: FifoBuffer[ndarray] = FifoBuffer()
        self._audioFormat: Optional[AudioFormat] = None
        self._thread: Optional[Thread] = None

        self._shutdownEvent: Event = Event()
        self._audioFormatChangeEvent: Event = Event()

        self._shouldPlay: bool = self._DEFAULT_SHOULD_PLAY

        self._latency: float = self._DEFAULT_LATENCY
        self._volumeLevel: float = 1.0
        self._volumeMuted: bool = False

        if OsInfo.name == OsName.Linux:
            soundcard.set_name(appName)

    @property
    def latency(self) -> Milliseconds:
        return Milliseconds.fromRawUnit(unit=Seconds, value=self._latency)

    def isVolumeMuted(self) -> bool:
        return self._volumeMuted

    def setVolumeMuted(self, value: bool) -> None:
        self._volumeMuted = value

    def getVolumeLevel(self) -> float:
        return self._volumeLevel

    def setVolumeLevel(self, value: float) -> None:
        self._volumeLevel = value

    def setAudioFormat(self, audioFormat: AudioFormat) -> None:
        if audioFormat != self._audioFormat:
            self._reset(audioFormat=audioFormat)
            self._audioFormatChangeEvent.set()

    def init(self) -> None:
        if self._thread is None:
            self._thread = Thread(
                target=self._run,
                name=self.__class__.__name__,
                daemon=True
            )
            self._thread.start()

    def shutdown(self) -> None:
        if self._thread is not None:
            self._shutdownEvent.set()
            self._thread.join()
            self._thread = None

            self._reset()

    def play(self) -> None:
        self._shouldPlay = True

    def stop(self) -> None:
        self._shouldPlay = False

    def enqueueFrame(self, data: ndarray) -> None:
        self._frameBuffer.tryPut(item=data)

    def _adjustVolume(self, frame: ndarray) -> ndarray:
        if self._volumeMuted:
            return numpy.zeros(frame.shape)

        multiplier = math.pow(2, (math.sqrt(math.sqrt(math.sqrt(self._volumeLevel))) * 192 - 192)/6)
        return numpy.multiply(frame, multiplier, casting="unsafe")

    def _reset(self, audioFormat: Optional[AudioFormat] = None) -> None:
        self._audioFormat = audioFormat
        self._frameBuffer.clear()
        self._shouldPlay = self._DEFAULT_SHOULD_PLAY

    def _playerLoop(self, player: PlayerCore) -> None:
        try:
            while(
                    not self._shutdownEvent.is_set()
                    and not self._audioFormatChangeEvent.is_set()
            ):
                time.sleep(self._COOLDOWN_DELAY.toRawUnit(unit=Seconds))

                self._latency = player.latency

                if not self._shouldPlay:
                    time.sleep(self._IDLE_DELAY.toRawUnit(unit=Seconds))
                    continue

                frame = self._frameBuffer.tryGet(timeout=self._COOLDOWN_DELAY)
                if frame is not None:
                    player.play(self._adjustVolume(frame))

        finally:
            self._latency = self._DEFAULT_LATENCY
            self._audioFormatChangeEvent.clear()

    def _run(self) -> None:
        self.log.info(f"{self.__class__.__name__} started.")
        try:
            while not self._shutdownEvent.is_set():
                try:
                    time.sleep(self._COOLDOWN_DELAY.toRawUnit(unit=Seconds))

                    if self._audioFormat is None:
                        time.sleep(self._IDLE_DELAY.toRawUnit(unit=Seconds))
                        continue

                    with soundcard.default_speaker().player(
                        samplerate=self._audioFormat.sampleRate,
                        channels=self._audioFormat.channelCount,
                        # exclusive_mode=True  # Windows only - might fix audio
                    ) as player:
                        self._playerLoop(player=player)

                except Exception as ex:
                    self.log.exception(ex)
                    self._audioFormat = None

        finally:
            self._audioFormatChangeEvent.clear()
            self._shutdownEvent.clear()
            self.log.info(f"{self.__class__.__name__} stopped.")
