#!/usr/bin/env python2
# -*- coding: utf-8 -*-
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

import tkinter
import time
from PIL import Image

################################################################################

class Splash:

    def __init__(self, root, file):
        self.__root = root
        self.__file = file
        #self.__wait = wait + time.clock()

    def __enter__(self):
        # Hide the root while it is built.
        #self.__root.withdraw()
        # Create components of splash screen.
        window = tkinter.Toplevel(self.__root)
        canvas = tkinter.Canvas(window)
        splash = tkinter.PhotoImage(master=window, file=self.__file)
        # Get the screen's width and height.
        scrW = window.winfo_screenwidth()
        scrH = window.winfo_screenheight()
        # Get the images's width and height.
        imgW = splash.width()
        imgH = splash.height()
        # Compute positioning for splash screen.
        Xpos = (scrW - imgW) // 2
        Ypos = (scrH - imgH) // 2
        # Configure the window showing the logo.
        window.overrideredirect(True)
        window.geometry('+{}+{}'.format(Xpos, Ypos))
        # Setup canvas on which image is drawn.
        canvas.configure(width=imgW, height=imgH, highlightthickness=0)
        canvas.grid()
        # Show the splash screen on the monitor.
        canvas.create_image(imgW // 2, imgH // 2, image=splash)
        window.update()
        # Save the variables for later cleanup.
        self.__window = window
        self.__canvas = canvas
        self.__splash = splash

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure that required time has passed.
        #now = time.clock()
        #if now < self.__wait:
        #    time.sleep(self.__wait - now)
        # Free used resources in reverse order.
        del self.__splash
        self.__canvas.destroy()
        self.__window.destroy()
        # Give control back to the root program.
        self.__root.update_idletasks()
        self.__root.deiconify()
    
