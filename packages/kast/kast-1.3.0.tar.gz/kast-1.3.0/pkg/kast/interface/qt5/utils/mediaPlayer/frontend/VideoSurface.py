#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import List

from PyQt5.QtCore import QPoint, QRect, QSize, Qt, pyqtBoundSignal, pyqtSignal
from PyQt5.QtGui import QImage, QPainter, QPixmap
from PyQt5.QtMultimedia import QAbstractVideoBuffer, QAbstractVideoSurface, QVideoFrame, QVideoSurfaceFormat
from PyQt5.QtWidgets import QWidget

from kast.interface.qt5.utils.mediaPlayer.backend.common.utils.FpsCounter import FpsCounter


class VideoSurface(QAbstractVideoSurface):

    _signalDisplay: pyqtBoundSignal = pyqtSignal(QVideoFrame)

    def __init__(self, surfaceWidget: QWidget) -> None:
        super().__init__(parent=surfaceWidget)

        self._surfaceWidget = surfaceWidget

        self._imageFormat = QImage.Format_Invalid
        self._imageSize = QSize()
        self._sourceRect = QRect()
        self._targetRect = QRect()
        self._currentPixmap = QPixmap()
        self._currentSubtitle: str = ""

        self._fpsCounter = FpsCounter()

        self._signalDisplay.connect(self._display)

        self.activeChanged.connect(self._onActiveChanged)

    @property
    def renderer(self) -> str:
        return self._surfaceWidget.renderer

    @property
    def signalFps(self) -> pyqtBoundSignal:
        return self._fpsCounter.signalFps

    @property
    def fps(self) -> int:
        return self._fpsCounter.fps

    @property
    def videoRect(self):
        return self._targetRect

    def supportedPixelFormats(self, handleType: QAbstractVideoBuffer.HandleType = QAbstractVideoBuffer.NoHandle) -> List[QVideoFrame.PixelFormat]:
        if handleType == QAbstractVideoBuffer.NoHandle:
            return [
                QVideoFrame.Format_RGB24,
                QVideoFrame.Format_RGB32,
                QVideoFrame.Format_ARGB32,
                QVideoFrame.Format_ARGB32_Premultiplied,
                QVideoFrame.Format_RGB565,
                QVideoFrame.Format_RGB555,
            ]

        return []

    def isFormatSupported(self, videoSurfaceFormat: QVideoSurfaceFormat) -> bool:
        imageFormat, imageSize = self._getImageFormatAndSize(videoSurfaceFormat)

        return (
            imageFormat != QImage.Format_Invalid and
            not imageSize.isEmpty() and
            videoSurfaceFormat.handleType() == QAbstractVideoBuffer.NoHandle
        )

    def updateVideoRect(self, repaint: bool = False):
        size = self.surfaceFormat().sizeHint()
        size.scale(size.boundedTo(self._surfaceWidget.size()), Qt.KeepAspectRatio)
        size.scale(size.expandedTo(self._surfaceWidget.size()), Qt.KeepAspectRatio)

        targetRect = QRect(QPoint(0, 0), size)
        targetRect.moveCenter(self._surfaceWidget.rect().center())

        self._targetRect = targetRect

        if repaint:
            self._surfaceWidget.repaint()

    def start(self, videoSurfaceFormat: QVideoSurfaceFormat) -> bool:
        imageFormat, imageSize = self._getImageFormatAndSize(videoSurfaceFormat)

        if imageFormat == QImage.Format_Invalid or imageSize.isEmpty():
            self.setError(QAbstractVideoSurface.UnsupportedFormatError)
            return False

        self._imageFormat = imageFormat
        self._imageSize = imageSize
        self._sourceRect = videoSurfaceFormat.viewport()

        super().start(videoSurfaceFormat)

        self._surfaceWidget.updateGeometry()
        self.updateVideoRect()

        return True

    def stop(self) -> None:
        self._targetRect = QRect()
        self._currentPixmap = QPixmap()
        self._currentSubtitle = ""

        self._fpsCounter.reset()

        super().stop()

        self._surfaceWidget.update()

    def present(self, frame: QVideoFrame) -> bool:
        if not self.isActive():
            return False

        if(
            self.surfaceFormat().pixelFormat() != frame.pixelFormat() or
            self.surfaceFormat().frameSize() != frame.size()
        ):
            self.setError(QAbstractVideoSurface.IncorrectFormatError)
            self.stop()
            return False

        self._signalDisplay.emit(frame)

        return True

    def setSubtitle(self, subtitle: str) -> None:
        self._currentSubtitle = subtitle

    def paint(self, painter: QPainter) -> None:
        oldTransform = painter.transform()

        if self.surfaceFormat().scanLineDirection() == QVideoSurfaceFormat.BottomToTop:
            painter.scale(1, -1)
            painter.translate(0, -self._surfaceWidget.height())

        painter.drawPixmap(self._targetRect, self._currentPixmap, self._sourceRect)
        painter.setTransform(oldTransform)

        if self._currentSubtitle:
            self._paintSubtitle(painter)

        self._fpsCounter.tick()

    def _paintSubtitle(self, painter: QPainter) -> None:
        painter.save()

        fontSize = int(painter.device().height() / 32)

        font = painter.font()
        font.setPointSize(fontSize)
        font.setBold(True)
        painter.setFont(font)

        offset = 3
        flags = Qt.AlignBottom | Qt.AlignHCenter | Qt.TextWordWrap
        painter.setPen(Qt.black)
        painter.drawText(painter.device().rect().adjusted(offset, offset, offset, offset), flags, self._currentSubtitle)
        painter.setPen(Qt.white)
        painter.drawText(painter.device().rect(), flags, self._currentSubtitle)

        painter.restore()

    def _display(self, frame: QVideoFrame) -> None:
        self._currentPixmap = QPixmap.fromImage(frame.image())
        self._surfaceWidget.repaint(self._targetRect)

    def _onActiveChanged(self, active: bool) -> None:
        if active:
            self._surfaceWidget.repaint()

    @staticmethod
    def _getImageFormatAndSize(videoSurfaceFormat: QVideoSurfaceFormat) -> (QImage.Format, QSize):
        return (
            QVideoFrame.imageFormatFromPixelFormat(videoSurfaceFormat.pixelFormat()),
            videoSurfaceFormat.frameSize()
        )
