#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import argparse
import os
import sys

from kast.utils.OsInfo import OsInfo, OsName


def _platformTweaks() -> None:
    if OsInfo.name == OsName.Windows:
        # Needed for console-less version [pythonw/PyInstaller]:
        stdnull = open(os.devnull, 'w')
        sys.stdout = sys.stdout if sys.stdout is not None else stdnull
        sys.stderr = sys.stderr if sys.stderr is not None else stdnull

        # Workaround for COM thread configuration interference with PyQt:
        from winrt import _winrt
        _winrt.uninit_apartment()


def main() -> None:
    _platformTweaks()

    from kast.KastApp import KastApp

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="enable debug mode", action="store_true")
    parsedArgs = parser.parse_args()

    app = KastApp(debug=parsedArgs.debug)
    sys.exit(app.run())


if __name__ == "__main__":
    main()
