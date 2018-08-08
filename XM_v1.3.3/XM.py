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

import sys
from PIL import ImageTk
import PIL.Image
import matplotlib.pyplot as plt
import locale
import pandas as pd
import numpy as np
from Tkinter import *
import ttk
import Tkinter, Tkconstants, tkFileDialog
import matplotlib
import Grafici as graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import platform
if platform.system() == 'Linux':
    import GUI_inserimento_dati as gid
from pandastable import Table, TableModel
import tkMessageBox
from CheckBar import Checkbar
from LoadingScreen import Splash
from VSF import VerticalScrolledFrame
import os
import matplotlib.pylab as pl
import matplotlib.patches as mpatches
import colorsys
#from HSF import HorizontalScrolledFrame as HSF

global percorsoD
global percorsoS
global percorsoG
global gt
global var


def handler():
    if (varD.get()=="Dataset") and (varG.get()=="Time Series"):
        draw_graph(finestra, finestra.pack_slaves(), percorsoD, "/")
        return 
    if (varD.get()=="Dataset") and (varG.get()=="2D/3D Scatters"):
        scatters_2d3d(finestra, finestra.pack_slaves(), percorsoD, "/")
        return
    if (varD.get()=="Dataset") and (varG.get()=="BoxPlot"):
        create_boxplot(finestra, finestra.pack_slaves(), percorsoD, "/")
        return 
    if (varD.get()=="Dataset") and (varG.get()=="BarPlot"):
        create_barplot(finestra, finestra.pack_slaves(), percorsoD, "/")
        return 
    if (varD.get()=="Dataset") and (varG.get()=="Heatmap"):
        model_h(finestra, finestra.pack_slaves(), percorsoD, "/")
        return 
    if (var.get()=="All") and (varG.get()=="Time Series"):
        if gt == False:
            if varDN.get() == "Normalized":
                draw_graph(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", True)
            else:
                draw_graph(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/")
        else:
            if varDN.get() == "Normalized":
                draw_graph(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, True)
            else:
                draw_graph(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG)            
        return
    if (var.get()!="All") and (varG.get()=="Time Series"):
        if gt == False:
            if varDN.get() == "Normalized":
                draw_highlight(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", True, int(var.get().split(" ")[0]))
            else:
                draw_highlight(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", False, int(var.get().split(" ")[0]))
        else:
            if varDN.get() == "Normalized":
                draw_highlight(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", True, int(var.get().split(" ")[0]), percorsoG)
            else:
                draw_highlight(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", int(var.get().split(" ")[0]), percorsoG)
        return
    if (var.get()=="All") and (varG.get()=="BoxPlot"):
        if gt == False:
            if varDN.get() == "Normalized":
                create_boxplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", True, means)
            else:
                create_boxplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", False, means)
        else:
            if varDN.get() == "Normalized":
                create_boxplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, True)
            else:
                create_boxplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, False)
        return
    if (var.get()!="All") and (varG.get()=="BoxPlot"):
        if gt == False:
            if varDN.get() == "Normalized":
                sort_boxplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", True, int(var.get().split(" ")[0]), means)
            else:
                sort_boxplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", False, int(var.get().split(" ")[0]), means)
        else:
            if varDN.get() == "Normalized":
                sort_boxplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, True, int(var.get().split(" ")[0]))
            else:
                sort_boxplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, False, int(var.get().split(" ")[0]))
        return
    if (var.get()=="All") and (varG.get()=="BarPlot"):
        if gt == False:
            if varDN.get() == "Normalized":
                create_barplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+'/', "", True)
            else:
                create_barplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+'/', "", False)
        else:
            if varDN.get() == "Normalized":
                create_barplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+'/', percorsoG, True)
            else:
                create_barplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+'/', percorsoG, False)
        return
    if (var.get()!="All") and (varG.get()=="BarPlot"):
        if gt == False:
            if varDN.get() == "Normalized":
                highlight_barplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+'/', "", True, int(var.get().split(" ")[0]))
            else:
                highlight_barplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+'/', "", False, int(var.get().split(" ")[0]))
        else:
            if varDN.get() == "Normalized":
                highlight_barplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+'/', percorsoG, True, int(var.get().split(" ")[0]))
            else:
                highlight_barplot(finestra, finestra.pack_slaves(), percorsoD, percorsoS+'/', percorsoG, False, int(var.get().split(" ")[0]))
        return
    if (var.get()=="All") and (varG.get()=="General Info"):
        create_general_info(means, finestra, finestra.pack_slaves(), percorsoD, percorsoS+'/')
        return
    if (var.get()!="All") and (varG.get()=="General Info"):
        var.set("All")
        create_general_info(means, finestra, finestra.pack_slaves(), percorsoD, percorsoS+'/')
        tkMessageBox.showwarning("Invalid choice", "In order to view tab 'General Info' Model: All must be selected")
        return
    if (var.get()=="All") and (varG.get()=="2D/3D Scatters"):
        if gt == False:
            if varDN.get() == "Normalized":
                scatters_2d3d(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", True)
            else:
                scatters_2d3d(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", False)
        else:
            if varDN.get() == "Normalized":
                scatters_2d3d(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, True)
            else:
                scatters_2d3d(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, False)
        return
    if (var.get()!="All") and (varG.get()=="2D/3D Scatters"):
        if gt == False:
            if varDN.get() == "Normalized":
                scatters_2d3d(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", True, int(var.get().split(" ")[0]))
            else:
                scatters_2d3d(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", False, int(var.get().split(" ")[0]))
        else:
            if varDN.get() == "Normalized":
                scatters_2d3d(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, True, int(var.get().split(" ")[0]))
            else:
                scatters_2d3d(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, False, int(var.get().split(" ")[0]))
        return
    if (var.get()=="All") and (varG.get()=="Model Parameters"):
        if varDN.get() == "Normalized":
            model_p(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", True, means)
        else:
            model_p(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", False, means)
        return
    if (var.get()!="All") and (varG.get()=="Model Parameters"):
        if varDN.get() == "Normalized":
            highlight_model_p(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", True, means, int(var.get().split(" ")[0]))
        else:
            highlight_model_p(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", False, means, int(var.get().split(" ")[0]))
        return
    if (var.get()=="All") and (varG.get()=="Heatmap clustering"):
        if gt == False:
            if varDN.get() == "Normalized":
                model_h(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", True)
            else:
                model_h(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", False)
        else:
            if varDN.get() == "Normalized":
                model_h(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, True)
            else:
                model_h(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, False)
        return
    if (var.get()!="All") and (varG.get()=="Heatmap clustering"):
        if gt == False:
            if varDN.get() == "Normalized":
                model_h(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", True, int(var.get().split(" ")[0]))
            else:
                model_h(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", False, int(var.get().split(" ")[0]))
        else:
            if varDN.get() == "Normalized":
                model_h(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, True, int(var.get().split(" ")[0]))
            else:
                model_h(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, False, int(var.get().split(" ")[0]))
        return
    if (var.get()=="All") and (varG.get()=="Heatmap dataset"):
        if gt == False:
            if varDN.get() == "Normalized":
                model_h_ds(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", True)
            else:
                model_h_ds(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", False)
        else:
            if varDN.get() == "Normalized":
                model_h_ds(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, True)
            else:
                model_h_ds(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, False)
        return
    if (var.get()!="All") and (varG.get()=="Heatmap dataset"):
        var.set("All")
        if gt == False:
            if varDN.get() == "Normalized":
                model_h_ds(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", True)
            else:
                model_h_ds(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", "", False)
        else:
            if varDN.get() == "Normalized":
                model_h_ds(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, True)
            else:
                model_h_ds(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", percorsoG, False)
        return 
    if (var.get()=="All") and (varG.get()=="Geo-localization"):   
        draw_geo(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/")
    if (var.get()!="All") and (varG.get()=="Geo-localization"):   
        draw_geo(finestra, finestra.pack_slaves(), percorsoD, percorsoS+"/", int(var.get().split(" ")[0]))

def crea(finestra):
    popup = Toplevel(finestra)
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

def first(nc, means, finestra, list_slaves, sidebar, percorsoD, percorsoS, percorsoG=""):
    if(len(sidebar.pack_slaves())>0):
        for item in sidebar.pack_slaves():
            item.destroy()
    if percorsoS != "/":
        options = ["All"]
        var.set(options[0])
        optionsApp = []
        for i in range(1, nc+1):
            optionsApp.append(str(i))
        #means = graph.silhouette(percorsoD, percorsoS)
        meansS = list(np.copy(means))
        clusternorm, clustergiusti, cl = graph.get_cl(percorsoS)
        df, latitude, longitude, experiment = graph.get_dataset(percorsoD, percorsoS, False)
        su = graph.compute_su(clusternorm, df)
        righe, colonne = df.shape
        #meansI = silhouette(percorsoD, percorsoS)
        meansB = np.copy(meansS)
        for i in range(0,colonne):
            pos = su.index(max(su))
            freq = [[] for x in clustergiusti]
            r = 0
            for c in clusternorm:
                freq[int(c)-1].append(df.iloc[r,pos])
                r = r+1
            means = list(np.copy(meansB))
            su[pos] = -1
        points = []
        for i in range(0, len(clustergiusti)):
            points.append(len(freq[i]))
        colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
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
            fileDN = open(percorsoS+"dataStandardization.csv", 'r')
            varDN.set(optionsDN[0])
            labelDN = Label(sidebar, text="Data: ")
            labelDN.pack(side=LEFT)
            dropDN = OptionMenu(sidebar, varDN, *optionsDN)
            dropDN.pack(side=LEFT)
        except:
            print
        start = Button(sidebar)
        start.configure(text="GO", command=handler)
        start.pack(side=LEFT)
        if percorsoG != "":
            #varGT.set(optionsGT[0])
            #varGT.trace("w", lambda: switch_fun(finestra, sidebar, percorsoD, percorsoS, percorsoG, False))
            #dropGT = OptionMenu(sidebar, varGT, *optionsGT)
            #dropGT.pack(side=LEFT)
            switch = Button(sidebar)
            switch.configure(text="Ground Truth", command= lambda: switch_fun(finestra, sidebar, percorsoD, percorsoS, percorsoG, True))
            switch.pack(side=LEFT)
        #return means
        
    else:
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
        start = Button(sidebar)
        start.configure(text="GO", command=handler)
        start.pack(side=LEFT)
    """
    diz = Button(sidebar)
    diz.configure(text="Dictionary", command= lambda : view_dictionary(finestra, finestra.pack_slaves()))
    diz.pack(side=LEFT)
    """  

def switch_fun(finestra, sidebar, percorsoD, percorsoS, percorsoG, which):
    for item in sidebar.pack_slaves():
        item.destroy()
    global gt
    if which == False:
        """global percorsoS
        percorsoS = percorsoSBack"""
        gt = False
        do_nc(percorsoS)
        create_general_info(finestra, finestra.pack_slaves(), percorsoD, percorsoS, percorsoG)
    else:
        gt = True
        do_nc(percorsoS, percorsoG)
        options = ["All"]
        var.set(options[0])
        for i in range(1, nc+1):
            options.append(str(i))
        clusternorm, clustergiusti, cl = graph.get_cl(percorsoS, percorsoG)
        colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
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
        optionsGT1 = [item for item in optionsG if item != "General Info" and item != "Model Parameters" and item != "Heatmap"]
        varG.set(optionsGT1[0])
        dropG = OptionMenu(sidebar, varG, *optionsGT1)
        dropG.pack(side=LEFT)
        varS.set(optionsO[0])
        labelS = Label(sidebar, text="Sorting: ")
        labelS.pack(side=LEFT)
        dropS = OptionMenu(sidebar, varS, *optionsO)
        dropS.pack(side=LEFT)
        #varGT.trace("w", lambda: switch_fun(finestra, sidebar, percorsoD, percorsoS, percorsoG, False))
        #dropGT = OptionMenu(sidebar, varGT, *optionsGT)
        #dropGT.pack(side=LEFT)
        start = Button(sidebar)
        start.configure(text="GO", command=handler)
        start.pack(side=LEFT)
        switch = Button(sidebar)
        switch.configure(text="Go to Results", command= lambda: switch_fun(finestra, sidebar, percorsoD, percorsoS, percorsoG, False))
        switch.pack(side=LEFT)
        draw_graph(finestra, finestra.pack_slaves(), percorsoD, percorsoS, percorsoG, False)
    
def openD(finestra, sidebar):    
    #global percorsoD
    #global percorsoS
    popup = Toplevel(finestra)
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
    goButton.configure(text="LOAD", command= lambda: on_load(finestra, finestra.pack_slaves(), str(textOpen.get("1.0","end-1c")), str(textRes.get("1.0","end-1c"))+"/", str(textGT.get("1.0","end-1c"))))
    goButton.pack(side=BOTTOM)
    popup.mainloop()
    do_nc(percorsoS+"/")
    
        
def do_nc(percorsoS, percorsoG=""):
    if percorsoG != "":
        clu = open(percorsoG,'r').readlines()
    else:
        clu = open(percorsoS+'/cl.txt','r').readlines()
    global nc 
    nc = len(set(clu))
    
def updateV(cb, fromF, contC, percorsoD, percorsoS, percorsoG, norm, finestra, numero=0):
    n = 0
    for i in list(cb.state()):
        if i == 1:
            n+=1
    if n > 10:
        tkMessageBox.showerror("Too many variables", "Choose 10 variables at max")
        return
    if n==0:
        tkMessageBox.showerror("Too few variables", "Choose at least 1 variable")
        return
    ls = Splash(finestra, "IMG/hg.gif")
    ls.__enter__()
    for item in contC.pack_slaves():
        item.destroy()
    if fromF == "DG":
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        if percorsoG != "":
            figura = graph.disegna_grafici(percorsoD, percorsoS, percorsoG, norm, cb.state())
        else:
            figura = graph.disegna_grafici(percorsoD, percorsoS, "", norm, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
    if fromF == "DB":
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        if percorsoG != "":
            figura = graph.disegna_boxplot(0, percorsoD, percorsoS, percorsoG, norm, cb.state())
        else:
            figura = graph.disegna_boxplot(means, percorsoD, percorsoS, "", norm, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
    if fromF == "DH":
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        if percorsoG != "":
            figura = graph.disegna_barplot(percorsoD, percorsoS, percorsoG, norm, cb.state())
        else:
            figura = graph.disegna_barplot(percorsoD, percorsoS, "", norm, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
    if fromF == "HG":
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        if percorsoG != "":
            figura = graph.highlight_cluster(percorsoD, percorsoS, percorsoG, norm, numero, cb.state())
        else:
            figura = graph.highlight_cluster(percorsoD, percorsoS, "", norm, numero, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
    if fromF == "HB":
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        if percorsoG != "":
            figura, punti, righe = graph.ordina_boxplot(0, percorsoD, percorsoS, percorsoG, norm, numero, cb.state())
        else:
            figura, punti, righe = graph.ordina_boxplot(means, percorsoD, percorsoS, "", norm, numero, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
        points = Label(contC, text="NbPoints: "+str(punti)+"/"+str(righe))
        points.pack(side = BOTTOM)
    if fromF == "HH":
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        if percorsoG != "":
            figura, punti, righe = graph.highlight_barplot(percorsoD, percorsoS, percorsoG, norm, numero, cb.state())
        else:
            figura, punti, righe = graph.highlight_barplot(percorsoD, percorsoS, "", norm, numero, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
        points = Label(contC, text="NbPoints: "+str(punti)+"/"+str(righe))
        points.pack(side = BOTTOM)
    if fromF == "GEO":
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        figura = graph.geo_localization(percorsoD, percorsoS, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
    if fromF == "GEOH":
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        figura = graph.geo_localization(percorsoD, percorsoS, cb.state(), numero)
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
    ls.__exit__(None, None, None)

def deconstruct(finestra, ls):
    for i in finestra.pack_slaves():
            i.destroy()
    sidebar = Frame(finestra)
    sidebar.pack(side=TOP, fill=X)
    cont = Frame(finestra)
    cont.pack(side=TOP, expand=1, fill=BOTH)
    var = StringVar(sidebar)
    varG = StringVar(sidebar)
    optionsG = ["Time Series", "BoxPlot", "BarPlot", "General Info"]
    varS = StringVar(sidebar)
    optionsO = ["Symmetrical Uncertainty"]
    make_welcome(finestra, cont)
    ls.__exit__(None, None, None)
    tkMessageBox.showerror("ERROR", "Dataset may contain non-numerical values or may not correspond to clustering results")
    finestra.update()

def support(finestra):
    popup = Toplevel(finestra)
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

def draw_graph(finestra, list_slaves, percorsoD, percorsoS, percorsoG="", norm=False):    
    #try:
        ls = Splash(finestra, "IMG/hg.gif")
        ls.__enter__()
        if len(finestra.pack_slaves())==2:
            finestra.pack_slaves()[0].destroy()
            finestra.pack_slaves()[0].destroy()
            contMenu = Frame(finestra)
            contMenu.pack()
            menu = Menu(contMenu)
            finestra.config(menu=menu)
            file = Menu(menu)
            file.add_command(label='Open Cluster Results', command = lambda: openD(finestra, sidebar))
            file.add_command(label='Create New Clustering', command = lambda: crea(finestra))
            file.add_command(label='?', command = lambda: support(finestra))
            menu.add_cascade(label='File', menu = file)
            sidebar = Frame(finestra)
            sidebar.pack(side=TOP, fill=X)
            first(nc, finestra, finestra.pack_slaves(), finestra.pack_slaves()[1], percorsoD, percorsoS, percorsoG)
            var.set(None)
        else: 
            if len(finestra.pack_slaves()) > 3:
                list_slaves[2].destroy()
                list_slaves[3].destroy()
            else:
                list_slaves[2].destroy()
        df, latitude, longitude, experiment = graph.get_dataset(percorsoD, percorsoS, norm)
        vs = list(df)
        if percorsoS != "/":
            do_nc(percorsoS)
            ordV = graph.sort_var(percorsoD, percorsoS, percorsoG)
        else:
            ordV = [item for item in range(0,len(vs))]
        contCB = Frame(finestra)
        contCB.pack(side=LEFT, fill=Y)
        labelV = Label(contCB, text="Variables")
        labelV.pack(side=TOP)
        sframe = VerticalScrolledFrame(contCB)
        sframe.pack(side=TOP)
        cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV)
        cb.pack()
        c = 0
        for chk in cb.chks:
            if c < 10:
                chk.select()
            c+=1
        contU = Frame(contCB)
        contU.pack(side=TOP)
        update = Button(contU)
        update.configure(text="Update", command= lambda: updateV(cb, "DG", contC, percorsoD, percorsoS, percorsoG, norm, finestra))
        update.pack(side=TOP)
        contC = Frame(finestra)
        contC.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        figura = graph.disegna_grafici(percorsoD, percorsoS, percorsoG, norm, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
        ls.__exit__(None, None, None)
        
    #except ValueError:
    #    deconstruct(finestra, ls)
        
        
def create_boxplot(finestra, list_slaves, percorsoD, percorsoS, percorsoG="", norm=False, means=0):   
    #try:
        ls = Splash(finestra, "IMG/hg.gif")
        ls.__enter__()
        if len(finestra.pack_slaves()) > 3:
            list_slaves[2].destroy()
            list_slaves[3].destroy()
        else:
            list_slaves[2].destroy()
        df, latitude, longitude, experiment = graph.get_dataset(percorsoD, percorsoS, norm)
        vs = list(df)
        if percorsoS != "/":
            ordV = graph.sort_var(percorsoD, percorsoS, percorsoG)
        else:
            ordV = [item for item in range(0,len(vs))]
        contCB = Frame(finestra)
        contCB.pack(side=LEFT, fill=Y)
        labelV = Label(contCB, text="Variables")
        labelV.pack(side=TOP)
        sframe = VerticalScrolledFrame(contCB)
        sframe.pack(side=TOP)
        cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV)
        cb.pack()
        c = 0
        for chk in cb.chks:
            if c < 10:
                chk.select()
            c+=1
        contU = Frame(contCB)
        contU.pack(side=TOP)
        update = Button(contU)
        update.configure(text="Update", command= lambda: updateV(cb, "DB", contC, percorsoD, percorsoS, percorsoG, norm, finestra))
        update.pack(side=TOP)
        contC = Frame(finestra)
        contC.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        figura = graph.disegna_boxplot(means, percorsoD, percorsoS, percorsoG, norm, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
        ls.__exit__(None, None, None)
    #except ValueError:
    #    deconstruct(finestra, ls)
    
def create_barplot(finestra, list_slaves, percorsoD, percorsoS, percorsoG="", norm=False): 
    try:
        
        ls = Splash(finestra, "IMG/hg.gif")
        ls.__enter__()
        if len(finestra.pack_slaves()) > 3:
            list_slaves[2].destroy()
            list_slaves[3].destroy()
        else:
            list_slaves[2].destroy()
        df, latitude, longitude, experiment = graph.get_dataset(percorsoD, percorsoS, norm)
        vs = list(df)
        if percorsoS != "/":
            ordV = graph.sort_var(percorsoD, percorsoS, percorsoG)
        else:
            ordV = [item for item in range(0,len(vs))]
        contCB = Frame(finestra)
        contCB.pack(side=LEFT, fill=Y)
        labelV = Label(contCB, text="Variables")
        labelV.pack(side=TOP)
        sframe = VerticalScrolledFrame(contCB)
        sframe.pack(side=TOP)
        cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV)
        cb.pack()
        c = 0
        for chk in cb.chks:
            if c < 10:
                chk.select()
            c+=1
        contU = Frame(contCB)
        contU.pack(side=TOP)
        update = Button(contU)
        update.configure(text="Update", command= lambda: updateV(cb, "DH", contC, percorsoD, percorsoS, percorsoG, norm, finestra))
        update.pack(side=TOP)
        contC = Frame(finestra)
        contC.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        figura = graph.disegna_barplot(percorsoD, percorsoS, percorsoG, norm, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
        ls.__exit__(None, None, None)
    except ValueError:
        deconstruct(finestra, ls)
    
def draw_highlight(finestra, list_slaves, percorsoD, percorsoS, norm, numero, percorsoG=""):  
    try:
        ls = Splash(finestra, "IMG/hg.gif")
        ls.__enter__()
        if len(finestra.pack_slaves()) > 3:
            list_slaves[2].destroy()
            list_slaves[3].destroy()
        else:
            list_slaves[2].destroy()
        df, latitude, longitude, experiment = graph.get_dataset(percorsoD, percorsoS, norm)
        vs = list(df)
        ordV = graph.sort_var(percorsoD, percorsoS, percorsoG, numero)
        contCB = Frame(finestra)
        contCB.pack(side=LEFT, fill=Y)
        labelV = Label(contCB, text="Variables")
        labelV.pack(side=TOP)
        sframe = VerticalScrolledFrame(contCB)
        sframe.pack(side=TOP)
        cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV)
        cb.pack()
        c = 0
        for chk in cb.chks:
            if c < 10:
                chk.select()
            c+=1
        contU = Frame(contCB)
        contU.pack(side=TOP)
        update = Button(contU)
        update.configure(text="Update", command= lambda: updateV(cb, "HG", contC, percorsoD, percorsoS, percorsoG, norm, finestra, numero))
        update.pack(side=TOP)
        contC = Frame(finestra)
        contC.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        figura = graph.highlight_cluster(percorsoD, percorsoS, percorsoG, norm, numero, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
        ls.__exit__(None, None, None)
    except ValueError:
        deconstruct(finestra, ls)

def highlight_barplot(finestra, list_slaves, percorsoD, percorsoS, percorsoG, norm, numero): 
    try:
        ls = Splash(finestra, "IMG/hg.gif")
        ls.__enter__()
        if len(finestra.pack_slaves()) > 3:
            list_slaves[2].destroy()
            list_slaves[3].destroy()
        else:
            list_slaves[2].destroy()
        df, latitude, longitude, experiment = graph.get_dataset(percorsoD, percorsoS, norm)
        vs = list(df)
        ordV = graph.sort_var(percorsoD, percorsoS, percorsoG, numero)
        contCB = Frame(finestra)
        contCB.pack(side=LEFT, fill=Y)
        labelV = Label(contCB, text="Variables")
        labelV.pack(side=TOP)
        sframe = VerticalScrolledFrame(contCB)
        sframe.pack(side=TOP)
        cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV)
        cb.pack()
        c = 0
        for chk in cb.chks:
            if c < 10:
                chk.select()
            c+=1
        contU = Frame(contCB)
        contU.pack(side=TOP)
        update = Button(contU)
        update.configure(text="Update", command= lambda: updateV(cb, "HH", contC, percorsoD, percorsoS, percorsoG, norm, finestra, numero))
        update.pack(side=TOP)
        contC = Frame(finestra)
        contC.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        figura, punti, righe = graph.highlight_barplot(percorsoD, percorsoS, percorsoG, norm, numero, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
        points = Label(contC, text="NbPoints: "+str(punti)+"/"+str(righe))
        points.pack(side = BOTTOM)
        ls.__exit__(None, None, None)
    except ValueError:
        deconstruct(finestra, ls)
    
def sort_boxplot(finestra, list_slaves, percorsoD, percorsoS, percorsoG, norm, numero, means=0): 
    try:
        ls = Splash(finestra, "IMG/hg.gif")
        ls.__enter__()
        if len(finestra.pack_slaves()) > 3:
            list_slaves[2].destroy()
            list_slaves[3].destroy()
        else:
            list_slaves[2].destroy()
        df, latitude, longitude, experiment = graph.get_dataset(percorsoD, percorsoS, norm)
        vs = list(df)
        ordV = graph.sort_var(percorsoD, percorsoS, percorsoG, numero)
        contCB = Frame(finestra)
        contCB.pack(side=LEFT, fill=Y)
        labelV = Label(contCB, text="Variables")
        labelV.pack(side=TOP)
        sframe = VerticalScrolledFrame(contCB)
        sframe.pack(side=TOP)
        cb = Checkbar(sframe.interior, vs, side=TOP, sort=ordV)
        cb.pack()
        c = 0
        for chk in cb.chks:
            if c < 10:
                chk.select()
            c+=1
        contU = Frame(contCB)
        contU.pack(side=TOP)
        update = Button(contU)
        update.configure(text="Update", command= lambda: updateV(cb, "HB", contC, percorsoD, percorsoS, percorsoG, norm, finestra, numero))
        update.pack(side=TOP)
        contC = Frame(finestra)
        contC.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(contC)
        my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        figura, punti, righe = graph.ordina_boxplot(means, percorsoD, percorsoS, percorsoG, norm, numero, cb.state())
        canvas = FigureCanvasTkAgg(figura, my_canvas)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        canvas.draw()
        tool = NavigationToolbar2TkAgg(canvas, contC)
        tool.update()
        canvas._tkcanvas.pack(fill=BOTH, expand=1)
        graph.add_subplot_zoom(canvas)
        points = Label(contC, text="NbPoints: "+str(punti)+"/"+str(righe))
        points.pack(side = BOTTOM)
        ls.__exit__(None, None, None)
    except ValueError:
        deconstruct(finestra, ls)
    
def secure(finestra, percorsoD):
    sure = Toplevel(finestra)
    cont = Frame(sure)
    cont.pack(side=TOP)
    contS = Frame(sure)
    contS.pack(side=BOTTOM)
    label = Label(cont)
    label.configure(text="No clustering selected.\nAre you sure to procede?", font=8)
    label.pack(side=TOP)
    yes = Button(contS, text="Yes", command= lambda: simple_data(sure, finestra, percorsoD))
    no = Button(contS, text="No", command= lambda: sure.destroy())
    yes.pack(side=LEFT)
    no.pack(side=RIGHT)
    sure.geometry('+{}+{}'.format(Xpos, Ypos))
    sure.mainloop()

def simple_data(sure, finestra, percorsoD):
    sure.destroy()
    for item in finestra.pack_slaves():
        item.destroy()
    contMenu = Frame(finestra)
    contMenu.pack()
    menu = Menu(contMenu)
    finestra.config(menu=menu)
    file = Menu(menu)
    file.add_command(label='Open Cluster Results', command = lambda: openD(finestra, sidebar))
    file.add_command(label='Create New Clustering', command = lambda: crea(finestra))
    file.add_command(label='?', command = lambda: support(finestra))
    menu.add_cascade(label='File', menu = file)
    sidebar = Frame(finestra)
    sidebar.pack(side=TOP, fill=X)
    global nc
    nc = 0
    first(nc, means, finestra, finestra.pack_slaves(), sidebar, percorsoD, "/")
    placeholder = Frame(finestra)
    placeholder.pack()
    draw_graph(finestra, finestra.pack_slaves(), percorsoD, "/", "", False)

def create_general_info(means, finestra, list_slaves, percorsoD, percorsoS, percorsoG="", norm=False):  
    global gt
    gt = False
    if percorsoD == "":
        tkMessageBox.showerror("No Dataset Selected","Please select a dataset")
        return
    if percorsoS == "/":
        secure(finestra, percorsoD)
        return
    #try:
    ls = Splash(finestra, "IMG/hg.gif")
    ls.__enter__()
    locale.setlocale(locale.LC_NUMERIC, 'C')
    do_nc(percorsoS)
    if len(finestra.pack_slaves())==2:
        finestra.pack_slaves()[0].destroy()
        finestra.pack_slaves()[0].destroy()
        contMenu = Frame(finestra)
        contMenu.pack()
        menu = Menu(contMenu)
        finestra.config(menu=menu)
        file = Menu(menu)
        file.add_command(label='Open Cluster Results', command = lambda: openD(finestra, sidebar))
        file.add_command(label='Create New Clustering', command = lambda: crea(finestra))
        file.add_command(label='?', command = lambda: support(finestra))
        menu.add_cascade(label='File', menu = file)
        sidebar = Frame(finestra)
        sidebar.pack(side=TOP, fill=X)
    else: 
        if len(finestra.pack_slaves()) > 3:
            list_slaves[2].destroy()
            list_slaves[3].destroy()
        else:
            list_slaves[2].destroy()
    #global means
    #means = graph.silhouette(percorsoD, percorsoS)
    first(nc, means, finestra, list_slaves, finestra.pack_slaves()[1], percorsoD, percorsoS, percorsoG)
    varD.set(None)
    df, general = graph.general_info(means, percorsoD, percorsoS, norm)
    f = Frame(finestra)
    f.pack(fill=BOTH, expand=1)
    f1 = Frame(f)
    f1.pack(side=LEFT, fill=BOTH,expand=1)
    f2 = Frame(f)
    f2.pack(side=LEFT, fill=BOTH,expand=1)
    #df = TableModel.getSampleData()
    pt = Table(f1, dataframe=df)
    pt2 = Table(f2, dataframe=general)
    pt.show()    
    pt2.show()   
    ls.__exit__(None, None, None)
    #except ValueError:
    #    deconstruct(finestra, ls)

def on_load(finestra, list_slaves, percorsoD, percorsoS, percorsoG="", norm=False):
    try:
        fileM = open(percorsoS+"generalInfo.csv", 'r')
        r = 0
        clS = []
        for lines in fileM:
            r +=1
            if r > 17:
                clS.append(lines)
        clS = [float(item) for item in clS]
        if r== 17:
            fileA = open(percorsoS+"generalInfo.csv", 'a')
            clS = graph.silhouette(percorsoD, percorsoS)
            for cl in clS:
                fileA.write("{0:.3f}".format(cl)+"\n")
        global means 
        means = clS
        create_general_info(means, finestra, list_slaves, percorsoD, percorsoS, percorsoG, norm)
    except:
        global means
        means = ""
        create_general_info(means, finestra, list_slaves, percorsoD, percorsoS, percorsoG, norm)
    
def draw_geo(finestra, list_slaves, percorsoD, percorsoS, numerocl=0):
    ls = Splash(finestra, "IMG/hg.gif")
    ls.__enter__()
    if len(finestra.pack_slaves()) == 2:
        finestra.pack_slaves()[0].destroy()
        finestra.pack_slaves()[0].destroy()
        contMenu = Frame(finestra)
        contMenu.pack()
        menu = Menu(contMenu)
        finestra.config(menu=menu)
        file = Menu(menu)
        file.add_command(label='Open Cluster Results', command = lambda: openD(finestra, sidebar))
        file.add_command(label='Create New Clustering', command = lambda: crea(finestra))
        file.add_command(label='?', command = lambda: support(finestra))
        menu.add_cascade(label='File', menu = file)
        sidebar = Frame(finestra)
        sidebar.pack(side=TOP, fill=X)
        first(nc, finestra, finestra.pack_slaves(), finestra.pack_slaves()[1], percorsoD, percorsoS, percorsoG)
        var.set(None)
    else: 
        if len(finestra.pack_slaves()) > 3:
            list_slaves[2].destroy()
            list_slaves[3].destroy()
        else:
            list_slaves[2].destroy()
    df, latitude, longitude, experiment = graph.get_dataset(percorsoD, percorsoS, False)
    if len(experiment)!=0:
        exps = list(pd.unique(experiment))
        sort= []
        for i in range(0, len(exps)):
            sort.append(i)
        contCB = Frame(finestra)
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
        if numerocl == 0:
            update.configure(text="Update", command= lambda: updateV(cb, "GEO", contC, percorsoD, percorsoS, "", False, finestra))
        else:
            update.configure(text="Update", command= lambda: updateV(cb, "GEOH", contC, percorsoD, percorsoS, "", False, finestra, numerocl))
        update.pack(side=TOP)
    contC = Frame(finestra)
    contC.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(contC)
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    try:
        figura = graph.geo_localization(percorsoD, percorsoS, cb.state(), numerocl)
    except:
        figura = graph.geo_localization(percorsoD, percorsoS, [1])
    canvas = FigureCanvasTkAgg(figura, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    canvas.draw()
    tool = NavigationToolbar2TkAgg(canvas, contC)
    tool.update()
    canvas._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
    graph.add_subplot_zoom(canvas)
    ls.__exit__(None, None, None)


def draw_2d(cont, percorsoD, percorsoS, percorsoG, norm, var1, var2, numerocl):
    ls = Splash(finestra, "IMG/hg.gif")
    ls.__enter__()
    for item in cont.pack_slaves():
        item.destroy()
    my_canvas = Canvas(cont)
    my_canvas.pack(side=BOTTOM,fill=BOTH, expand=1)
    figura = graph.scatter_2d(percorsoD, percorsoS, percorsoG, norm, var1, var2, numerocl)
    canvas = FigureCanvasTkAgg(figura, my_canvas)
    canvas.get_tk_widget().pack(fill=X, expand=1)
    canvas.draw()
    tool = NavigationToolbar2TkAgg(canvas, cont)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    ls.__exit__(None, None, None)
    
def draw_3d(cont, percorsoD, percorsoS, percorsoG, norm, var1, var2, var3, numerocl):
    ls = Splash(finestra, "IMG/hg.gif")
    ls.__enter__()
    for item in cont.pack_slaves():
        item.destroy()
    my_canvas = Canvas(cont)
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    figura = graph.scatter_3d(percorsoD, percorsoS, percorsoG, norm, var1, var2, var3, numerocl)
    canvas = FigureCanvasTkAgg(figura, my_canvas)
    canvas.get_tk_widget().pack(fill=X, expand=1)
    canvas.draw()
    tool = NavigationToolbar2TkAgg(canvas, cont)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    ls.__exit__(None, None, None)

def scatters_2d(percorsoD, percorsoS, percorsoG, norm, cont, numerocl):
    df, latitude, longitude, experiment = graph.get_dataset(percorsoD, percorsoS, norm)  
    labels = list(df)
    for item in cont.pack_slaves():
        item.destroy()
    contScatter = Frame(cont)
    contScatter.pack(side=TOP,fill=BOTH, expand=1)
    
    canvas2 = Canvas(contScatter)
    figura2 = plt.figure()
    plt.plot()
    plt.title("2D Scatter Plot")
    canvas = FigureCanvasTkAgg(figura2, canvas2)
    canvas.get_tk_widget().pack(fill=X, expand=1)
    canvas.draw()
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
    drawB.configure(text="Go", command= lambda: draw_2d(contScatter, percorsoD, percorsoS, percorsoG, norm, labels.index(var2d1.get()), labels.index(var2d2.get()), numerocl))
    drawB.pack(side=LEFT)
   
def scatters_3d(percorsoD, percorsoS, percorsoG, norm, cont, numerocl):
    try:
        df, latitude, longitude, experiment = graph.get_dataset(percorsoD, percorsoS, norm)  
        labels = list(df)
        for item in cont.pack_slaves():
            item.destroy()
        contScatter = Frame(cont)
        contScatter.pack(side=TOP,fill=BOTH, expand=1)
        canvas1 = Canvas(contScatter)
        figura = plt.figure()
        plt.plot()
        plt.title("3D Scatter Plot")
        canvas = FigureCanvasTkAgg(figura, canvas1)
        canvas.get_tk_widget().pack(fill=X, expand=1)
        canvas.draw()
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
        drawB.configure(text="Go", command= lambda: draw_3d(contScatter, percorsoD, percorsoS, percorsoG, norm, labels.index(var2d1.get()), labels.index(var2d2.get()), labels.index(var2d3.get()), numerocl))
        drawB.pack(side=LEFT)
        
    except ValueError:
        deconstruct(finestra, ls)
    
    
def scatters_2d3d(finestra, list_slaves, percorsoD, percorsoS, percorsoG="", norm=False, numerocl=0):
    if len(finestra.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    contAll = Frame(finestra)
    contAll.pack(fill=BOTH, expand=1)
    contS2d = Frame(contAll, background='white')
    contSpace = Frame(contAll, width=10, background='white')
    contS3d = Frame(contAll, background='white')
    contS2d.pack(side=LEFT, fill=BOTH, expand=1)
    contSpace.pack(side=LEFT, fill=Y)
    contS3d.pack(side=RIGHT, fill=BOTH, expand=1)
    scatters_2d(percorsoD, percorsoS, percorsoG, norm, contS2d, numerocl)
    scatters_3d(percorsoD, percorsoS, percorsoG, norm, contS3d, numerocl)

def model_h(finestra, list_slaves, percorsoD, percorsoS, percorsoG="", norm=False, numero=0):
    ls = Splash(finestra, "IMG/hg.gif")
    ls.__enter__()
    if len(finestra.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    contH = Frame(finestra)
    contH.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(contH)
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    if percorsoS != "/":
        figura = graph.heat_clust(percorsoD, percorsoS, percorsoG, norm, numero)
    else:
        figura = graph.heat_ds(percorsoD, percorsoS, norm)
    canvas = FigureCanvasTkAgg(figura, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    canvas.draw()
    tool = NavigationToolbar2TkAgg(canvas, contH)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    graph.add_subplot_zoom(canvas)
    ls.__exit__(None,None,None)
    
def model_h_ds(finestra, list_slaves, percorsoD, percorsoS, percorsoG="", norm=False, numero=0):
    ls = Splash(finestra, "IMG/hg.gif")
    ls.__enter__()
    if len(finestra.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    contH = Frame(finestra)
    contH.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(contH)
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    figura = graph.heat_ds(percorsoD, percorsoS, norm)
    canvas = FigureCanvasTkAgg(figura, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    canvas.draw()
    tool = NavigationToolbar2TkAgg(canvas, contH)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    graph.add_subplot_zoom(canvas)
    ls.__exit__(None,None,None)

def model_p(finestra, list_slaves, percorsoD, percorsoS, norm=False, means=0, numero=0):
    ls = Splash(finestra, "IMG/hg.gif")
    ls.__enter__()
    if len(finestra.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    contH = Frame(finestra)
    contH.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(contH)
    my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
    figura = graph.model_parameters(means, percorsoD, percorsoS, norm, numero)
    canvas = FigureCanvasTkAgg(figura, my_canvas)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    canvas.draw()
    tool = NavigationToolbar2TkAgg(canvas, contH)
    tool.update()
    canvas._tkcanvas.pack(fill=BOTH, expand=1)
    graph.add_subplot_zoom(canvas)
    ls.__exit__(None,None,None)

def highlight_model_p(finestra, list_slaves, percorsoD, percorsoS, norm=False, means=0, numero=0):
    ls = Splash(finestra, "IMG/hg.gif")
    ls.__enter__()
    locale.setlocale(locale.LC_NUMERIC, 'C')
    if len(finestra.pack_slaves()) > 3:
        list_slaves[2].destroy()
        list_slaves[3].destroy()
    else:
        list_slaves[2].destroy()
    gi, mp = graph.highlight_model_p(means, percorsoD, percorsoS, norm, numero)
    f = Frame(finestra)
    f.pack(fill=BOTH, expand=1)
    f1 = Frame(f)
    f1.pack(side=LEFT, fill=BOTH,expand=1)
    f2 = Frame(f)
    f2.pack(side=LEFT, fill=BOTH,expand=1)
    #df = TableModel.getSampleData()
    pt = Table(f1, dataframe=gi)
    pt2 = Table(f2, dataframe=mp)
    pt.show()    
    pt2.show()
    ls.__exit__(None,None,None)

def view_dictionary(finestra, list_slaves):    
    list_slaves[2].destroy()
    f = Frame(finestra)
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
    
def openResults(finestra, text): 
    global percorsoS
    percorsoS = tkFileDialog.askdirectory(title = "Select directory of Results")
    text.delete('1.0', END)
    text.insert(INSERT, percorsoS)
    #do_nc(percorsoS+"/")
    finestra.lift()
    
def openDataset(finestra, text):
    global percorsoD
    percorsoD = tkFileDialog.askopenfilename(initialdir = "/home/whitebreeze/Tirocinio/InCatch/DATASETS",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*")))
    text.delete('1.0', END)
    text.insert(INSERT, percorsoD)
    finestra.lift()

def openGroundTruth(finestra, text):
    global percorsoG
    percorsoG = tkFileDialog.askopenfilename(initialdir = "/home/whitebreeze/Tirocinio/InCatch/DATASETS",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*")))
    text.delete('1.0', END)
    text.insert(INSERT, percorsoG)
    finestra.lift()

def make_welcome(finestra, cont):
    if len(cont.pack_slaves()) > 0:
        for item in cont.pack_slaves():
            item.destroy() 
    contW = Frame(cont)
    contW.pack(fill=BOTH, expand=1)
    #path = os.path.abspath("XM.pgm")
    #ico = tkinter.PhotoImage(master=contW, file="XM.pgm")
    #labelIco = Label(contW, image = ico)
    #labelIco.image = ico
    #labelIco.pack(side=LEFT)
    openB = Button(contW)
    openB.configure(text="Open cluster results", command= lambda: continueO(finestra, contW, cont))
    computeB = Button(contW)
    computeB.configure(text="Create new clustering", command= lambda: continueC(finestra, contW, cont))
    openB.pack(fill=BOTH, expand=1)
    computeB.pack(fill=BOTH, expand=1)
    finestra.update()
    
def continueO(finestra, contW, cont):
    for item in contW.pack_slaves():
        item.destroy()
    backB = Button(contW)
    backB.configure(text="Back", command= lambda: make_welcome(finestra, cont))
    backB.pack(side=LEFT, fill=BOTH, expand=1)
    frameO = Frame(contW)
    frameO.pack(side=RIGHT, fill=BOTH, expand=1)
    frameOpen = Frame(frameO)
    frameOpen.pack(side=TOP)
    frameRes = Frame(frameO)
    frameRes.pack(side=TOP)
    frameGT = Frame(frameO)
    frameOpen.pack(side=TOP)
    frameGT.pack(side=TOP)
    textOpen = Text(frameOpen, height=1)
    textRes = Text(frameRes, height=1)
    textRes.pack(side=RIGHT, fill=X, expand=1)
    textOpen.pack(side=RIGHT, fill=X, expand=1)
    textGT = Text(frameGT, height=1)
    textGT.pack(side=RIGHT, fill=X, expand=1)
    openData = Button(frameOpen, text='Open Dataset', command=lambda : openDataset(finestra, textOpen))
    openGT = Button(frameGT, text='Open Ground Truth', command=lambda : openGroundTruth(finestra, textGT))
    openRes = Button(frameRes, text='Open Results', command=lambda : openResults(finestra, textRes))
    openData.pack(side=LEFT)
    openRes.pack(side=LEFT)
    openGT.pack(side=LEFT)
    goButton = Button(frameO)
    goButton.configure(text="LOAD", command= lambda: on_load(finestra, finestra.pack_slaves(), str(textOpen.get("1.0","end-1c")), str(textRes.get("1.0","end-1c"))+"/", str(textGT.get("1.0","end-1c"))))
    goButton.pack(side=BOTTOM)
    finestra.update()
    
def continueC(finestra, contW, cont):
    if platform.system() != 'Linux':
        return
    for item in contW.pack_slaves():
        item.destroy()
    backB = Button(contW)
    backB.configure(text="Back", command= lambda: make_welcome(finestra, cont))
    backB.pack(side=LEFT, fill=BOTH, expand=1)
    contM = Frame(contW)
    contM.pack(fill=BOTH, expand=1)
    varM = StringVar()
    radioSCM = Radiobutton(contM, text="SubCMedians", variable=varM, value="SCM")
    radioSCM.pack(side=TOP)
    radioSCM.deselect()
    contCB = Button(contM)
    contCB.configure(text="Continue", command= lambda: finishC(finestra, contW, cont, varM.get()))
    contCB.pack(fill=BOTH, expand=1)
    finestra.update()
    
def finishC(finestra, contW, cont, method):
    if method == "":
        tkMessageBox.showwarning("No Method Selected", "Choose a method before continuing")
        return
    for item in contW.pack_slaves():
        item.destroy()
    backB = Button(contW)
    backB.configure(text="Back", command= lambda: continueC(finestra, contW, cont))
    backB.pack(side=LEFT, fill=BOTH, expand=1)
    contF = Frame(contW)
    contF.pack(side=RIGHT, fill=BOTH, expand=1)
    if method == "SCM":
        gid.SCM(contF, cont, finestra)
    finestra.update()
   
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
    
def build_up():
    try:
        global finestra
        dizionario = ["Acqua", "Non acqua", "Con Corrente", "Contro Corrente", "Anomalia"]
        finestra = Tk()
        finestra.title("XM_v1.3")
        finestra.wm_iconbitmap("@"+"IMG/XM_icon.xbm")
        cont = Frame(finestra)
        cont.pack(side=TOP, expand=1, fill=BOTH)
        #my_canvas = Canvas(finestra)
        #my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        sidebar = Frame(finestra)
        sidebar.pack(side=TOP, fill=X)
        global var
        global varD
        global varG
        global varGT
        global varS
        global varDN
        global optionsG
        global optionsD
        global optionsGT
        global optionsO
        global optionsDN
        var = StringVar(sidebar)
        varD = StringVar(sidebar)
        varG = StringVar(sidebar)
        varGT = StringVar(sidebar)
        varDN = StringVar(sidebar)
        optionsDa = ["Dataset"]
        optionsG = ["General Info", "Model Parameters", "Heatmap clustering", "Heatmap dataset", "Time Series", "2D/3D Scatters", "BoxPlot", "BarPlot", "Geo-localization"]
        optionsD = ["Time Series", "2D/3D Scatters", "BoxPlot", "BarPlot", "Heatmap"]
        optionsGT = ["Modeling", "Ground Truth"]
        varS = StringVar(sidebar)
        optionsO = ["Symmetrical Uncertainty"]
        optionsDN = ["Real", "Normalized"]
        make_welcome(finestra, cont)
        finW = finestra.winfo_reqwidth()
        finH = finestra.winfo_reqheight()
        scrW = finestra.winfo_screenwidth()
        scrH = finestra.winfo_screenheight()
        Xpos = (scrW - finW) // 2
        Ypos = (scrH - finH) // 2
        finestra.geometry('+{}+{}'.format(Xpos, Ypos))
        finestra.mainloop()
    except ImportError as err:
        print sys.exc_info()
        finestra.destroy()
        errore = Tk()
        errore.title("CRASH")
        contB = Frame(errore)
        contB.pack(fill=BOTH, expand=1)
        showL = Button(contB, text="Show help", command= lambda: helpL(contB))
        showL.pack()
        errore.mainloop()
    
    
    
if __name__ == "__main__":
    try:
        dizionario = ["Acqua", "Non acqua", "Con Corrente", "Contro Corrente", "Anomalia"]
        finestra = Tk()
        finestra.title("XM_v1.3")
        finestra.wm_iconbitmap("@"+"IMG/XM_icon.xbm")
        cont = Frame(finestra)
        cont.pack(side=TOP, expand=1, fill=BOTH)
        #my_canvas = Canvas(finestra)
        #my_canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        sidebar = Frame(finestra)
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
        var = StringVar(sidebar)
        varD = StringVar(sidebar)
        varG = StringVar(sidebar)
        varGT = StringVar(sidebar)
        varDN = StringVar(sidebar)
        optionsDa = ["Dataset"]
        optionsG = ["General Info", "Model Parameters", "Heatmap clustering", "Heatmap dataset", "Time Series", "2D/3D Scatters", "BoxPlot", "BarPlot", "Geo-localization"]
        optionsD = ["Time Series", "2D/3D Scatters", "BoxPlot", "BarPlot", "Heatmap"]
        optionsGT = ["Modeling", "Ground Truth"]
        varS = StringVar(sidebar)
        optionsO = ["Symmetrical Uncertainty"]
        optionsDN = ["Real", "Normalized"]
        make_welcome(finestra, cont)
        finW = finestra.winfo_reqwidth()
        finH = finestra.winfo_reqheight()
        scrW = finestra.winfo_screenwidth()
        scrH = finestra.winfo_screenheight()
        Xpos = (scrW - finW) // 2
        Ypos = (scrH - finH) // 2
        finestra.geometry('+{}+{}'.format(Xpos, Ypos))
        finestra.mainloop()
    except ImportError as err:
        print sys.exc_info()
        finestra.destroy()
        errore = Tk()
        errore.title("CRASH")
        contB = Frame(errore)
        contB.pack(fill=BOTH, expand=1)
        showL = Button(contB, text="Show help", command= lambda: helpL(contB))
        showL.pack()
        errore.mainloop()