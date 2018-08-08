#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
XC - eXplainable Clustering
Copyright 2018 © Alberto Castellini, Alessandro Farinelli, Francesco Masillo

This file is part of XC.
XC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XC.  If not, see <http://www.gnu.org/licenses/>.

Please, report suggestions/comments/bugs to
 alberto.castellini@univr.it, alessandro.farinelli@univr.it, francesco.masillo@studenti.univr.it
"""
from Tkinter import *

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W, sort=[]):
      Frame.__init__(self, parent)
      self.vars = []
      self.chks = []
      for p in range(0, len(picks)):
         var = IntVar()
         chk = Checkbutton(self, text=picks[sort[p]], variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
         self.chks.append(chk)
   def state(self):
      return map((lambda var: var.get()), self.vars)
