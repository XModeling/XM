#! /usr/bin/env python
#  -*- coding: utf-8 -*-
"""
XM_HeatForecast - eXplainable Modeling for heat forecast
Copyright 2020 © Alberto Castellini, Alessandro Farinelli, Federico Bianchi, Francesco Masillo

This file is part of XM_HeatForecast.
XM_HeatForecast is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XM_HeatForecast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XM_HeatForecast.  If not, see <http://www.gnu.org/licenses/>.

Please, report suggestions/comments/bugs to
 alberto.castellini@univr.it, alessandro.farinelli@univr.it, federico.bianchi@univr.it, francesco.masillo@studenti.univr.it
"""
import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import first_gui
    first_gui.vp_start_gui()




