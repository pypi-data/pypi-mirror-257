#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Callable, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPaintEvent, QPalette
from PyQt5.QtWidgets import QOpenGLWidget, QSizePolicy, QWidget

PaintEventHandler = Callable[[QPaintEvent], None]

DEFAULT_BACKGROUND_COLOR = Qt.black


class AbstractVideoSurfaceWidget:

    def __init__(
        self,
        renderer: str,
        widget: QWidget,
        paintEventHandler: PaintEventHandler,
        backgroundColor: QColor = DEFAULT_BACKGROUND_COLOR,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self._renderer: str = renderer
        self._widget: QWidget = widget
        self._paintEventHandler: PaintEventHandler = paintEventHandler
        self._backgroundColor = backgroundColor

        self._initUi()

    @property
    def renderer(self) -> str:
        return self._renderer

    @property
    def backgroundBrush(self) -> QBrush:
        return self._widget.palette().color(QPalette.Background)

    def paintEvent(self, event: QPaintEvent) -> None:
        self._paintEventHandler(event)

    def _initUi(self) -> None:
        self._widget.setAttribute(Qt.WA_NoSystemBackground, True)

        palette = self._widget.palette()
        palette.setColor(QPalette.Background, self._backgroundColor)
        self._widget.setPalette(palette)
        self._widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)


class RasterVideoSurfaceWidget(QWidget, AbstractVideoSurfaceWidget):
    def __init__(
        self,
        paintEventHandler: PaintEventHandler,
        backgroundColor: QColor = DEFAULT_BACKGROUND_COLOR,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(
            renderer="Raster",
            widget=self,
            paintEventHandler=paintEventHandler,
            backgroundColor=backgroundColor,
            parent=parent
        )


class OpenGlVideoSurfaceWidget(QOpenGLWidget, AbstractVideoSurfaceWidget):
    def __init__(
        self,
        paintEventHandler: PaintEventHandler,
        backgroundColor: QColor = DEFAULT_BACKGROUND_COLOR,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(
            renderer="OpenGL",
            widget=self,
            paintEventHandler=paintEventHandler,
            backgroundColor=backgroundColor,
            parent=parent
        )
