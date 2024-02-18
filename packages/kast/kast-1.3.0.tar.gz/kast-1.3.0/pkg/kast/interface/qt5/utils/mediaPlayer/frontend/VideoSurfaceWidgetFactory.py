#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Optional, Union

from PyQt5.QtGui import QOpenGLContext
from PyQt5.QtWidgets import QWidget

from kast.interface.qt5.utils.mediaPlayer.frontend.VideoSurfaceWidget import AbstractVideoSurfaceWidget, \
    OpenGlVideoSurfaceWidget, PaintEventHandler, \
    RasterVideoSurfaceWidget


class VideoSurfaceWidgetFactory:

    @classmethod
    def create(
        cls,
        paintEventHandler: PaintEventHandler,
        parent: Optional[QWidget]
    ) -> Union[QWidget, AbstractVideoSurfaceWidget]:
        VideoSurfaceWidget = RasterVideoSurfaceWidget
        if cls._isOpenGl():
            VideoSurfaceWidget = OpenGlVideoSurfaceWidget

        return VideoSurfaceWidget(
            paintEventHandler=paintEventHandler,
            parent=parent
        )

    @staticmethod
    def _isOpenGl() -> bool:
        return QOpenGLContext().create()
