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
along with XM.  If not, see <http://www.gnu.org/licenses/>.

Please, report suggestions/comments/bugs to
 alberto.castellini@univr.it, alessandro.farinelli@univr.it, francesco.masillo@studenti.univr.it
"""
#import pyximport; pyximport.install(reload_support=True)
from XM_clustering_results import XM_clustering_results
from XM_only_data import XM_only_data
import sys
from tkinter.ttk import Style
import locale
import pandas as pd
import numpy as np
#from tkinter import *
from tkinter import Tk, Frame, Menu, X, Y, TOP, BOTTOM, RIGHT, LEFT, BOTH, Listbox, Radiobutton, Button, OptionMenu, Label, Text, Canvas, Toplevel, StringVar, INSERT, END, VERTICAL
import tkinter.ttk as ttk
#import tkinter
from tkinter import filedialog
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import platform
#if platform.system() == 'Linux':
#    import GUI_generation as gid
from MethodLib.pandastable_master.pandastable import Table
from tkinter import messagebox
from CheckBar import Checkbar
from LoadingScreen import Splash
from VSF import VerticalScrolledFrame
#import os
from pathlib import Path
import matplotlib.pylab as pl
import matplotlib.patches as mpatches
matplotlib.use('TkAgg')

from MarkerUpdater import MarkerUpdater as mu
zoomer = mu()

import mplcursors
import math
import itertools

#import matplotlib.pyplot as plt
#from HSF import HorizontalScrolledFrame as HSF


global pathD
global pathS
global pathGT
global gt
global var


def handler():
    if (varD.get()=="Dataset") and (varG.get()=="Time Series"):
        draw_graph(window, window.pack_slaves(), False, varExp.get())
        return 
    if (varD.get()=="Dataset") and (varG.get()=="2D/3D Scatters"):
        scatters_2d3d(window, window.pack_slaves(), False, exp=varExp.get())
        return
    if (varD.get()=="Dataset") and (varG.get()=="BoxPlot"):
        draw_boxplot(window, window.pack_slaves(), False, 0, varExp.get())
        return 
    if (varD.get()=="Dataset") and (varG.get()=="BarPlot"):
        draw_barplot(window, window.pack_slaves(), False, varExp.get())
        return 
    if (varD.get()=="Dataset") and (varG.get()=="Heatmap"):
        model_h_ds(window, window.pack_slaves(), True, varExp.get())
        return 
    if (varD.get()=="Dataset") and (varG.get()=="Geo-localization"):
        if len(obj.latitude) != 0:
            draw_geo(window, window.pack_slaves(), 0, varExp.get())
        else:
            messagebox.showwarning("Invalid choice", "The dataset does not contain latitude-longitude data")
        return
    if (var.get()=="All") and (varG.get()=="Time Series"):
        if varDN.get() == "Normalized":
            draw_graph(window, window.pack_slaves(), True, varExp.get(), gt)
        else:
            draw_graph(window, window.pack_slaves(), False, varExp.get(), gt)
        return
    if (var.get()!="All") and (varG.get()=="Time Series"):
        if varDN.get() == "Normalized":
            draw_highlight(window, window.pack_slaves(), True, int(var.get().split(" ")[0]), varExp.get(), gt)
        else:
            draw_highlight(window, window.pack_slaves(), False, int(var.get().split(" ")[0]), varExp.get(), gt)
        return
    if (var.get()=="All") and (varG.get()=="BoxPlot"):
        if varDN.get() == "Normalized":
            draw_boxplot(window, window.pack_slaves(), True, means, varExp.get(), gt)
        else:
            draw_boxplot(window, window.pack_slaves(), False, means, varExp.get(), gt)
        return
    if (var.get()!="All") and (varG.get()=="BoxPlot"):
        if varDN.get() == "Normalized":
            sort_boxplot(window, window.pack_slaves(), True, int(var.get().split(" ")[0]), means, varExp.get(), gt)
        else:
            sort_boxplot(window, window.pack_slaves(), False, int(var.get().split(" ")[0]), means, varExp.get(), gt)
        return
    if (var.get()=="All") and (varG.get()=="BarPlot"):
        if varDN.get() == "Normalized":
            draw_barplot(window, window.pack_slaves(), True, varExp.get(), gt)
        else:
            draw_barplot(window, window.pack_slaves(), False, varExp.get(), gt)
        return
    if (var.get()!="All") and (varG.get()=="BarPlot"):
        if varDN.get() == "Normalized":
            highlight_barplot(window, window.pack_slaves(), True, int(var.get().split(" ")[0]), varExp.get(), gt)
        else:
            highlight_barplot(window, window.pack_slaves(), False, int(var.get().split(" ")[0]), varExp.get(), gt)
        return
    if (var.get()=="All") and (varG.get()=="General Info"):
        create_general_info(window, window.pack_slaves())
        return
    if (var.get()!="All") and (varG.get()=="General Info"):
        var.set("All")
        create_general_info(window, window.pack_slaves())
        messagebox.showwarning("Invalid choice", "In order to view tab 'General Info' Model: All must be selected")
        return
    if (var.get()=="All") and (varG.get()=="2D/3D Scatters"):
        if varDN.get() == "Normalized":
            scatters_2d3d(window, window.pack_slaves(), True, 0, varExp.get(), gt)
        else:
            scatters_2d3d(window, window.pack_slaves(), False, 0, varExp.get(), gt)
        return
    if (var.get()!="All") and (varG.get()=="2D/3D Scatters"):
        if varDN.get() == "Normalized":
            scatters_2d3d(window, window.pack_slaves(), True, int(var.get().split(" ")[0]), varExp.get(), gt)
        else:
            scatters_2d3d(window, window.pack_slaves(), False, int(var.get().split(" ")[0]), varExp.get(), gt)
        return
    if (var.get()=="All") and (varG.get()=="Model Parameters"):
        if varDN.get() == "Normalized":
            model_p(window, window.pack_slaves(), True, means)
        else:
            model_p(window, window.pack_slaves(), False, means)
        return
    if (var.get()!="All") and (varG.get()=="Model Parameters"):
        if varDN.get() == "Normalized":
            highlight_model_p(window, window.pack_slaves(),True, means, int(var.get().split(" ")[0]))
        else:
            highlight_model_p(window, window.pack_slaves(), False, means, int(var.get().split(" ")[0]))
        return
    if (var.get()=="All") and (varG.get()=="Model Parameters 2"):
        if varDN.get() == "Normalized":
            model_p_2(window, window.pack_slaves(), True, means)
        else:
            model_p_2(window, window.pack_slaves(), False, means)
    if (var.get()=="All") and (varG.get()=="Heatmap clustering"):
        if varDN.get() == "Normalized":
            model_h(window, window.pack_slaves(), True, 0, varExp.get(), gt)
        else:
            model_h(window, window.pack_slaves(), False, 0, varExp.get(), gt)
        return
    if (var.get()!="All") and (varG.get()=="Heatmap clustering"):
        if varDN.get() == "Normalized":
            model_h(window, window.pack_slaves(), True, int(var.get().split(" ")[0]), varExp.get(), gt)
        else:
            model_h(window, window.pack_slaves(), False, int(var.get().split(" ")[0]), varExp.get(), gt)
        return
    if (var.get()=="All") and (varG.get()=="Heatmap dataset"):
        if varDN.get() == "Normalized":
            model_h_ds(window, window.pack_slaves(), True, varExp.get())
        else:
            model_h_ds(window, window.pack_slaves(), False, varExp.get())
        return
    if (var.get()!="All") and (varG.get()=="Heatmap dataset"):
        var.set("All")
        if varDN.get() == "Normalized":
            model_h_ds(window, window.pack_slaves(), True, varExp.get())
        else:
            model_h_ds(window, window.pack_slaves(), False, varExp.get())
        messagebox.showwarning("Invalid choice", "In order to view tab 'Heatmap dataset' Model: All must be selected")
        return 
    if (var.get()=="All") and (varG.get()=="Geo-localization"):
        if len(obj.latitude) != 0:
            draw_geo(window, window.pack_slaves(), 0, varExp.get(), gt)
        else:
            messagebox.showwarning("Invalid choice", "The dataset does not contain latitude-longitude data")
        return
    if (var.get()!="All") and (varG.get()=="Geo-localization"): 
        if len(obj.latitude) != 0:
            draw_geo(window, window.pack_slaves(), int(var.get().split(" ")[0]), varExp.get(), gt)
        else:
            messagebox.showwarning("Invalid choice", "The dataset does not contain latitude-longitude data")
        return
    if (var.get()=="All") and (varG.get()=="Dimensionality Reduction"):
        try:
            tsne = open(obj.pathS+"/tsne.csv", 'r')
            tsne.close()
            dim_red(window, window.pack_slaves())
        except:
            messagebox.showwarning("Invalid choice", "The result folder does not contain tsne.csv (tsne data)")
        return
    if (var.get()!="All") and (varG.get()=="Dimensionality Reduction"):
        try:
            tsne = open(obj.pathS+"/tsne.csv", 'r')
            tsne.close()
            dim_red(window, window.pack_slaves(), numbercl= int(var.get().split(" ")[0]))
        except:
            messagebox.showwarning("Invalid choice", "The result folder does not contain tsne.csv (tsne data)")
        return

def crea(window):
    popup = Toplevel(window)
    popup.title("Create new Clustering")
    cont = Frame(popup)
    cont.pack(side=TOP, expand=1, fill=BOTH)
    contW = Frame(cont)
    contW.pack(fill=BOTH, expand=1)
    continueC(popup, contW, cont)
    popup.mainloop()
    
def rgb_to_hex(r,g,b):
    hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
    return hex      

def first(nc, means, window, list_slaves, sidebar):
    if(len(sidebar.pack_slaves())>0):
        for item in sidebar.pack_slaves():
            item.destroy()
    if obj.pathS != "/":
        options = ["All"]
        var.set(options[0])
        optionsApp = []
        for i in range(1, nc+1):
            optionsApp.append(str(i))
        #means = graph.silhouette(pathD, pathS)
        meansS = list(np.copy(means))
        #clusternorm, clustergiusti, cl = obj.get_cl()
        #df, latitude, longitude, experiment = obj.get_dataset()
        #su = obj.compute_su(obj.clusternorm, obj.dataset)
        rows, cols = obj.dataset.shape
        #meansI = silhouette(pathD, pathS)
        """
        meansB = np.copy(meansS)
        for i in range(0,cols):
            pos = su.index(max(su))
            freq = [[] for x in obj.clusterset]
            r = 0
            for c in obj.clusternorm:
                freq[int(c)-1].append(obj.dataset.iloc[r,pos])
                r = r+1
            means = list(np.copy(meansB))
            su[pos] = -1
        """
        freq = [[] for x in obj.clusterset]
        for i, cluster in enumerate(obj.clusterset):
            for c in obj.clusternorm:
                if c == cluster:
                    freq[i].append(1)
        points = []
        for i in range(0, len(obj.clusterset)):
            points.append(len(freq[i]))
        colorset = [pl.cm.jet(item/len(obj.clusterset)) for item in list(set(obj.clusternorm))]
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        colorsF = []
        for i in range(0, len(optionsApp)):
            pos = meansS.index(max(meansS))
            options.append(optionsApp[pos]+" ({0:.3f})".format(meansS[pos])+" - {}".format(points[pos]))
            colorsF.append(colorset[pos])
            meansS[pos] = -2
        labelN = Label(sidebar, text="Model: ")
        labelN.pack(side=LEFT)
        drop = OptionMenu(sidebar, var, *options)
        for i in range(0, len(options)-1):
            drop["menu"].entryconfigure(i+1, activebackground=rgb_to_hex(int(colorsF[i][0]*255), int(colorsF[i][1]*255), int(colorsF[i][2]*255)) , background=rgb_to_hex(int(colorsF[i][0]*255), int(colorsF[i][1]*255), int(colorsF[i][2]*255))) 
        drop.pack(side=LEFT)
        gi = pd.read_csv(obj.pathS+"generalInfo.csv",error_bad_lines=False, warn_bad_lines=False).values
        global optionsG
        if "IHMM" in gi:
            optionsG = ["General Info", "Model Parameters", "Model Parameters 2", "Heatmap clustering", "Heatmap dataset", "Time Series", "2D/3D Scatters", "BoxPlot", "BarPlot", "Geo-localization", "Dimensionality Reduction"]
        if "GMM" in gi:
            optionsG = ["General Info", "Model Parameters", "Model Parameters 2", "Heatmap clustering", "Heatmap dataset", "Time Series", "2D/3D Scatters", "BoxPlot", "BarPlot", "Geo-localization", "Dimensionality Reduction"]
        if "TICC" in gi:
            optionsG = ["General Info", "Model Parameters", "Model Parameters 2", "Heatmap clustering", "Heatmap dataset", "Time Series", "2D/3D Scatters", "BoxPlot", "BarPlot", "Geo-localization", "Dimensionality Reduction"]
        varG.set(optionsG[0])
        labelT = Label(sidebar, text="Visualization Type: ")
        labelT.pack(side=LEFT)
        dropG = OptionMenu(sidebar, varG, *optionsG)
        dropG.pack(side=LEFT)
        varS.set(optionsO[0])
        labelS = Label(sidebar, text="Sorting: ")
        labelS.pack(side=LEFT)
        dropS = OptionMenu(sidebar, varS, *optionsO)
        dropS.pack(side=LEFT)
        try:
            open(obj.pathS+"dataStandardization.csv", 'r')
            varDN.set(optionsDN[0])
            labelDN = Label(sidebar, text="Data: ")
            labelDN.pack(side=LEFT)
            dropDN = OptionMenu(sidebar, varDN, *optionsDN)
            dropDN.pack(side=LEFT)
        except:
            varDN.set(None)
        if len(obj.experiments) != 0:
            exps = list(pd.unique(obj.experiments))
            optionsExp = ["All"]
            for exp in exps:
                optionsExp.append(exp)
            varExp.set(optionsExp[0])
            labelExp = Label(sidebar, text="Experiments: ")
            labelExp.pack(side=LEFT)
            dropExp = OptionMenu(sidebar, varExp, *optionsExp)
            dropExp.pack(side=LEFT)
        else:
            varExp.set("All")
        start = Button(sidebar)
        start.configure(text="GO", command=handler)
        start.pack(side=LEFT)
        if obj.pathGT != "":
            #varGT.set(optionsGT[0])
            #varGT.trace("w", lambda: switch_fun(window, sidebar, pathD, pathS, pathGT, False))
            #dropGT = OptionMenu(sidebar, varGT, *optionsGT)
            #dropGT.pack(side=LEFT)
            switch = Button(sidebar)
            switch.configure(text="Ground Truth", command= lambda: switch_fun(window, sidebar, pathD, pathS, pathGT, True))
            switch.pack(side=LEFT)
        #return means
        
    else:
        #df, latitude, longitude, experiment = graph.get_dataset(pathD, pathS, False)
        varD.set(optionsDa[0])
        labelN = Label(sidebar, text="Model: ")
        labelN.pack(side=LEFT)
        drop = OptionMenu(sidebar, varD, *optionsDa)
        drop.pack(side=LEFT)
        varG.set(optionsD[0])
        labelT = Label(sidebar, text="Visualization Type: ")
        labelT.pack(side=LEFT)
        dropG = OptionMenu(sidebar, varG, *optionsD)
        dropG.pack(side=LEFT)
        if len(obj.experiments) != 0:
            exps = list(pd.unique(obj.experiments))
            optionsExp = ["All"]
            for exp in exps:
                optionsExp.append(exp)
            varExp.set(optionsExp[0])
            labelExp = Label(sidebar, text="Experiments: ")
            labelExp.pack(side=LEFT)
            dropExp = OptionMenu(sidebar, varExp, *optionsExp)
            dropExp.pack(side=LEFT)
        start = Button(sidebar)
        start.configure(text="GO", command=handler)
        start.pack(side=LEFT)
    """
    diz = Button(sidebar)
    diz.configure(text="Dictionary", command= lambda : view_dictionary(window, window.pack_slaves()))
    diz.pack(side=LEFT)
    """  

def switch_fun(window, sidebar, pathD, pathS, pathGT, which):
    for item in sidebar.pack_slaves():
        item.destroy()
    global gt
    if which == False:
        """global pathS
        pathS = pathSBack"""
        gt = False
        do_nc(pathS)
        first(nc, means, window, window.pack_slaves(), window.pack_slaves()[1])
        create_general_info(window, window.pack_slaves())
    else:
        gt = True
        do_nc(pathS, pathGT)
        options = ["All"]
        var.set(options[0])
        for i in range(1, nc+1):
            options.append(str(i))
        #clusternorm, clustergiusti, cl = graph.get_cl(pathD, pathS, pathGT)
        colorset = [pl.cm.jet(item/len(obj.clustersetGT)) for item in list(set(obj.clustersetGT))]
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        colorsF = []
        for i in range(0, len(options)-1):
            colorsF.append(colorset[i])
        labelN = Label(sidebar, text="Model: ")
        labelN.pack(side=LEFT)
        drop = OptionMenu(sidebar, var, *options)
        for i in range(0, len(options)-1):
            drop["menu"].entryconfigure(i+1, activebackground=rgb_to_hex(int(colorsF[i][0]*255), int(colorsF[i][1]*255), int(colorsF[i][2]*255)) , background=rgb_to_hex(int(colorsF[i][0]*255), int(colorsF[i][1]*255), int(colorsF[i][2]*255))) 
        drop.pack(side=LEFT)
        varG.set(optionsG[0])
        labelT = Label(sidebar, text="Visualization Type: ")
        labelT.pack(side=LEFT)
        optionsGT1 = [item for item in optionsG if item != "General Info" and item != "Model Parameters" and item != "Heatmap dataset" and item != "Dimensionality Reduction"]
        varG.set(optionsGT1[0])
        dropG = OptionMenu(sidebar, varG, *optionsGT1)
        dropG.pack(side=LEFT)
        varS.set(optionsO[0])
        labelS = Label(sidebar, text="Sorting: ")
        labelS.pack(side=LEFT)
        dropS = OptionMenu(sidebar, varS, *optionsO)
        dropS.pack(side=LEFT)
        try:
            varDN.set(optionsDN[0])
            labelDN = Label(sidebar, text="Data: ")
            labelDN.pack(side=LEFT)
            dropDN = OptionMenu(sidebar, varDN, *optionsDN)
            dropDN.pack(side=LEFT)
        except:
            varDN.set(None)
        if len(obj.experiments) != 0:
            exps = list(pd.unique(obj.experiments))
            optionsExp = ["All"]
            for exp in exps:
                optionsExp.append(exp)
            varExp.set(optionsExp[0])
            labelExp = Label(sidebar, text="Experiments: ")
            labelExp.pack(side=LEFT)
            dropExp = OptionMenu(sidebar, varExp, *optionsExp)
            dropExp.pack(side=LEFT)
        else:
            varExp.set("All")
        #varGT.trace("w", lambda: switch_fun(window, sidebar, pathD, pathS, pathGT, False))
        #dropGT = OptionMenu(sidebar, varGT, *optionsGT)
        #dropGT.pack(side=LEFT)
        start = Button(sidebar)
        start.configure(text="GO", command=handler)
        start.pack(side=LEFT)
        switch = Button(sidebar)
        switch.configure(text="Go to Results", command= lambda: switch_fun(window, sidebar, pathD, pathS, pathGT, False))
        switch.pack(side=LEFT)
        model_h(window, window.pack_slaves(), False, 0, "All", gt)
        #draw_graph(window, window.pack_slaves(), False, GT=gt)
    
def openD(window, sidebar):    
    #global pathD
    #global pathS
    popup = Toplevel(window)
    popup.title("Open")
    contOpen = Frame(popup)
    contOpen.pack(anchor="s", expand=1, fill=BOTH)
    frameOpen = Frame(contOpen)
    frameOpen.pack(side=TOP)
    frameRes = Frame(contOpen)
    frameRes.pack(side=TOP)
    frameGT = Frame(contOpen)
    frameGT.pack(side=TOP)
    textOpen = Text(frameOpen, height=1)
    textRes = Text(frameRes, height=1)
    textRes.pack(side=RIGHT, fill=X, expand=1)
    textOpen.pack(side=RIGHT, fill=X, expand=1)
    textGT = Text(frameGT, height=1)
    textGT.pack(side=RIGHT, fill=X, expand=1)
    openData = Button(frameOpen, text='Open Dataset', command=lambda : openDataset(popup, textOpen))
    openRes = Button(frameRes, text='Open Results', command=lambda : openResults(popup, textRes))
    openGT = Button(frameGT, text='Open Ground Truth', command=lambda : openGroundTruth(popup, textGT))
    openGT.pack(side=LEFT)
    openData.pack(side=LEFT)
    openRes.pack(side=LEFT)
    goButton = Button(contOpen)
    goButton.configure(text="LOAD", command= lambda: on_load(window, window.pack_slaves(), str(textOpen.get("1.0","end-1c")), str(textRes.get("1.0","end-1c"))+"/", str(textGT.get("1.0","end-1c"))))
    goButton.pack(side=BOTTOM)
    popup.mainloop()
    do_nc(pathS+"/")
    
        
def do_nc(pathS, pathGT=""):
    if pathGT != "":
        clu = open(pathGT,'r').readlines()
    else:
        clu = open(pathS+'/cl.txt','r').readlines()
    global nc 
    nc = len(set(clu))
    
def updateV(cb, fromF, contC, norm, window, numbercl=0, exp="All", GT=False):
    n = 0
    for i in list(cb.state()):
        if i == 1:
            n+=1
    if n > 12:
        messagebox.showerror("Too many variables", "Choose 10 variables at max")
        return
    if n==0:
        messagebox.showerror("Too few variables", "Choose at least 1 variable")
        return
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    for item in contC.pack_slaves():
        item.destroy()
    if fromF == "DG":
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        fig = obj.draw_timeseries(norm, cb.state(), exp, GT)
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        #canvas.draw()
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
        for ax in canvas.figure.axes:
            zoomer.add_ax(ax, ['size'])
    elif fromF == "DB":
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        if GT:
            fig = obj.draw_boxplot(0, norm, cb.state(), exp, GT)
        else:
            fig = obj.draw_boxplot(means, norm, cb.state(), exp, GT)
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        #canvas.draw()
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
    elif fromF == "DH":
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        fig = obj.draw_barplot(norm, cb.state(), exp, GT)
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        #canvas.draw()
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
    elif fromF == "HG":
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        fig = obj.highlight_cluster(norm, numbercl, cb.state(), exp, GT)
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        #canvas.draw()
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
        for ax in canvas.figure.axes:
            zoomer.add_ax(ax, ['size'])
    elif fromF == "HB":
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        if GT:
            fig, points, rows = obj.sort_boxplot(0, norm, numbercl, cb.state(), exp, GT)
        else:
            fig, points, rows = obj.sort_boxplot(means, norm, numbercl, cb.state(), exp, GT)
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        #canvas.draw()
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
        points = Label(contC, text="NbPoints: "+str(points)+"/"+str(rows))
        points.pack(side = BOTTOM)
    if fromF == "HH":
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        fig, points, rows = obj.highlight_barplot(norm, numbercl, cb.state(), exp, GT)
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        #canvas.draw()
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
        points = Label(contC, text="NbPoints: "+str(points)+"/"+str(rows))
        points.pack(side = BOTTOM)
    if fromF == "GEO":
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        fig = obj.geo_localization(cb.state(), 0, exp, GT)
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        #canvas.draw()
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
        for ax in canvas.figure.axes:
            zoomer.add_ax(ax, ['size'])
    if fromF == "GEOH":
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        fig = obj.geo_localization(cb.state(), numbercl, exp, GT)
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        #canvas.draw()
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
        for ax in canvas.figure.axes:
            zoomer.add_ax(ax, ['size'])
    ls.__exit__(None, None, None)

def deconstruct(window, ls):
    for i in window.pack_slaves():
            i.destroy()
    sidebar = Frame(window)
    sidebar.pack(side=TOP, fill=X)
    cont = Frame(window)
    cont.pack(side=TOP, expand=1, fill=BOTH)
    #var = StringVar(sidebar)
    #varG = StringVar(sidebar)
    #optionsG = ["Time Series", "BoxPlot", "BarPlot", "General Info"]
    #varS = StringVar(sidebar)
    #optionsO = ["Symmetrical Uncertainty"]
    make_welcome(window, cont)
    ls.__exit__(None, None, None)
    messagebox.showerror("ERROR", "Dataset may contain non-numerical values or may not correspond to clustering results")
    window.update()

def support(window):
    popup = Toplevel(window)
    l = Listbox(popup, height=5)
    l.pack(side=LEFT, fill=BOTH, expand=1)
    s = ttk.Scrollbar(popup, orient=VERTICAL, command=l.yview)
    s.pack(side=LEFT, fill=Y)
    l['yscrollcommand'] = s.set
    ttk.Sizegrip().pack(fill=BOTH)
    #popup.grid_columnconfigure(0, weight=1)
    #popup.grid_rowconfigure(0, weight=1)
    file = open("README.md", "r")
    for line in file:
        text = line.split("\n")
        l.insert(END, str(text[0]))
    popup.mainloop()

def draw_graph(window, list_slaves, norm=False, exp="All", GT=False):    
    #try:
        ls = Splash(window, "IMG/hg.gif")
        ls.__enter__()
        if len(window.pack_slaves())==2:
            window.pack_slaves()[0].destroy()
            window.pack_slaves()[0].destroy()
            contMenu = Frame(window)
            contMenu.pack()
            menu = Menu(contMenu)
            window.config(menu=menu)
            file = Menu(menu)
            file.add_command(label='Open Cluster Results', command = lambda: openD(window, sidebar))
            file.add_command(label='Create New Clustering', command = lambda: crea(window))
            file.add_command(label='?', command = lambda: support(window))
            menu.add_cascade(label='File', menu = file)
            sidebar = Frame(window)
            sidebar.pack(side=TOP, fill=X)
            first(nc, window, window.pack_slaves(), window.pack_slaves()[1], pathD, pathS, pathGT)
            var.set(None)
        else: 
            if len(window.pack_slaves()) > 3:
                list_slaves[2].destroy()
                list_slaves[3].destroy()
            else:
                list_slaves[2].destroy()
        fixed = []
        if obj.pathS != "/":
            fixed.append("Clusters")
        if len(obj.latitude) != 0:
            fixed.append("Geo")
        vs = fixed + list(obj.dataset)
        if obj.pathS != "/":
            do_nc(obj.pathS)
            ordV = obj.sort_var(GT)
        else:
            ordV = [item for item in range(0,len(vs))]
        contCB = Frame(window)
        contCB.pack(side=LEFT, fill=Y)
        labelV = Label(contCB, text="Variables")
        labelV.pack(side=TOP)
        sframe = VerticalScrolledFrame(contCB)
        sframe.pack(side=TOP)
        cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV)
        cb.pack()
        if np.array(obj.usedV==np.zeros(len(obj.usedV))).all() or 0 != obj.numbercl:
            c = 0
            for chk in cb.chks:
                if c < 12:
                    chk.select()
                c+=1
        else:
            for c, chk in enumerate(cb.chks):
                if obj.usedV[c] == 1:
                    chk.select()
        contU = Frame(contCB)
        contU.pack(side=TOP)
        update = Button(contU)
        update.configure(text="Update", command= lambda: updateV(cb, "DG", contC, norm, window, 0, exp, GT))
        update.pack(side=TOP)
        contC = Frame(window)
        contC.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        fig = obj.draw_timeseries(norm, cb.state(), exp, GT)
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        #canvas.draw()
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
        for ax in canvas.figure.axes:
            zoomer.add_ax(ax, ['size'])
        ls.__exit__(None, None, None)
    #except ValueError:
    #    deconstruct(window, ls)
        
        
def draw_boxplot(window, list_slaves, norm=False, means=0, exp="All", GT=False):   
    #try:
        ls = Splash(window, "IMG/hg.gif")
        ls.__enter__()
        if len(window.pack_slaves()) > 3:
            list_slaves[2].destroy()
            list_slaves[3].destroy()
        else:
            list_slaves[2].destroy()
        fixed = []
        if obj.pathS != "/":
            fixed.append("Clusters")
        if len(obj.latitude) != 0:
            fixed.append("Geo")
        vs = fixed + list(obj.dataset)
        if obj.pathS != "/":
            do_nc(obj.pathS)
            ordV = obj.sort_var()
        else:
            ordV = [item for item in range(0,len(vs))]
        contCB = Frame(window)
        contCB.pack(side=LEFT, fill=Y)
        labelV = Label(contCB, text="Variables")
        labelV.pack(side=TOP)
        sframe = VerticalScrolledFrame(contCB)
        sframe.pack(side=TOP)
        cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV)
        cb.pack()
        if np.array(obj.usedV==np.zeros(len(obj.usedV))).all() or 0 != obj.numbercl:
            c = 0
            for chk in cb.chks:
                if c < 12:
                    chk.select()
                c+=1
        else:
            for c, chk in enumerate(cb.chks):
                if obj.usedV[c] == 1:
                    chk.select()
        contU = Frame(contCB)
        contU.pack(side=TOP)
        update = Button(contU)
        update.configure(text="Update", command= lambda: updateV(cb, "DB", contC, norm, window, 0, exp, GT))
        update.pack(side=TOP)
        contC = Frame(window)
        contC.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        fig = obj.draw_boxplot(means, norm, cb.state(), exp, GT)
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        #canvas.draw()
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
        ls.__exit__(None, None, None)
    #except ValueError:
    #    deconstruct(window, ls)
    
def draw_barplot(window, list_slaves, norm=False, exp="All", GT=False): 
    #try:
        
        ls = Splash(window, "IMG/hg.gif")
        ls.__enter__()
        if len(window.pack_slaves()) > 3:
            list_slaves[2].destroy()
            list_slaves[3].destroy()
        else:
            list_slaves[2].destroy()
        fixed = []
        if obj.pathS != "/":
            fixed.append("Clusters")
        if len(obj.latitude) != 0:
            fixed.append("Geo")
        vs = fixed + list(obj.dataset)
        if obj.pathS != "/":
            do_nc(obj.pathS)
            ordV = obj.sort_var()
        else:
            ordV = [item for item in range(0,len(vs))]
        contCB = Frame(window)
        contCB.pack(side=LEFT, fill=Y)
        labelV = Label(contCB, text="Variables")
        labelV.pack(side=TOP)
        sframe = VerticalScrolledFrame(contCB)
        sframe.pack(side=TOP)
        cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV)
        cb.pack()
        if np.array(obj.usedV==np.zeros(len(obj.usedV))).all() or 0 != obj.numbercl:
            c = 0
            for chk in cb.chks:
                if c < 12:
                    chk.select()
                c+=1
        else:
            for c, chk in enumerate(cb.chks):
                if obj.usedV[c] == 1:
                    chk.select()
        contU = Frame(contCB)
        contU.pack(side=TOP)
        update = Button(contU)
        update.configure(text="Update", command= lambda: updateV(cb, "DH", contC, norm, window, 0, exp, GT))
        update.pack(side=TOP)
        contC = Frame(window)
        contC.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        fig = obj.draw_barplot(norm, cb.state(), exp, GT)
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
        ls.__exit__(None, None, None)
    #except ValueError:
    #    deconstruct(window, ls)
    
def draw_highlight(window, list_slaves, norm, numbercl, exp="All", GT=False):  
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    if len(window.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    selected = []
    if obj.method == "SubCMedians":
        try:
            mp = pd.read_csv(obj.pathS+'model_parameters.txt', sep='\s+')
            order = obj.sort_var(GT, numbercl)
            ord_coN = []
            for i in range(0, len(order)):
               ord_coN.append(mp[mp.columns[order[i]]])
            ord_coN = pd.DataFrame(ord_coN).T
            cols = ord_coN.shape[1]
            ord_coN = ord_coN.values
            for i in range(0, cols):
                if str(ord_coN[numbercl-1][i]) != "nan":
                    selected.append(1)
                else:
                    selected.append(0)
        except:
            pass
    fixed = []
    if obj.pathS != "/":
        fixed.append("Clusters")
        if len(obj.latitude) != 0:
            fixed.append("Geo")
    vs = fixed + list(obj.dataset)
    if obj.pathS != "/":
        do_nc(obj.pathS)
        ordV = obj.sort_var(GT, numbercl)
    else:
        ordV = [item for item in range(0,len(vs))]
    contCB = Frame(window)
    contCB.pack(side=LEFT, fill=Y)
    labelV = Label(contCB, text="Variables")
    labelV.pack(side=TOP)
    sframe = VerticalScrolledFrame(contCB)
    sframe.pack(side=TOP)
    cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV, selected=selected)
    cb.pack()
    if np.array(obj.usedV==np.zeros(len(obj.usedV))).all() or numbercl != obj.numbercl:
        c = 0
        for chk in cb.chks:
            if c < 12:
                chk.select()
            c+=1
    else:
        for c, chk in enumerate(cb.chks):
            if obj.usedV[c] == 1:
                chk.select()
    contU = Frame(contCB)
    contU.pack(side=TOP)
    update = Button(contU)
    update.configure(text="Update", command= lambda: updateV(cb, "HG", contC, norm, window, numbercl, exp, GT))
    update.pack(side=TOP)
    contC = Frame(window)
    contC.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(contC, background='white')
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    fig = obj.highlight_cluster(norm, numbercl, cb.state(), exp, GT)
    canvas = FigureCanvasTkAgg(fig, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    tool = NavigationToolbar2Tk(canvas, contC)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    obj.add_subplot_zoom(canvas)
    for ax in canvas.figure.axes:
        zoomer.add_ax(ax, ['size'])
    ls.__exit__(None, None, None)
    

def highlight_barplot(window, list_slaves, norm, numbercl, exp="All", GT=False): 
    try:
        ls = Splash(window, "IMG/hg.gif")
        ls.__enter__()
        if len(window.pack_slaves()) > 3:
            list_slaves[2].destroy()
            list_slaves[3].destroy()
        else:
            list_slaves[2].destroy()
        #df, latitude, longitude, experiment = graph.get_dataset(pathD, pathS, norm, exp)
        selected = []
        if obj.method == "SubCMedians":
            try:
                mp = pd.read_csv(obj.pathS+'model_parameters.txt', sep='\s+')
                order = obj.sort_var(GT, numbercl)
                ord_coN = []
                for i in range(0, len(order)):
                   ord_coN.append(mp[mp.columns[order[i]]])
                ord_coN = pd.DataFrame(ord_coN).T
                cols = ord_coN.shape[1]
                ord_coN = ord_coN.values
                for i in range(0, cols):
                    if str(ord_coN[numbercl-1][i]) != "nan":
                        selected.append(1)
                    else:
                        selected.append(0)
            except:
                pass
        fixed = []
        if obj.pathS != "/":
            fixed.append("Clusters")
            if len(obj.latitude) != 0:
                fixed.append("Geo")
        vs = fixed + list(obj.dataset)
        if obj.pathS != "/":
            do_nc(obj.pathS)
            ordV = obj.sort_var(GT, numbercl)
        else:
            ordV = [item for item in range(0,len(vs))]
        contCB = Frame(window)
        contCB.pack(side=LEFT, fill=Y)
        labelV = Label(contCB, text="Variables")
        labelV.pack(side=TOP)
        sframe = VerticalScrolledFrame(contCB)
        sframe.pack(side=TOP)
        cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV, selected=selected)
        cb.pack()
        if np.array(obj.usedV==np.zeros(len(obj.usedV))).all() or numbercl != obj.numbercl:
            c = 0
            for chk in cb.chks:
                if c < 12:
                    chk.select()
                c+=1
        else:
            for c, chk in enumerate(cb.chks):
                if obj.usedV[c] == 1:
                    chk.select()
        contU = Frame(contCB)
        contU.pack(side=TOP)
        update = Button(contU)
        update.configure(text="Update", command= lambda: updateV(cb, "HH", contC, norm, window, numbercl, exp, GT))
        update.pack(side=TOP)
        contC = Frame(window)
        contC.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(contC, background='white')
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        fig, points, rows = obj.highlight_barplot(norm, numbercl, cb.state(), exp, GT)
        if fig == 0:
            ls.__exit__(None, None, None)
            messagebox.showerror("Not found","This cluster doesn't exists in the selected experiment.")
            return
        canvas = FigureCanvasTkAgg(fig, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        tool = NavigationToolbar2Tk(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        obj.add_subplot_zoom(canvas)
        points = Label(contC, text="NbPoints: "+str(points)+"/"+str(rows))
        points.pack(side = BOTTOM)
        ls.__exit__(None, None, None)
    except ValueError:
        deconstruct(window, ls)
    
def sort_boxplot(window, list_slaves, norm, numbercl, means=0, exp="All", GT=False): 
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    if len(window.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    selected = []
    if obj.method == "SubCMedians":
        try:
            mp = pd.read_csv(obj.pathS+'model_parameters.txt', sep='\s+')
            order = obj.sort_var(GT, numbercl)
            ord_coN = []
            for i in range(0, len(order)):
               ord_coN.append(mp[mp.columns[order[i]]])
            ord_coN = pd.DataFrame(ord_coN).T
            cols = ord_coN.shape[1]
            ord_coN = ord_coN.values
            for i in range(0, cols):
                if str(ord_coN[numbercl-1][i]) != "nan":
                    selected.append(1)
                else:
                    selected.append(0)
        except:
            pass
    fixed = []
    if obj.pathS != "/":
        fixed.append("Clusters")
        if len(obj.latitude) != 0:
            fixed.append("Geo")
    vs = fixed + list(obj.dataset)
    if obj.pathS != "/":
        do_nc(obj.pathS)
        ordV = obj.sort_var(GT, numbercl)
    else:
        ordV = [item for item in range(0,len(vs))]
    contCB = Frame(window)
    contCB.pack(side=LEFT, fill=Y)
    labelV = Label(contCB, text="Variables")
    labelV.pack(side=TOP)
    sframe = VerticalScrolledFrame(contCB)
    sframe.pack(side=TOP)
    cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV, selected=selected)
    cb.pack()
    if np.array(obj.usedV==np.zeros(len(obj.usedV))).all() or numbercl != obj.numbercl:
        c = 0
        for chk in cb.chks:
            if c < 12:
                chk.select()
            c+=1
    else:
        for c, chk in enumerate(cb.chks):
            if obj.usedV[c] == 1:
                chk.select()
    contU = Frame(contCB)
    contU.pack(side=TOP)
    update = Button(contU)
    update.configure(text="Update", command= lambda: updateV(cb, "HB", contC, norm, window, numbercl, exp, GT))
    update.pack(side=TOP)
    contC = Frame(window)
    contC.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(contC, background='white')
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    fig, points, rows = obj.sort_boxplot(means, norm, numbercl, cb.state(), exp, GT)
    if fig == 0:
        ls.__exit__(None, None, None)
        messagebox.showerror("Not found","This cluster doesn't exists in the selected experiment.")
        return
    canvas = FigureCanvasTkAgg(fig, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    tool = NavigationToolbar2Tk(canvas, contC)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    obj.add_subplot_zoom(canvas)
    points = Label(contC, text="NbPoints: "+str(points)+"/"+str(rows))
    points.pack(side = BOTTOM)
    ls.__exit__(None, None, None)

    
def secure(window, pathD):
    sure = Toplevel(window)
    cont = Frame(sure)
    cont.pack(side=TOP)
    contS = Frame(sure)
    contS.pack(side=BOTTOM)
    label = Label(cont)
    label.configure(text="No clustering selected.\nAre you sure to procede?", font=8)
    label.pack(side=TOP)
    yes = Button(contS, text="Yes", command= lambda: simple_data(sure, window, pathD))
    no = Button(contS, text="No", command= lambda: sure.destroy())
    yes.pack(side=LEFT)
    no.pack(side=RIGHT)
    sure.geometry('+{}+{}'.format(Xpos, Ypos))
    sure.mainloop()

def simple_data(sure, window, pathD):
    sure.destroy()
    for item in window.pack_slaves():
        item.destroy()
    contMenu = Frame(window)
    contMenu.pack()
    menu = Menu(contMenu)
    window.config(menu=menu)
    file = Menu(menu)
    file.add_command(label='Open Cluster Results', command = lambda: openD(window, sidebar))
    file.add_command(label='Create New Clustering', command = lambda: crea(window))
    file.add_command(label='?', command = lambda: support(window))
    menu.add_cascade(label='File', menu = file)
    sidebar = Frame(window)
    sidebar.pack(side=TOP, fill=X)
    global obj
    obj = XM_only_data(pathD)
    global nc
    nc = 0
    global means
    means = 0
    first(nc, "", window, window.pack_slaves(), sidebar)
    placeholder = Frame(window)
    placeholder.pack()
    draw_graph(window, window.pack_slaves(), False)

def create_general_info(window, list_slaves, norm=False):  
    global gt
    gt = False
    #try:
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    locale.setlocale(locale.LC_NUMERIC, 'C')
    if len(window.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        if len(window.pack_slaves()) != 2:
            list_slaves[2].destroy()
        else:
            list_slaves[1].destroy()
    #global means
    #means = graph.silhouette(pathD, pathS)
    varD.set(None)
    df, general = obj.general_info()
    f = Frame(window)
    f.pack(fill=BOTH, expand=1)
    f1 = Frame(f)
    f1.pack(side=LEFT, fill=BOTH,expand=1)
    f2 = Frame(f)
    f2.pack(side=LEFT, fill=BOTH,expand=1)
    #df = TableModel.getSampleData()
    pt = Table(f1, dataframe=df)
    #pt.adjustColumnWidths()
    pt2 = Table(f2, dataframe=general)
    pt.show()    
    pt2.show()   
    ls.__exit__(None, None, None)
    #except ValueError:
    #    deconstruct(window, ls)

def on_load(window, list_slaves, pathD, pathS, pathGT="", norm=False):
    if pathD == "":
        messagebox.showerror("No Dataset Selected","Please select a dataset")
        return
    if pathS != "/":
        ls = Splash(window, "IMG/hg.gif")
        ls.__enter__()
        fileM = open(pathS+"generalInfo.csv", 'r')
        r = 0
        clS = []
        clN = []
        for lines in fileM:
            r +=1
            if r == 6:
                method = lines.split(",")[1].strip()
            if r > 20 and method == "SubCMedians":
                clS.append(lines.split(",")[0])
                clN.append(lines.split(",")[1].strip())
            if r > 17 and method == "K-Means":
                clS.append(lines.split(",")[0])
                clN.append(0)
            if r > 18 and method == "GMM":
                clS.append(lines.split(",")[0])
                clN.append(0)
            if r > 16 and method == "Spectral Clustering":
                clS.append(lines.split(",")[0])
                clN.append(0)
            if r > 22 and method == "TICC":
                clS.append(lines.split(",")[0])
                clN.append(0)
            if r > 18 and (method == "IHMM" or method== "HMM"):
                clS.append(lines.split(",")[0])
                clN.append(0)
        clS = [float(item) for item in clS]
        clN = [float(item) for item in clN]
        """if r== 17:
            fileA = open(pathS+"generalInfo.csv", 'a')
            clS = graph.silhouette(pathD, pathS)
            for cl in clS:
                fileA.write("{0:.3f}".format(cl)+"\n")"""
        global means
        global meansN
        for item in window.pack_slaves():
            item.destroy()
        for item in window.grid_slaves():
            item.destroy()
        means = clS
        meansN = clN
        #window.pack_slaves()[0].destroy()
        #window.pack_slaves()[0].destroy()
        contMenu = Frame(window)
        contMenu.pack()
        menu = Menu(contMenu)
        window.config(menu=menu)
        file = Menu(menu)
        file.add_command(label='Open Cluster Results', command = lambda: openD(window, sidebar))
        file.add_command(label='Create New Clustering', command = lambda: crea(window))
        file.add_command(label='?', command = lambda: support(window))
        menu.add_cascade(label='File', menu = file)
        sidebar = Frame(window)
        sidebar.pack(side=TOP, fill=X)
        global obj
        clust = XM_clustering_results(pathD, pathS, pathGT)
        obj = clust
        do_nc(pathS)
        first(nc, means, window, list_slaves, window.pack_slaves()[1])
        create_general_info(window, list_slaves, norm)
        ls.__exit__(None, None, None)
    else:
        secure(window, pathD)
    
def draw_geo(window, list_slaves, numbercl=0, exp="All", GT=False):
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    if len(window.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    if len(obj.experiments)!=0:
        exps = list(pd.unique(obj.experiments))
        sort= []
        for i in range(0, len(exps)):
            sort.append(i)
        contCB = Frame(window)
        contCB.pack(side=LEFT, fill=Y)
        labelV = Label(contCB, text="Experiments")
        labelV.pack(side=TOP)
        sframe = VerticalScrolledFrame(contCB)
        sframe.pack(side=TOP)
        cb = Checkbar(sframe.interior, exps, side=TOP, sort=sort)
        cb.pack()
        c = 0
        for chk in cb.chks:
            if c < 6:
                chk.select()
            c+=1
        contU = Frame(contCB)
        contU.pack(side=TOP)
        update = Button(contU)
        if numbercl == 0:
            update.configure(text="Update", command= lambda: updateV(cb, "GEO", contC, False, window, 0, exp, GT))
        else:
            update.configure(text="Update", command= lambda: updateV(cb, "GEOH", contC, False, window, numbercl, exp, GT))
        update.pack(side=TOP)
    contC = Frame(window)
    contC.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(contC, background='white')
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    try:
        fig = obj.geo_localization(cb.state(), numbercl, exp, GT)
    except:
        fig = obj.geo_localization([1], 0, exp, GT)
    canvas = FigureCanvasTkAgg(fig, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    #canvas.draw()
    tool = NavigationToolbar2Tk(canvas, contC)
    tool.update()
    canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
    obj.add_subplot_zoom(canvas)
    for ax in canvas.figure.axes:
        zoomer.add_ax(ax, ['size'])
    ls.__exit__(None, None, None)


def draw_2d(cont, norm, var1, var2, numbercl, exp, GT):
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    for item in cont.pack_slaves():
        item.destroy()
    my_canvas = Canvas(cont, background='white')
    my_canvas.pack(side=BOTTOM,fill=BOTH, expand=1)
    fig = obj.scatter_2d(norm, var1, var2, numbercl, exp, GT)
    canvas = FigureCanvasTkAgg(fig, my_canvas)
    canvas.get_tk_widget().pack(fill=X, expand=1)
    #canvas.draw()
    tool = NavigationToolbar2Tk(canvas, cont)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    for ax in canvas.figure.axes:
        zoomer.add_ax(ax, ['size'])
    ls.__exit__(None, None, None)
    
def draw_3d(cont, norm, var1, var2, var3, numbercl, exp, GT):
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    for item in cont.pack_slaves():
        item.destroy()
    #my_canvas = Canvas(cont, background='white')
    #my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    #fig = graph.scatter_3d(pathD, pathS, pathGT, norm, var1, var2, var3, numbercl, exp)
    fig = Figure(figsize=(6,6), dpi=100, facecolor="white")
    canvas = FigureCanvasTkAgg(fig, cont)
    tool = NavigationToolbar2Tk(canvas, cont)
    tool.update()
    canvas.get_tk_widget().pack(fill=X, expand=1)
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    fig = obj.scatter_3d(norm, fig, var1, var2, var3, numbercl, exp, GT)
    #canvas.draw()
    ls.__exit__(None, None, None)

def scatters_2d(norm, cont, numbercl, exp, GT):
    labels = list(obj.dataset)
    for item in cont.pack_slaves():
        item.destroy()
    contScatter = Frame(cont)
    contScatter.pack(side=TOP,fill=BOTH, expand=1)
    
    canvas2 = Canvas(contScatter, background='white')
    fig2 = matplotlib.pyplot.figure(facecolor="white")
    matplotlib.pyplot.plot()
    matplotlib.pyplot.title("2D Scatter Plot")
    canvas = FigureCanvasTkAgg(fig2, canvas2)
    canvas.get_tk_widget().pack(fill=X, expand=1)
    canvas2.pack(side=TOP, expand=1, fill=BOTH)
    contChoose = Frame(cont)
    contChoose.pack(side=TOP,fill=X)
    labelChoose = Label(contChoose, text="Select variables for 2D scatter plot")
    labelChoose.pack(side=LEFT)
    var2d1 = StringVar()
    var2d1.set(labels[0])
    drop1 = OptionMenu(contChoose, var2d1, *labels)
    drop1.pack(side=LEFT)
    var2d2 = StringVar()
    var2d2.set(labels[1])
    drop2 = OptionMenu(contChoose, var2d2, *labels)
    drop2.pack(side=LEFT)
    drawB = Button(contChoose)
    drawB.configure(text="Go", command= lambda: draw_2d(contScatter,norm, labels.index(var2d1.get()), labels.index(var2d2.get()), numbercl, exp, GT))
    drawB.pack(side=LEFT)
   
def scatters_3d(norm, cont, numbercl, exp, GT):
    #try:
    labels = list(obj.dataset)
    for item in cont.pack_slaves():
        item.destroy()
    contScatter = Frame(cont)
    contScatter.pack(side=TOP,fill=BOTH, expand=1)
    canvas1 = Canvas(contScatter, background='white')
    figure = Figure(figsize=(6,6), dpi=100, facecolor="white")
    canvas = FigureCanvasTkAgg(figure, canvas1)
    canvas.get_tk_widget().pack(fill=X, expand=1)
    axes = figure.gca(projection='3d')
    axes.set_xlim((0.0, 1.0))
    axes.set_ylim((0.0, 1.0))
    axes.set_zlim((0.0, 1.0))
    axes.set_xlabel('X')
    axes.set_ylabel('Y')
    axes.set_zlabel('Z')
    axes.set_xticks(np.arange(0.0,1.0,0.1))
    axes.set_yticks(np.arange(0.0,1.0,0.1))
    axes.set_zticks(np.arange(0.0,1.0,0.1))
    axes.tick_params(labelsize=9)
    axes.set_title("3D Scatter Plot")
    #plt.title("3D Scatter Plot")
    canvas1.pack(side=TOP, expand=1, fill=BOTH)
    contChoose = Frame(cont)
    contChoose.pack(side=TOP,fill=X)
    labelChoose = Label(contChoose, text="Select variables for 3D scatter plot")
    labelChoose.pack(side=LEFT)
    var2d1 = StringVar()
    var2d1.set(labels[0])
    drop1 = OptionMenu(contChoose, var2d1, *labels)
    drop1.pack(side=LEFT)
    var2d2 = StringVar()
    var2d2.set(labels[1])
    drop2 = OptionMenu(contChoose, var2d2, *labels)
    drop2.pack(side=LEFT)
    var2d3 = StringVar()
    var2d3.set(labels[2])
    drop3 = OptionMenu(contChoose, var2d3, *labels)
    drop3.pack(side=LEFT)
    drawB = Button(contChoose)
    drawB.configure(text="Go", command= lambda: draw_3d(contScatter, norm, labels.index(var2d1.get()), labels.index(var2d2.get()), labels.index(var2d3.get()), numbercl, exp, GT))
    drawB.pack(side=LEFT)
    #except ValueError:
    #    deconstruct(window, ls)
    
    
def scatters_2d3d(window, list_slaves, norm=False, numbercl=0, exp="All", GT=False):
    if len(window.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    contAll = Frame(window)
    contAll.pack(fill=BOTH, expand=1)
    contS2d = Frame(contAll, background='white')
    contSpace = Frame(contAll, width=10, background='white')
    contS3d = Frame(contAll, background='white')
    contS2d.pack(side=LEFT, fill=BOTH, expand=1)
    contSpace.pack(side=LEFT, fill=Y)
    contS3d.pack(side=RIGHT, fill=BOTH, expand=1)
    scatters_2d(norm, contS2d, numbercl, exp, GT)
    scatters_3d(norm, contS3d, numbercl, exp, GT)

def model_h(window, list_slaves, norm=False, numbercl=0, exp="All", GT=False):
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    if len(window.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    contH = Frame(window)
    contH.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(contH, background='white')
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    if obj.pathS != "/":
        fig = obj.heat_clust(norm, numbercl, exp, GT)
    else:
        fig = obj.heat_ds(norm, exp)
    if fig == 0:
        ls.__exit__(None,None,None)
        messagebox.showwarning("Invalid choice", "No points correspond to selected model + experiment")
        return
    canvas = FigureCanvasTkAgg(fig, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    #canvas.draw()
    tool = NavigationToolbar2Tk(canvas, contH)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    obj.add_subplot_zoom(canvas)
    ls.__exit__(None,None,None)
    
def model_h_ds(window, list_slaves, norm=False, exp="All"):
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    if len(window.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    contH = Frame(window)
    contH.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(contH, background='white')
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    fig = obj.heat_ds(norm, exp)
    canvas = FigureCanvasTkAgg(fig, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    #canvas.draw()
    tool = NavigationToolbar2Tk(canvas, contH)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    obj.add_subplot_zoom(canvas)
    ls.__exit__(None,None,None)

def model_p(window, list_slaves, norm=False, means=0, numbercl=0):
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    if len(window.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    contH = Frame(window)
    contH.pack(fill=BOTH, expand=1)
    contB = Frame(contH)
    contB.pack(side=BOTTOM, fill=X)
    my_canvas = Canvas(contH, background='white')
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    fig = obj.model_parameters(means, norm, numbercl)
    canvas = FigureCanvasTkAgg(fig, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    #canvas.draw()
    tool = NavigationToolbar2Tk(canvas, contH)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    obj.add_subplot_zoom(canvas)
    #df, latitude, longitude, experiment = graph.get_dataset(pathD, pathS, False)
    vs = list(obj.dataset)
    if len(vs) > 10:
        usedV = [1 for i in range(0,10)]
    else:
        usedV = [1 for i in vs]
    mplcursors.cursor().connect("add", lambda sel: sel.annotation.set_text(str(vs[math.ceil(list(sel.target)[1]-0.5)])+" "+str(sel.artist.get_array()[list(sel.target.index)[0],list(sel.target.index)[1]])))
    report = Button(contB, text="Generate Model Figures", command= lambda:  create_images(window, pathD, pathS, "", norm, usedV))
    report.pack()
    ls.__exit__(None,None,None)

def highlight_model_p(window, list_slaves, norm=False, means=0, numbercl=0):
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    locale.setlocale(locale.LC_NUMERIC, 'C')
    if len(window.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    gi, mp = obj.highlight_model_p(means, norm, numbercl)
    f = Frame(window)
    f.pack(fill=BOTH, expand=1)
    fTOP = Frame(f)
    fTOP.pack(side=TOP, fill=BOTH, expand=1)
    f1 = Frame(fTOP)
    f1.pack(side=LEFT, fill=BOTH,expand=1)
    f2 = Canvas(fTOP, background='white')
    f2.pack(side=LEFT, fill=BOTH,expand=1)
    #df = TableModel.getSampleData()
    pt = Table(f1, dataframe=gi)
    pt2 = Table(f2, dataframe=mp)
    f3 = Frame(f)
    f3.pack(side=BOTTOM, fill=X)
    #df, latitude, longitude, experiment = graph.get_dataset(pathD, pathS, False)
    vs = list(obj.dataset)
    if len(vs) > 10:
        usedV = [1 for i in range(0,10)]
    else:
        usedV = [1 for i in vs]
    report = Button(f3, text="Generate Model Figures", command= lambda: create_images(window, pathD, pathS, "", norm, usedV, numbercl))
    report.pack()
    pt.show()    
    pt2.show()
    ls.__exit__(None,None,None)
    
def model_p_2(window, list_slaves, norm=False, means=0, numbercl=0):
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    if len(window.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    contH = Frame(window)
    contH.pack(fill=BOTH, expand=1)
    contB = Frame(contH)
    contB.pack(side=BOTTOM, fill=X)
    my_canvas = Canvas(contH, background='white')
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    fig = obj.model_parameters2(means, norm, numbercl)
    canvas = FigureCanvasTkAgg(fig, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    #canvas.draw()
    tool = NavigationToolbar2Tk(canvas, contH)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    obj.add_subplot_zoom(canvas)
    vs = list(obj.dataset)
    if len(vs) > 10:
        usedV = [1 for i in range(0,10)]
    else:
        usedV = [1 for i in vs]
    labels = list(obj.dataset)
    comb_labels = list(itertools.combinations(labels, 2))
    mplcursors.cursor(canvas.figure.axes[0]).connect("add", lambda sel: sel.annotation.set_text(str(comb_labels[math.ceil(list(sel.target)[1]-0.5)])+" "+str(sel.artist.get_array()[list(sel.target.index)[0],list(sel.target.index)[1]])))
    if len(canvas.figure.axes) > 1:
        mplcursors.cursor(canvas.figure.axes[1])
    report = Button(contB, text="Generate Model Figures", command= lambda:  create_images(window, pathD, pathS, "", norm, usedV))
    report.pack()
    ls.__exit__(None,None,None)
    
def dim_red(window, list_slaves, norm=False, numbercl=0):
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    if len(window.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    contH = Frame(window)
    contH.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(contH, background='white')
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    fig = obj.tsne(norm, numbercl)
    canvas = FigureCanvasTkAgg(fig, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    tool = NavigationToolbar2Tk(canvas, contH)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    obj.add_subplot_zoom(canvas)
    for ax in canvas.figure.axes:
        zoomer.add_ax(ax, ['size'])
    ls.__exit__(None,None,None)

def create_images(window, pathD, pathS, pathGT, norm, usedV, numbercl=0):
    """
    ls = Splash(window, "IMG/hg.gif")
    ls.__enter__()
    directory = pathS+"images"
    if not os.path.exists(directory):
        os.makedirs(directory)
    df, latitude, longitude, experiments = graph.get_dataset(pathD, pathS, norm)
    if len(set(experiments)) > 6:
        exps = [1 for i in range(0,6)]
    else:
        exps = [1 for i in set(experiments)]
    if numbercl != 0:
        print("[XM]> Generating images for model {}".format(numbercl))
        figs = [graph.highlight_cluster(pathD, pathS, pathGT, norm, numbercl, usedV, "All"), graph.highlight_barplot(pathD, pathS, pathGT, norm, numbercl, usedV, "All")[0], graph.ordina_boxplot(means, pathD, pathS, pathGT, norm, numbercl, usedV, "All")[0], graph.heat_clust(pathD, pathS, pathGT, norm, numbercl, "All")]
        if norm == False:
            names_fig = [str(numbercl)+"_r_timeseries.png", str(numbercl)+"_r_barplots.png", str(numbercl)+"_r_boxplots.png", str(numbercl)+"_r_heatmap.png"]
        else:
            names_fig = [str(numbercl)+"_s_timeseries.png", str(numbercl)+"_s_barplots.png", str(numbercl)+"_s_boxplots.png", str(numbercl)+"_s_heatmap.png"]
        if len(latitude) != 0 and len(experiments) != 0:
            figs.append(graph.geo_localization(pathD, pathS, exps, numbercl, "All"))
            if norm == False:
                names_fig.append(str(numbercl)+"_r_geo.png")
            else:
                names_fig.append(str(numbercl)+"_s_geo.png")
        try:
            filetsne = open(pathS+"tsne.csv", 'r')
            filetsne.close()
            figs.append(graph.tsne(pathD, pathS, norm, numbercl))
            if norm == False:
                names_fig.append(str(numbercl)+"_r_tsne.png")
            else:
                names_fig.append(str(numbercl)+"_s_tsne.png")
        except:
            pass
        i = 0
        scrW = window.winfo_screenwidth()
        scrH = window.winfo_screenheight()
        for fig in figs:
            fig.set_size_inches(scrW/fig.get_dpi(), scrH/fig.get_dpi())
            fig.savefig(directory+"/"+names_fig[i], bbox_inches='tight')
            i += 1
            matplotlib.pyplot.close(fig)
            fig = None
            gc.collect()
        gi, mp = graph.highlight_model_p(means, pathD, pathS, norm, numbercl)
        mp = mp.to_string()
        if norm == False:
            table = open(directory+"/"+str(numbercl)+"_r_modelp.txt", 'w')
        else:
            table = open(directory+"/"+str(numbercl)+"_s_modelp.txt", 'w')
        table.write("{}".format(mp))
        table.close()
    else:
        print("[XM]> Generating images for all_model")
        figs = [graph.disegna_grafici(pathD, pathS, pathGT, norm, usedV, "All"), graph.disegna_barplot(pathD, pathS, pathGT, norm, usedV, "All"), graph.disegna_boxplot(means, pathD, pathS, pathGT, norm, usedV, "All"), graph.heat_clust(pathD, pathS, pathGT, norm, numbercl, "All"), graph.model_parameters(means, pathD, pathS, norm)]
        if norm == False:
            names_fig = ["all_r_timeseries.png", "all_r_barplots.png", "all_r_boxplots.png", "all_r_heatmap.png", "all_r_modelp.png"]
        else:
            names_fig = ["all_s_timeseries.png", "all_s_barplots.png", "all_s_boxplots.png", "all_s_heatmap.png", "all_s_modelp.png"]
        if len(latitude) != 0 and len(experiments) != 0:
            figs.append(graph.geo_localization(pathD, pathS, exps, 0, "All"))
            if norm == False:
                names_fig.append("all_r_geo.png")
            else:
                names_fig.append("all_s_geo.png")
        try:
            filetsne = open(pathS+"tsne.csv", 'r')
            filetsne.close()
            figs.append(graph.tsne(pathD, pathS, norm))
            if norm == False:
                names_fig.append("all_r_tsne.png")
            else:
                names_fig.append("all_s_tsne.png")
        except:
            pass
        i = 0
        scrW = window.winfo_screenwidth()
        scrH = window.winfo_screenheight()
        for fig in figs:
            fig.set_size_inches(scrW/fig.get_dpi(), scrH/fig.get_dpi())
            fig.savefig(directory+"/"+names_fig[i], bbox_inches='tight')
            i += 1
            matplotlib.pyplot.close(fig)
            fig = None
            gc.collect()
        dfEle, gi = graph.general_info(pathD, pathS, norm)
        dfEle = dfEle.to_string()
        fileDF = open(directory+"/"+"all_generalInfo.txt", 'w')
        fileDF.write("{}".format(dfEle))
        fileDF.close()
        for i in range(1, nc+1):
            print("[XM]> Generating images for model {}".format(i)+"/{}".format(nc))
            figs = [graph.highlight_cluster(pathD, pathS, pathGT, norm, i, usedV, "All"), graph.highlight_barplot(pathD, pathS, pathGT, norm, i, usedV, "All")[0], graph.ordina_boxplot(means, pathD, pathS, pathGT, norm, i, usedV, "All")[0], graph.heat_clust(pathD, pathS, pathGT, norm, i, "All")]
            if norm == False:
                names_fig = [str(i)+"_r_timeseries.png", str(i)+"_r_barplots.png", str(i)+"_r_boxplots.png", str(i)+"_r_heatmap.png"]
            else:
                names_fig = [str(i)+"_s_timeseries.png", str(i)+"_s_barplots.png", str(i)+"_s_boxplots.png", str(i)+"_s_heatmap.png"]
            if len(latitude) != 0 and len(experiments) != 0:
                figs.append(graph.geo_localization(pathD, pathS, exps, i, "All"))
                if norm == False:
                    names_fig.append(str(i)+"_r_geo.png")
                else:
                    names_fig.append(str(i)+"_s_geo.png")
            try:
                filetsne = open(pathS+"tsne.csv", 'r')
                filetsne.close()
                figs.append(graph.tsne(pathD, pathS, norm, i))
                if norm == False:
                    names_fig.append(str(i)+"_r_tsne.png")
                else:
                    names_fig.append(str(i)+"_s_tsne.png")
            except:
                pass
            j = 0
            scrW = window.winfo_screenwidth()
            scrH = window.winfo_screenheight()
            for fig in figs:
                fig.set_size_inches(scrW/fig.get_dpi(), scrH/fig.get_dpi())
                fig.savefig(directory+"/"+names_fig[j], bbox_inches='tight')
                j += 1 
                matplotlib.pyplot.close(fig)
                fig = None
                gc.collect()
            gi, mp = graph.highlight_model_p(means, pathD, pathS, norm, i)
            mp = mp.to_string()
            if norm == False:
                table = open(directory+"/"+str(i)+"_r_modelp.txt", 'w')
            else:
                table = open(directory+"/"+str(i)+"_s_modelp.txt", 'w')
            table.write("{}".format(mp))
            table.close()
    ls.__exit__(None,None,None)
    print("[XM]> End of images generation")
    messagebox.showinfo("End of generation", "You can find the images in "+directory)
    """  

"""
def view_dictionary(window, list_slaves):    
    list_slaves[2].destroy()
    f = Frame(window)
    f.pack(fill=BOTH, expand=1)
    f1 = Frame(f)
    f1.pack(side=LEFT, fill=BOTH,expand=1)
    f2 = Frame(f)
    df = pd.DataFrame()
    df["Words"] = dizionario
    df2 = pd.DataFrame()
    df2["Used"] = [None]
    pt = Table(f1, dataframe=df)
    pt2 = Table(f2, dataframe=df2)
    pt.show()    
    vertical = Frame(f)
    sub = Button(vertical)
    sub.configure(text=">", command= lambda : subW(pt, pt2, df2, f2))
    vertical.pack(side=LEFT, fill=Y)
    f2.pack(side=LEFT, fill=BOTH,expand=1)
    sub.pack()
    pt2.show()
    
