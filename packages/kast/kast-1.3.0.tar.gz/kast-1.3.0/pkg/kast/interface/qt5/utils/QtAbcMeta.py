#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABC

from PyQt5.QtCore import QObject


class QtAbcMeta(type(ABC), type(QObject)):
    """
    Allows QObject based classes to inherit ABC based abstract classes. Usage:

    class NewClass(QObject, AbcBasedAbstractClass, metaclass=QtAbcMeta):
        ...
    """
