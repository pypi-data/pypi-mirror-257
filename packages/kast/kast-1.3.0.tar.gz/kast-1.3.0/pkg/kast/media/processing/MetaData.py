#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from kast.media.processing.common import StreamId


class SubtitleStreamType(Enum):
    Unknown = 'unknown'
    Bitmap = 'bitmap'
    Text = 'text'
    Ass = 'ass'


@dataclass(frozen=True)
class StreamInfo:
    id: StreamId
    language: Optional[str] = None
    title: Optional[str] = None


@dataclass(frozen=True)
class SubtitleStreamInfo(StreamInfo):
    type: SubtitleStreamType = SubtitleStreamType.Unknown


@dataclass(frozen=True)
class MetaData:
    title: str = ''
    videoStreams: List[StreamInfo] = field(default_factory=lambda: [])
    audioStreams: List[StreamInfo] = field(default_factory=lambda: [])
    subtitleStreams: List[SubtitleStreamInfo] = field(default_factory=lambda: [])
