#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from pathlib import Path

import av

from kast.media.processing.MetaData import MetaData, StreamInfo, SubtitleStreamInfo, SubtitleStreamType
from kast.media.processing.common import StreamId
from kast.utils.log.Loggable import Loggable


class MediaInfoExtractor(Loggable):

    @classmethod
    def extractMetaData(cls, inputFile: Path) -> MetaData:
        with av.open(str(inputFile)) as f:
            return MetaData(
                title=inputFile.stem,
                videoStreams=[cls._extractStreamInfo(streamId=idx, stream=stream) for idx, stream in enumerate(f.streams.video)],
                audioStreams=[cls._extractStreamInfo(streamId=idx, stream=stream) for idx, stream in enumerate(f.streams.audio)],
                subtitleStreams=[cls._extractSubtitleStreamInfo(streamId=idx, stream=stream, container=f) for idx, stream in enumerate(f.streams.subtitles)]
            )

    @classmethod
    def _extractSubtitleStreamInfo(cls, streamId: StreamId, stream: av.stream.Stream, container: av.container.Container) -> SubtitleStreamInfo:
        streamInfo = cls._extractStreamInfo(streamId=streamId, stream=stream)
        return SubtitleStreamInfo(
            id=streamInfo.id,
            language=streamInfo.language,
            title=streamInfo.title,
            type=cls._extractSubtitleStreamType(stream=stream, container=container)
        )

    @staticmethod
    def _extractStreamInfo(streamId: StreamId, stream: av.stream.Stream) -> StreamInfo:
        return StreamInfo(
            id=streamId,
            language=stream.language,
            title=stream.metadata.get('title')
        )

    @classmethod
    def _extractSubtitleStreamType(cls, stream: av.stream.Stream, container: av.container.Container) -> SubtitleStreamType:
        try:
            for frame in container.decode(stream):
                if not len(frame.rects):
                    continue

                subtitleStreamTypeStr = frame.rects[0].type.decode('ascii')
                return SubtitleStreamType(subtitleStreamTypeStr)

        except ValueError as ex:
            cls.log.exception("Failed to detect subtitle stream type! (Will mark as unknown.) Reason:", ex)

        return SubtitleStreamType.Unknown
