#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional

from tunit import Milliseconds

from kast.Services import Services
from kast.core.settings.SettingsKeys import SettingsKeys
from kast.interface.qt5.service.ThreadContext import ThreadContext
from kast.interface.qt5.service.UiEvent import Progress, UiEvent, UiState
from kast.interface.qt5.service.UiStateService import UiStateService
from kast.interface.qt5.utils.Schedulable import Schedulable
from kast.interface.qt5.utils.dialogs import dialogError, dialogQuestionOkCancel
from kast.media.casting.CastException import CastException
from kast.media.casting.CastState import CastMediaState, CastState, DeviceName
from kast.media.processing.MetaData import MetaData, SubtitleStreamType
from kast.media.processing.SubtitleUtils import SubtitleException
from kast.media.processing.SubtitlesSource import SubtitlesFromFile, SubtitlesFromStream
from kast.media.processing.SubtitlesSourceList import SubtitlesSourceList
from kast.media.processing.Transcoder import Codecs, Streams, TranscodeParams, Transcoder
from kast.media.processing.common import StreamId, containerExtension
from kast.utils.log.Loggable import Loggable


@dataclass
class StreamParams:
    deviceName: DeviceName
    audioStreamId: StreamId
    subtitlesId: Optional[int] = None


class MediaControlService(Loggable, Schedulable):

    VideoOpenedCallback = Callable[[MetaData], None]
    TaskCallback = Callable[[], None]

    _UNSUPPORTED_SUBTITLE_STREAM_TYPES: List[SubtitleStreamType] = [SubtitleStreamType.Bitmap, SubtitleStreamType.Unknown]

    def __init__(
        self,
        services: Services,
        threadContext: ThreadContext,
        uiStateService: UiStateService
    ) -> None:
        super().__init__(threadContext=threadContext)

        self._services = services
        self._threadContext = threadContext
        self._uiStateService = uiStateService

        self._videoFilePath: Optional[Path] = None
        self._metaData = MetaData()
        self._subtitlesSourceList = SubtitlesSourceList()
        self._lastStreamParams: Optional[StreamParams] = None
        self._lastTranscodeParams: Optional[TranscodeParams] = None

    @property
    def _castState(self) -> CastState:
        return self._uiStateService.castState

    @property
    def _mediaState(self) -> CastMediaState:
        return self._castState.mediaState

    def playOrPause(self) -> None:
        if self._mediaState.isPlaying():
            self._services.castController.pause()
        else:
            self._services.castController.play()

    def stop(self) -> None:
        self._services.castController.stop()  # TODO: Make it possible to replay movie!

    def seekForward(self) -> None:
        self._services.castController.seekForward()

    def seekBackward(self) -> None:
        self._services.castController.seekBackward()

    def seek(self, position: Milliseconds) -> None:
        self._services.castController.seek(position)

    def setMute(self, mute: bool = True) -> None:
        self._services.castController.setMute(mute)

    def setVolume(self, value: float) -> None:
        self._services.castController.setVolume(value)

    def openVideo(self, filePath: Path, callback: VideoOpenedCallback) -> None:
        self._videoFilePath = filePath

        self._saveLastMediaDir(filePath)

        self._uiStateService.dispatch(UiEvent(state=UiState.VideoProbe, progress=Progress(complete=False)))

        self._extractMetaData(filePath, callback)

    @Schedulable.backgroundTask
    def _extractMetaData(self, filePath: Path, callback: VideoOpenedCallback) -> None:
        metaData = self._services.mediaProcessingService.extractMetaData(inputFile=filePath)

        self._notifyMetaDataExtracted(metaData, filePath, callback)

    @Schedulable.foregroundTask
    def _notifyMetaDataExtracted(self, metaData: MetaData, filePath: Path, callback: VideoOpenedCallback) -> None:
        filteredSubtitleStreams = [stream for stream in metaData.subtitleStreams if stream.type not in self._UNSUPPORTED_SUBTITLE_STREAM_TYPES]
        self._metaData = metaData = MetaData(
            title=metaData.title,
            videoStreams=metaData.videoStreams,
            audioStreams=metaData.audioStreams,
            subtitleStreams=filteredSubtitleStreams
        )

        self._subtitlesSourceList.clear()
        for streamInfo in metaData.subtitleStreams:
            self._subtitlesSourceList.append(SubtitlesFromStream(
                mediaProcessingService=self._services.mediaProcessingService,
                mediaFile=filePath,
                streamId=streamInfo.id
            ))

        callback(metaData)

        self._uiStateService.dispatch(UiEvent(state=UiState.Idle))

    def addSubtitles(self, filePath: Path) -> None:
        self._saveLastMediaDir(filePath)

        self._subtitlesSourceList.append(SubtitlesFromFile(
            mediaProcessingService=self._services.mediaProcessingService,
            subtitlesFile=filePath
        ))

    def startStream(
        self,
        deviceName: DeviceName,
        audioStreamId: StreamId,
        subtitlesId: Optional[int] = None
    ) -> None:
        if not self._videoFilePath:
            dialogError("No video file has been selected!")
            return

        self._lastStreamParams = StreamParams(deviceName, audioStreamId, subtitlesId)

        self._uiStateService.dispatch(UiEvent(state=UiState.Preprocessing, progress=Progress(complete=False)))

        self._initTranscoding()

    @Schedulable.backgroundTask
    def _initTranscoding(self) -> None:
        cancelEvent = threading.Event()

        def progressCallback(percent: int, complete: bool) -> None:
            self.log.info(f"Transcoding progress: {percent}% ({'Complete' if complete else 'Running'})")
            self._uiStateService.dispatch(UiEvent(state=UiState.AvProcessing, progress=Progress(
                complete=complete, percentage=percent, cancelEvent=cancelEvent
            )))

        castController = self._services.castController

        inputContainer = containerExtension(self._videoFilePath)
        outputContainer = inputContainer if inputContainer in castController.supportedContainerFormats \
            else castController.preferredContainerFormat

        outputCodecNames = Codecs(
            video=castController.preferredVideoCodec,
            audio=castController.preferredAudioCodec
        )

        transcoder = self._services.mediaProcessingService.createTranscoder(
            inputFile=self._videoFilePath,
            inputStreamIds=Streams(video=0, audio=self._lastStreamParams.audioStreamId),
            outputCodecNames=outputCodecNames,
            containerFormat=outputContainer,
            progressCallback=progressCallback,
            cancelEvent=cancelEvent
        )
        self.log.info(
            "Input file: "
            f"container='{inputContainer}', "
            f"codecs={transcoder.inputCodecNames}, "
            f"resolution={transcoder.inputResolution}"
        )
        self.log.info(
            "Output file: "
            f"container='{outputContainer}', "
            f"codecs={transcoder.outputCodecNames}, "
            f"resolution={transcoder.outputResolution}"
        )
        if transcoder.requireProcessing and self._lastTranscodeParams != transcoder.params:
            self._confirmTranscoding(transcoder)
            return

        self._startStreaming(transcoder.outputFile)

    @Schedulable.foregroundTask
    def _confirmTranscoding(self, transcoder: Transcoder) -> None:
        message = "Selected media is not supported in it's current form. " \
            "Either because of a codec mismatch, too high resolution or not supported media container type. " \
            "Your file can be remuxed and transcoded to address those issues.\n" \
            "\n" \
            "Remuxing is a quick process. While duration of transcoding varies. " \
            "It is usually fast for audio codecs and can take some time for video codecs. " \
            "Actual times will depend on your machine processing power.\n" \
            "\n" \
            "Provided Container -> Supported Container:\n" \
            f"- {containerExtension(transcoder.inputFile)} -> {containerExtension(transcoder.outputFile)}\n" \
            "\n" \
            "Provided Codecs -> Supported Codecs:\n" \
            f"- Video: '{transcoder.inputCodecNames.video}' -> '{transcoder.outputCodecNames.video}'\n" \
            f"- Audio: '{transcoder.inputCodecNames.audio}' -> '{transcoder.outputCodecNames.audio}'\n" \
            "\n" \
            f"Provided resolution / Max supported resolution:\n" \
            f"- '{transcoder.inputResolution}' / '{transcoder.maxResolution}'\n" \
            "\n" \
            "Proceed with media processing?\n" \
            "(Your original file will not be modified.)\n"

        if not dialogQuestionOkCancel(title="Media Processing", message=message):
            self._cancelAction()
            return

        self._startTranscoding(transcoder)

    @Schedulable.backgroundTask
    def _startTranscoding(self, transcoder: Transcoder) -> None:
        if not transcoder.run():
            self._cancelAction()
            return

        self._lastTranscodeParams = transcoder.params

        self._confirmStreaming(transcoder.outputFile)

    @Schedulable.foregroundTask
    def _confirmStreaming(self, videoFile: Path) -> None:
        message = "Media processing finished!\n\nProceed with streaming?\n"

        if not dialogQuestionOkCancel(title="Streaming", message=message):
            self._cancelAction()
            return

        self._startStreaming(videoFile)

    @Schedulable.backgroundTask
    def _startStreaming(self, videoFile: Path) -> None:
        mediaContent = self._services.mediaServer.mediaContent
        mediaContent.movieFile = videoFile
        mediaContent.subtitlesFile = self._getSubtitlesFilePath()

        self._uiStateService.dispatch(UiEvent(state=UiState.Connecting, progress=Progress(complete=False)))

        self._services.castController.connect(name=self._lastStreamParams.deviceName)
        self._services.castController.stream(
            movieUrl=self._services.mediaServer.movieUrl,
            subtitlesUrl=self._services.mediaServer.subtitleUrl,
            thumbnailUrl=self._services.mediaServer.thumbnailUrl,
            title=self._metaData.title
        )

        self._uiStateService.dispatch(UiEvent(state=UiState.Streaming))

    def _getSubtitlesFilePath(self) -> Optional[Path]:
        subtitlesId = self._lastStreamParams.subtitlesId
        return self._subtitlesSourceList[subtitlesId].toVtt() if subtitlesId is not None else None

    def _cancelAction(self) -> None:
        self._uiStateService.dispatch(UiEvent(state=UiState.Idle))

    def _saveLastMediaDir(self, filePath) -> None:
        self._services.settingsFacade.set(key=SettingsKeys.BrowseMediaPath, value=str(filePath.parent))

    @Schedulable.foregroundTask
    def _reportError(self, message) -> None:
        dialogError(message=message)
        self._uiStateService.dispatch(UiEvent(state=UiState.Idle))

    def backgroundExceptionHandler(self, ex: Exception) -> bool:
        if not isinstance(ex, (SubtitleException, CastException)):
            return False

        self.log.exception(ex)
        self._reportError(str(ex))
        return True
