#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Type

from kast.interface.qt5.viewModel.taskbar.TaskbarViewModelBase import TaskbarViewModelBase
from kast.utils.OsInfo import OsInfo, OsName


def _getImpl() -> Type[TaskbarViewModelBase]:
    if OsInfo.name == OsName.Linux:
        from ._unity.UnityTaskbarViewModel import UnityTaskbarViewModel
        return UnityTaskbarViewModel

    if OsInfo.name == OsName.Windows:
        from ._win32.Win32TaskbarViewModel import Win32TaskbarViewModel
        return Win32TaskbarViewModel

    return TaskbarViewModelBase


TaskbarViewModel = _getImpl()
