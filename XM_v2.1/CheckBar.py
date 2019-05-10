#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
XM - eXplainable Modeling
Copyright 2018 © Alberto Castellini, Alessandro Farinelli, Francesco Masillo

This file is part of XM.
XM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XC.  If not, see <http://www.gnu.org/licenses/>.

Please, report suggestions/comments/bugs to
 alberto.castellini@univr.it, alessandro.farinelli@univr.it, francesco.masillo@studenti.univr.it
"""
from tkinter import *
import tkinter.font

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W, sort=[], selected=[]):
      Frame.__init__(self, parent)
      self.vars = []
      self.chks = []
      fixed = len(picks)-len(sort)
      for p in range(0, len(picks)):
         var = IntVar()
         if p == 0:
             chk = Checkbutton(self, text=picks[0], variable=var)
         if p == 1 and fixed == 2:
             chk = Checkbutton(self, text=picks[1], variable=var)
         else:
             if p > 0:
                 chk = Checkbutton(self, text=picks[sort[p-fixed]+fixed], variable=var)
                 if len(selected) != 0:
                     if selected[p-fixed] == 1:
                         fontS = font.Font(chk, chk.cget("font"))
                         fontS.configure(underline=True, size=10)
                         chk.configure(font=fontS)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
         self.chks.append(chk)
   def state(self):
      return list(map((lambda var: var.get()), self.vars))
