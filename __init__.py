#-----------------------------------------------------------
# Copyright (C) 2015 Nathan Woodrow
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------
import console
import console.console
import os
import ast

from PyQt4.QtGui import *
from PyQt4.QtCore import *

def resolve(name, basepath=None):
    if not basepath:
      basepath = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(basepath, name)


def classFactory(iface):
    return HyShell(iface)


def displayPrompt(self, more=False):
    self.append("... ") if more else self.append(u"\u03BB=> ")
    self.move_cursor_to_end()


class HyShell:
    def __init__(self, iface):
        self.iface = iface
        self._oldrun = None
        self._olddisplay = None
        self.added = False

    def initGui(self):
        self.action = QAction(QIcon(resolve("icon.png")), "Hy!", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.toggled.connect(self.hymode)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def hymode(self, checked):
        if checked:
            if not console.console._console or not console.console._console.isVisible():
                console.console.show_console()

            if console.console._console and not self.added:
                console.console._console.console.toolBar.addAction(self.action)
                self.added = True

            from hy.cmdline import HyREPL

            if not self._oldrun and not self._olddisplay:
                self._oldrun = console.console_sci.ShellScintilla.runsource
                self._olddisplay = console.console_sci.ShellScintilla.displayPrompt

            self.repl = HyREPL(spy=False)
            console.console_sci.ShellScintilla.runsource = self.repl.runsource
            console.console_sci.ShellScintilla.displayPrompt = displayPrompt
        else:
            console.console_sci.ShellScintilla.runsource = self._oldrun
            console.console_sci.ShellScintilla.displayPrompt = self._olddisplay

        if console.console._console:
            console.console._console.console.shell.setText("")
            console.console._console.console.shell.displayPrompt()
