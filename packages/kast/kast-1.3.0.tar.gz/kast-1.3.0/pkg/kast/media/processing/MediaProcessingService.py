#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import threading
from pathlib import Path
from typing import Optional

from .MediaInfoExtractor import MediaInfoExtractor
from .MetaData import MetaData
from .SubtitleUtils import SubtitleUtils
from .Transcoder import Codecs, Streams, TranscodeParams, Transcoder
from kast.utils.log.Loggable import Loggable


class MediaProcessingService(Loggable):

    DEFAULT_CONTAINER_FORMAT = 'mp4'

    DEFAULT_CODEC_VIDEO = 'h264'
    DEFAULT_CODEC_AUDIO = 'ac3'

    DEFAULT_CODECS = Codecs(
        video=DEFAULT_CODEC_VIDEO,
        audio=DEFAULT_CODEC_AUDIO
    )

    def __init__(self, storageDir: Path) -> None:
        self._storageDir: Path = storageDir

        self._subtitleFile: Path = self._storageDir / 'subtitles.vtt'

    def extractMetaData(self, inputFile: Path) -> MetaData:
        return MediaInfoExtractor.extractMetaData(inputFile=inputFile)

    def extractSubtitles(self, inputFile: Path, streamId: int) -> Path:
        SubtitleUtils.extract(inputFile=inputFile, streamId=streamId, outputFile=self._subtitleFile)
        return self._subtitleFile

    def convertSubtitles(self, inputFile: Path) -> Path:
        SubtitleUtils.convert(inputFile=inputFile, outputFile=self._subtitleFile)
        return self._subtitleFile

    def createTranscoder(
        self,
        inputFile: Path,
        inputStreamIds: Streams,
        outputCodecNames: Optional[Codecs] = None,
        containerFormat: Optional[str] = None,
        progressCallback: Optional[Transcoder.Callback] = None,
        cancelEvent: Optional[threading.Event] = None
    ) -> Transcoder:
        containerFormat = containerFormat if containerFormat else self.DEFAULT_CONTAINER_FORMAT
        outputCodecNames = outputCodecNames if outputCodecNames else self.DEFAULT_CODECS
        return Transcoder(
            params=TranscodeParams(
                inputFile=inputFile,
                inputStreamIds=inputStreamIds,
                outputCodecNames=outputCodecNames
            ),
            outputFile=(self._storageDir / f'movie.{containerFormat}'),
            progressCallback=progressCallback,
            cancelEvent=cancelEvent
        )
