#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional, Union

from pychromecast.controllers.media import MEDIA_PLAYER_STATE_BUFFERING, MEDIA_PLAYER_STATE_IDLE, \
    MEDIA_PLAYER_STATE_PAUSED, \
    MEDIA_PLAYER_STATE_PLAYING, MEDIA_PLAYER_STATE_UNKNOWN, MediaStatus
from pychromecast.controllers.receiver import CastStatus
from pychromecast.socket_client import CONNECTION_STATUS_CONNECTED, CONNECTION_STATUS_CONNECTING, \
    CONNECTION_STATUS_DISCONNECTED, CONNECTION_STATUS_FAILED, CONNECTION_STATUS_FAILED_RESOLVE, CONNECTION_STATUS_LOST, \
    ConnectionStatus
from tunit import Milliseconds, Seconds

DeviceName = str
VolumeLevel = float


def propIgnoreNone(func):
    def wrapper(self, arg):
        if arg is None:
            return

        return func(self, arg)

    return wrapper


class CastConnectionState(Enum):
    Connecting = CONNECTION_STATUS_CONNECTING
    Connected = CONNECTION_STATUS_CONNECTED
    Disconnected = CONNECTION_STATUS_DISCONNECTED
    Failed = CONNECTION_STATUS_FAILED
    FailedResolve = CONNECTION_STATUS_FAILED_RESOLVE
    Lost = CONNECTION_STATUS_LOST


class CastPlayerState(Enum):
    Playing = MEDIA_PLAYER_STATE_PLAYING
    Buffering = MEDIA_PLAYER_STATE_BUFFERING
    Paused = MEDIA_PLAYER_STATE_PAUSED
    Idle = MEDIA_PLAYER_STATE_IDLE
    Unknown = MEDIA_PLAYER_STATE_UNKNOWN


@dataclass
class CastCapabilities:
    canPause: bool = False
    canSeek: bool = False
    canSetMute: bool = False
    canSetVolume: bool = False
    canSkipForward: bool = False
    canSkipBackward: bool = False
    canQueueNext: bool = False
    canQueuePrevious: bool = False


class CastMediaState:
    def __init__(self):
        self._volumeMuted: bool = False
        self._volumeLevel: VolumeLevel = 1.0
        self._playerState: CastPlayerState = CastPlayerState.Unknown
        self._duration: Milliseconds = Milliseconds()
        self._currentTime: Milliseconds = Milliseconds()
        self._title: str = ''
        self._displayName: str = ''
        self._iconUrl: str = ''
        self._imageUrl: str = ''
        self._contentUrl: str = ''
        self._lastPositionUpdateTimestamp: Optional[Milliseconds] = None
        self._playInterruptedTimestamp: Optional[Milliseconds] = None

    @property
    def volumeMuted(self) -> bool:
        return self._volumeMuted

    @volumeMuted.setter
    @propIgnoreNone
    def volumeMuted(self, value: bool) -> None:
        self._volumeMuted = value

    @property
    def volumeLevel(self) -> VolumeLevel:
        return self._volumeLevel

    @volumeLevel.setter
    @propIgnoreNone
    def volumeLevel(self, value: VolumeLevel) -> None:
        self._volumeLevel = value

    @property
    def playerState(self) -> CastPlayerState:
        return self._playerState

    @playerState.setter
    @propIgnoreNone
    def playerState(self, value: CastPlayerState) -> None:
        if self._isPlayerStopping(value):
            self._playInterruptedTimestamp = Milliseconds.fromRawUnit(unit=Seconds, value=time.time())
        elif self._isPlayerResuming(value):
            self._playInterruptedTimestamp = None

        self._playerState = value

    @property
    def duration(self) -> Milliseconds:
        return self._duration

    @duration.setter
    @propIgnoreNone
    def duration(self, value: Milliseconds) -> None:
        self._duration = value

    @property
    def currentTime(self) -> Milliseconds:
        return self._currentTime + (self._getLatestPlayTimestamp() - self._lastPositionUpdateTimestamp) \
            if self._lastPositionUpdateTimestamp is not None else self._currentTime

    @currentTime.setter
    @propIgnoreNone
    def currentTime(self, value: Milliseconds) -> None:
        self._currentTime = value
        self._lastPositionUpdateTimestamp = Milliseconds.fromRawUnit(unit=Seconds, value=time.time())

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    @propIgnoreNone
    def title(self, value: str) -> None:
        self._title = value

    @property
    def displayName(self) -> str:
        return self._displayName

    @displayName.setter
    @propIgnoreNone
    def displayName(self, value: str) -> None:
        self._displayName = value

    @property
    def iconUrl(self) -> str:
        return self._iconUrl

    @iconUrl.setter
    @propIgnoreNone
    def iconUrl(self, value: str) -> None:
        self._iconUrl = value

    @property
    def imageUrl(self) -> str:
        return self._imageUrl

    @imageUrl.setter
    @propIgnoreNone
    def imageUrl(self, value: str) -> None:
        self._imageUrl = value

    @property
    def contentUrl(self) -> str:
        return self._contentUrl

    @contentUrl.setter
    @propIgnoreNone
    def contentUrl(self, value: str) -> None:
        self._contentUrl = value

    def isPlaying(self) -> bool:
        return self.playerState in [CastPlayerState.Playing, CastPlayerState.Buffering]

    def isPaused(self) -> bool:
        return self.playerState == CastPlayerState.Paused

    def isStopped(self) -> bool:
        return not self.isPlaying() and not self.isPaused()

    def _isPlayerStopping(self, newState: CastPlayerState) -> bool:
        return self._playerState == CastPlayerState.Playing and newState != CastPlayerState.Playing

    def _isPlayerResuming(self, newState: CastPlayerState) -> bool:
        return self._playerState != CastPlayerState.Playing and newState == CastPlayerState.Playing

    def _getLatestPlayTimestamp(self) -> Milliseconds:
        return self._playInterruptedTimestamp if self._playInterruptedTimestamp is not None \
            else Milliseconds.fromRawUnit(unit=Seconds, value=time.time())