def subW(pt, pt2, df2, f2):   
    rowSel = pt.getSelectedRow()
    #colSel = pt.get_col_clicked()
    word = dizionario[rowSel]
    arr = [item for item in df2.values if item != None]
    if word not in arr:
        arr.append(word)
    df2 = pd.DataFrame()
    df2["Used"] = arr
    pt2 = Table(f2, dataframe=df2)
    pt2.show()
"""
    
def openResults(window, text): 
    global pathS
    pathS = filedialog.askdirectory(title = "Select directory of Results")
    text.delete('1.0', END)
    text.insert(INSERT, pathS)
    #do_nc(pathS+"/")
    window.lift()
    
def openDataset(window, text):
    global pathD
    pathD = filedialog.askopenfilename(initialdir = "/home/whitebreeze/Tirocinio/InCatch/DATASETS",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*")))
    text.delete('1.0', END)
    text.insert(INSERT, pathD)
    window.lift()

def openGroundTruth(window, text):
    global pathGT
    pathGT = filedialog.askopenfilename(initialdir = "/home/whitebreeze/Tirocinio/InCatch/DATASETS",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*")))
    text.delete('1.0', END)
    text.insert(INSERT, pathGT)
    window.lift()

def make_welcome(window, cont):
    if len(cont.grid_slaves()) > 0:
        for item in cont.grid_slaves():
            item.destroy() 
    contW = Frame(cont)
    contW.grid(sticky="WENS")
    #path = os.path.abspath("XM.pgm")
    #ico = tkinter.PhotoImage(master=contW, file="XM.pgm")
    #labelIco = Label(contW, image = ico)
    #labelIco.image = ico
    #labelIco.pack(side=LEFT)
    """
    openB = Button(contW)
    openB.configure(text="Open cluster results", command= lambda: continueO(window, contW, cont))
    computeB = Button(contW)
    computeB.configure(text="Create new clustering", command= lambda: continueC(window, contW, cont))
    openB.grid(sticky="WE")
    computeB.grid(sticky="WE")
    """
    continueO(window, contW, cont)
    window.update()
    
def continueO(window, contW, cont):
    for item in contW.grid_slaves():
        item.destroy()
    backB = Button(contW)
    backB.configure(text="Back", command= lambda: make_welcome(window, cont))
    backB.grid(row=0,column=0,sticky="NS")
    frameO = Frame(contW)
    frameO.grid(row=0,column=1,sticky="E")
    """
    frameOpen = Frame(frameO)
    frameOpen.grid(row=0,column)
    frameRes = Frame(frameO)
    frameRes.pack(side=TOP)
    frameGT = Frame(frameO)
    frameOpen.pack(side=TOP)
    frameGT.pack(side=TOP)
    """
    textOpen = Text(frameO, height=1)
    textOpen.grid(row=0,column=1)
    textRes = Text(frameO, height=1)
    textRes.grid(row=1,column=1)
    textGT = Text(frameO, height=1)
    textGT.grid(row=2,column=1)
    openData = Button(frameO, text='Open Dataset', command=lambda : openDataset(window, textOpen))
    openGT = Button(frameO, text='Open Ground Truth', command=lambda : openGroundTruth(window, textGT))
    openRes = Button(frameO, text='Open Results', command=lambda : openResults(window, textRes))
    openData.grid(row=0,column=0,sticky="E")
    openRes.grid(row=1,column=0,sticky="E")
    openGT.grid(row=2,column=0,sticky="E")
    goButton = Button(frameO)
    goButton.configure(text="LOAD", command= lambda: on_load(window, window.pack_slaves(), str(textOpen.get("1.0","end-1c")), str(textRes.get("1.0","end-1c"))+"/", str(textGT.get("1.0","end-1c"))))
    goButton.grid(row=4,columnspan=2)
    window.update()
    
def continueC(window, contW, cont):
    if platform.system() != 'Linux':
        return
    for item in contW.grid_slaves():
        item.destroy()
    backB = Button(contW)
    backB.configure(text="Back", command= lambda: make_welcome(window, cont))
    #backB.pack(side=LEFT, fill=BOTH, expand=1)
    backB.grid(row=0,column=0, sticky="NS")
    contM = Frame(contW)
    #contM.pack(fill=BOTH, expand=1)
    contM.grid(row=0, column=1)
    varM = StringVar()
    radioSCM = Radiobutton(contM, text="SubCMedians", variable=varM, value="SCM")
    #radioSCM.pack(side=TOP)
    radioSCM.grid(sticky="W")
    radioSCM.deselect()
    radioTSNE = Radiobutton(contM, text="t-SNE", variable=varM, value="TSNE")
    #radioTSNE.pack(side=TOP)
    radioTSNE.grid(sticky="W")
    radioTSNE.deselect()
    radioKM = Radiobutton(contM, text="K-Means", variable=varM, value="KM")
    #radioKM.pack(side=TOP)
    radioKM.grid(sticky="W")
    radioKM.deselect()
    radioGMM = Radiobutton(contM, text="GMM", variable=varM, value="GMM")
    #radioGMM.pack(side=TOP)
    radioGMM.grid(sticky="W")
    radioGMM.deselect()
    radioSPC = Radiobutton(contM, text="Spectral Clustering", variable=varM, value="SPC")
    #radioGMM.pack(side=TOP)
    radioSPC.grid(sticky="W")
    radioSPC.deselect()
    contCB = Button(contM)
    contCB.configure(text="Continue", command= lambda: finishC(window, contW, cont, varM.get()))
    #contCB.pack(fill=BOTH, expand=1)
    contCB.grid()
    window.update()
    
def finishC(window, contW, cont, method):
    if method == "":
        messagebox.showwarning("No Method Selected", "Choose a method before continuing")
        return
    for item in contW.grid_slaves():
        item.destroy()
    backB = Button(contW)
    backB.configure(text="Back", command= lambda: continueC(window, contW, cont))
    backB.grid(row=0,column=0, sticky="NS")
    contF = Frame(contW)
    contF.grid(row=0, column=1, sticky="WENS")
    if method == "SCM":
        gid.SCM_GUI(contF, cont, window)
    if method == "TSNE":
        gid.TSNE_GUI(contF, cont, window)
    if method == "KM":
        gid.KMEANS_GUI(contF, cont, window)
    if method == "GMM":
        gid.GMM_GUI(contF, cont, window)
    if method == "SPC":
        gid.SPECTRAL_GUI(contF, cont, window)
    window.update()
   
def helpL(cont):
    for item in cont.pack_slaves():
        item.destroy()
    l = Listbox(cont, height=5)
    l.pack(side=LEFT, fill=BOTH, expand=1)
    s = ttk.Scrollbar(cont, orient=VERTICAL, command=l.yview)
    s.pack(side=LEFT, fill=Y)
    l['yscrollcommand'] = s.set
    ttk.Sizegrip().pack(fill=BOTH)
    #popup.grid_columnconfigure(0, weight=1)
    #popup.grid_rowconfigure(0, weight=1)
    file = open("DOC/libraries.txt", "r")
    for line in file:
        text = line.split("\n")
        l.insert(END, str(text[0]))
 
def close_up():
    for i in matplotlib.pyplot.get_fignums():
        matplotlib.pyplot.close(matplotlib.pyplot.figure(i))
    window.destroy()
    
def build_up():
    try:
        global window
        #dizionario = ["Acqua", "Non acqua", "Con Corrente", "Contro Corrente", "Anomalia"]
        actualPath = Path().absolute()
        window = Tk()
        window.title("XM_v2.1")
        window.wm_iconbitmap("@"+str(actualPath)+"/IMG/XM_icon.xbm")
        cont = Frame(window)
        cont.pack(side=TOP, expand=1, fill=BOTH)
        #my_canvas = Canvas(window)
        #my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        sidebar = Frame(window)
        sidebar.pack(side=TOP, fill=X)
        global var
        global varD
        global varG
        global varGT
        global varS
        global varDN
        global varExp
        global optionsG
        global optionsD
        global optionsGT
        global optionsO
        global optionsDN
        global optionsExp
        global optionsDa
        var = StringVar(sidebar)
        varD = StringVar(sidebar)
        varG = StringVar(sidebar)
        varGT = StringVar(sidebar)
        varDN = StringVar(sidebar)
        varExp = StringVar(sidebar)
        optionsDa = ["Dataset"]
        optionsG = ["General Info", "Model Parameters", "Heatmap clustering", "Heatmap dataset", "Time Series", "2D/3D Scatters", "BoxPlot", "BarPlot", "Geo-localization", "Dimensionality Reduction"]
        optionsD = ["Time Series", "2D/3D Scatters", "BoxPlot", "BarPlot", "Heatmap", "Geo-localization"]
        optionsGT = ["Modeling", "Ground Truth"]
        varS = StringVar(sidebar)
        optionsO = ["Symmetrical Uncertainty"]
        optionsDN = ["Real", "Normalized"]
        make_welcome(window, cont)
        finW = window.winfo_reqwidth()
        finH = window.winfo_reqheight()
        scrW = window.winfo_screenwidth()
        scrH = window.winfo_screenheight()
        Xpos = (scrW - finW) // 2
        Ypos = (scrH - finH) // 2
        window.geometry('+{}+{}'.format(Xpos, Ypos))
        window.protocol("WM_DELETE_WINDOW", close_up)
        window.mainloop()
    except:
        print(sys.exc_info())
        window.destroy()
        error = Tk()
        error.title("CRASH")
        contB = Frame(error)
        contB.pack(fill=BOTH, expand=1)
        showL = Button(contB, text="Show help", command= lambda: helpL(contB))
        showL.pack()
        error.mainloop()
    
    
    
if __name__ == "__main__":
    try:
        #dizionario = ["Acqua", "Non acqua", "Con Corrente", "Contro Corrente", "Anomalia"]
        actualPath = Path().absolute()
        window = Tk()
        window.style = Style()
        window.style.theme_use('clam')
        window.title("XM_v2.1")
        window.wm_iconbitmap("@"+str(actualPath)+"/IMG/XM_icon.xbm")
        cont = Frame(window)
        cont.pack(side=TOP, expand=1, fill=BOTH)
        #my_canvas = Canvas(window)
        #my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        sidebar = Frame(window)
        sidebar.pack(side=TOP, fill=X)
        global var
        global varD
        global varG
        global varGT
        global varDN
        global optionsG
        global optionsD
        global optionsGT
        global optionsO
        global optionsDN
        global optionsExp
        var = StringVar(sidebar)
        varD = StringVar(sidebar)
        varG = StringVar(sidebar)
        varGT = StringVar(sidebar)
        varDN = StringVar(sidebar)
        varExp = StringVar(sidebar)
        optionsDa = ["Dataset"]
        optionsG = ["General Info", "Model Parameters", "Heatmap clustering", "Heatmap dataset", "Time Series", "2D/3D Scatters", "BoxPlot", "BarPlot", "Geo-localization", "Dimensionality Reduction"]
        optionsD = ["Time Series", "2D/3D Scatters", "BoxPlot", "BarPlot", "Heatmap", "Geo-localization"]
        optionsGT = ["Modeling", "Ground Truth"]
        varS = StringVar(sidebar)
        optionsO = ["Symmetrical Uncertainty"]
        optionsDN = ["Real", "Normalized"]
        make_welcome(window, cont)
        finW = window.winfo_reqwidth()
        finH = window.winfo_reqheight()
        scrW = window.winfo_screenwidth()
        scrH = window.winfo_screenheight()
        Xpos = (scrW - finW) // 2
        Ypos = (scrH - finH) // 2
        window.geometry('+{}+{}'.format(Xpos, Ypos))
        window.protocol("WM_DELETE_WINDOW", close_up)
        window.mainloop()
    except:
        print(sys.exc_info())
        window.destroy()
        error = Tk()
        error.title("CRASH")
        contB = Frame(error)
        contB.pack(fill=BOTH, expand=1)
        showL = Button(contB, text="Show help", command= lambda: helpL(contB))
        showL.pack()
        error.mainloop()

