#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import fractions
import time
from typing import Optional, Union

import av
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from PyQt5.QtMultimedia import QAbstractVideoBuffer, QVideoFrame, QVideoSurfaceFormat
from tunit import Milliseconds, Seconds

from kast.interface.qt5.utils.mediaPlayer.backend.pyav.Frame import AudioFrame, Frame, VideoFrame
from kast.interface.qt5.utils.mediaPlayer.backend.common.audio.IAudioService import AudioFormat
from kast.interface.qt5.utils.mediaPlayer.backend.pyav.core.LifecycleMonitor import LifecycleMonitor
from kast.interface.qt5.utils.mediaPlayer.backend.pyav.core.MPConstant import MPConstant
from kast.interface.qt5.utils.mediaPlayer.backend.common.core.MediaDetails import MediaDetails
from kast.interface.qt5.utils.mediaPlayer.backend.pyav.workers.IWorker import IWorker
from kast.utils.FifoBuffer import FifoBuffer
from kast.utils.log.Loggable import Loggable


class BufferingWorker(IWorker, Loggable):

    DEFAULT_FRAME_RATE = 30

    def __init__(
        self,
        mediaDetails: MediaDetails,
        lifecycleMonitor: LifecycleMonitor,
        videoFrameBuffer: FifoBuffer,
        audioFrameBuffer: FifoBuffer
    ) -> None:
        self._mediaDetails = mediaDetails
        self._lifecycleMonitor: LifecycleMonitor = lifecycleMonitor
        self._videoFrameBuffer = videoFrameBuffer
        self._audioFrameBuffer = audioFrameBuffer

    @property
    def name(self) -> str:
        return 'BufferingThread'

    def run(self) -> None:
        try:
            with av.open(str(self._mediaDetails.mediaFilePath)) as container:
                self._mediaDetails.duration = self._avTimeToMs(container.duration / av.time_base)

                self._seek(container=container)

                videoStream = container.streams.video[self._mediaDetails.videoStreamId]
                audioStream = container.streams.audio[self._mediaDetails.audioStreamId]

                frameRate = int(videoStream.guessed_rate)
                self._mediaDetails.fpsReport.mediaFps = frameRate
                self.log.info(f"Video frame rate: {frameRate}")

                frameBufferSize = self._pickFrameBufferSize(frameRate)
                self._videoFrameBuffer.resize(maxsize=frameBufferSize)
                self.log.info(f"Video frame buffer size: {frameBufferSize}")

                videoCodecContext = videoStream.codec_context
                size = QSize(
                    videoCodecContext.width,
                    videoCodecContext.height
                )
                self._mediaDetails.surfaceFormat = QVideoSurfaceFormat(size, QVideoFrame.PixelFormat.Format_RGB24)
                self.log.info(f"Video resolution: {size.width()}x{size.height()}")

                audioCodecContext = audioStream.codec_context
                self._mediaDetails.audioFormat = audioFormat = AudioFormat(
                    sampleRate=audioCodecContext.sample_rate,
                    channelCount=len(audioCodecContext.layout.channels)
                )
                self.log.info(f"Audio sample rate: {audioFormat.sampleRate}")
                self.log.info(f"Audio channel count: {audioFormat.channelCount}")

                for frame in container.decode([videoStream, audioStream]):
                    self._lifecycleMonitor.verifyNotStopped()

                    bufferedFrame = self._createFrame(frame=frame)
                    if bufferedFrame is None:
                        continue

                    frameBuffer = self._videoFrameBuffer if isinstance(bufferedFrame, VideoFrame) else self._audioFrameBuffer
                    while not frameBuffer.tryPut(item=bufferedFrame, timeout=MPConstant.SLEEP_WHILE_WAITING):
                        self._lifecycleMonitor.verifyNotStopped()

                    time.sleep(MPConstant.SLEEP_TO_COOL_DOWN.toRawUnit(unit=Seconds))

        finally:
            self._videoFrameBuffer.close()

    def cleanup(self) -> None:
        pass

    def _seek(self, container: av.container.Container) -> None:
        if self._mediaDetails.startPosition > 0:
            offset = int(float(self._mediaDetails.startPosition.toRawUnit(unit=Seconds)) * av.time_base)
            container.seek(offset)

    def _pickFrameBufferSize(self, frameRate: Optional[int]) -> int:
        return self.DEFAULT_FRAME_RATE if not frameRate or frameRate < self.DEFAULT_FRAME_RATE else frameRate

    def _createFrame(self, frame: av.frame.Frame) -> Frame:
        if isinstance(frame, av.VideoFrame):
            return self._createVideoFrame(frame=frame)
        return self._createAudioFrame(frame=frame)

    def _createVideoFrame(self, frame: av.VideoFrame) -> Optional[Frame]:
        matrix = frame.to_ndarray(format="rgb24")
        qFrame = QVideoFrame(QImage(
            matrix,
            matrix.shape[1],
            matrix.shape[0],
            QImage.Format_RGB888
        ))
        if not qFrame.map(QAbstractVideoBuffer.ReadOnly):
            self.log.error("Couldn't map frame as read only!")
            return None

        return VideoFrame(
            timePos=self._avTimeToMs(frame.time),
            frame=qFrame
        )

    def _createAudioFrame(self, frame: av.AudioFrame) -> Frame:
        return AudioFrame(
            timePos=self._avTimeToMs(frame.time),
            data=frame.to_ndarray().transpose()
        )

    @staticmethod
    def _avTimeToMs(avTime: Union[float, fractions.Fraction]):
        return Milliseconds.fromRawUnit(unit=Seconds, value=float(avTime))