@dataclass
class CastState:
    connection: CastConnectionState = CastConnectionState.Disconnected
    deviceName: Optional[DeviceName] = None
    capabilities: CastCapabilities = CastCapabilities()
    mediaState: CastMediaState = CastMediaState()

    def isConnected(self) -> bool:
        return self.connection in [
            CastConnectionState.Connected,
            CastConnectionState.Connecting
        ]

    def isConnectedOrRecoverable(self) -> bool:
        return self.isConnected() \
           or self.connection == CastConnectionState.Lost

    def update(
        self,
        mediaStatus: Optional[MediaStatus] = None,
        castStatus: Optional[CastStatus] = None,
        connectionStatus: Optional[ConnectionStatus] = None
    ) -> None:
        if connectionStatus:
            self.connection = CastConnectionState(self._nonNullUpdate(connectionStatus.status, self.connection.value))

        if castStatus:
            self.mediaState.volumeMuted = castStatus.volume_muted
            self.mediaState.volumeLevel = castStatus.volume_level
            self.mediaState.displayName = castStatus.display_name
            self.mediaState.iconUrl = castStatus.icon_url

        if mediaStatus:
            self.capabilities.canPause = self._nonNullUpdate(mediaStatus.supports_pause, self.capabilities.canPause)
            self.capabilities.canSeek = self._nonNullUpdate(mediaStatus.supports_seek, self.capabilities.canSeek)
            self.capabilities.canSetMute = self._nonNullUpdate(mediaStatus.supports_stream_mute, self.capabilities.canSetMute)
            self.capabilities.canSetVolume = self._nonNullUpdate(mediaStatus.supports_stream_volume, self.capabilities.canSetVolume)
            self.capabilities.canSkipForward = self._nonNullUpdate(mediaStatus.supports_skip_forward, self.capabilities.canSkipForward)
            self.capabilities.canSkipBackward = self._nonNullUpdate(mediaStatus.supports_skip_backward, self.capabilities.canSkipBackward)
            self.capabilities.canQueueNext = self._nonNullUpdate(mediaStatus.supports_queue_next, self.capabilities.canQueueNext)
            self.capabilities.canQueuePrevious = self._nonNullUpdate(mediaStatus.supports_queue_prev, self.capabilities.canQueuePrevious)

            self.mediaState.volumeMuted = mediaStatus.volume_muted
            self.mediaState.volumeLevel = mediaStatus.volume_level
            self.mediaState.playerState = self._updateIfNotNull(mediaStatus.player_state, CastPlayerState)
            self.mediaState.duration = self._updateIfNotNull(mediaStatus.duration, self._secToMs)
            self.mediaState.currentTime = self._updateIfNotNull(mediaStatus.adjusted_current_time, self._secToMs)  # TODO: Maybe we should use not adjusted?
            self.mediaState.title = mediaStatus.title
            self.mediaState.imageUrl = mediaStatus.images[0].url if mediaStatus.images else ''
            self.mediaState.contentUrl = mediaStatus.content_id

    @staticmethod
    def _secToMs(value: Union[int, float]) -> Milliseconds:
        return Milliseconds.fromRawUnit(unit=Seconds, value=value)

    @staticmethod
    def _nonNullUpdate(value: Optional[Any], defaultValue: Any) -> Any:
        return defaultValue if value is None else value

    @staticmethod
    def _updateIfNotNull(value: Optional[Any], updateCallback: Callable[[Any], Any]) -> Any:
        return None if value is None else updateCallback(value)
