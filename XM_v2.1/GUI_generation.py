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
from tkinter import *
import tkinter,tkinter.filedialog
#from MethodLib.SubCMedians import subc as sc
from MethodLib.KMeans import km
from MethodLib.GMM import gmm as gm
from MethodLib.SpectralClustering import spc
from MethodLib.TICC import ticc
import messagebox
import XM as XM


def SCM_GUI(finestra, cont, root):
    frameStatus = Frame(finestra)
    frameStatus.grid(row=3, column=0,sticky="WE")
    status= Label(frameStatus, bd=1, relief=SUNKEN, anchor=W, text="Ready")
    frameEntryRadio = Frame(finestra)
    frameEntryRadio.grid(row=0,column=0)
    frameEntry = Frame(frameEntryRadio)
    frameEntry.grid(row=0, column=0)
    frameRadio = Frame(frameEntryRadio)
    frameRadio.grid(row=0, column=1)
    frameBottoniVari = Frame(finestra)
    frameBottoniVari.grid(row=1, column=0, sticky="WENS")
    row = Frame(frameEntry)
    lab = Label(row, width=15, text='NbExpectedCluster', anchor='w')
    ent = Entry(row)
    row.grid(sticky="NWE", padx=5, pady=5)
    lab.grid(row=0,column=0)
    ent.grid(row=0,column=1)
    entry = []
    entry.append(('NbExpectedCluster', ent))
    var = IntVar()
    radioDefault = Radiobutton(frameRadio, text="Default parameters", variable=var, value=1, command= lambda: makeform(finestra, cont, root, frameBottoniVari, frameEntry, fields, entry, False, status))
    radioDefault.select()
    radioDefault.grid()
    radioCustom = Radiobutton(frameRadio, text="Custom parameters", variable=var, value=2, command= lambda: makeform(finestra, cont, root, frameBottoniVari, frameEntry, fields, entry, True, status))
    radioCustom.grid()
    frameOpen = Frame(frameBottoniVari)
    frameOpen.grid(row=0,sticky="E")
    frameSave = Frame(frameBottoniVari)
    frameSave.grid(row=1,sticky="E")
    frameGT = Frame(frameBottoniVari)
    frameGT.grid(row=2,sticky="E")
    frameEL = Frame(frameBottoniVari)
    #frameEL.pack(side=TOP)
    frameDN = Frame(frameBottoniVari)
    frameDN.grid(row=3,sticky="E")
    textOpen = Text(frameOpen, height=1)
    textSave = Text(frameSave, height=1)
    textSave.grid(row=0,column=1,sticky="E")
    textOpen.grid(row=0,column=1,sticky="E")
    textGT = Text(frameGT, height=1)
    textGT.grid(row=0,column=1,sticky="E")
    textEL = Text(frameEL, height=1)
    textEL.grid(row=0,column=1,sticky="E")
    textDN = Text(frameDN, height=1)
    textDN.grid(row=0,column=1,sticky="E")
    #entry = makeform(frameEntry, fields, True)
    fields = 'SDmax', 'N', 'NbIter'
    openB = Button(frameOpen, text='Select Dataset', command=lambda : openFile(finestra, textOpen))
    save = Button(frameSave, text='Save in', command=lambda : saveDirectory(finestra, textSave))
    gt = Button(frameGT, text='Ground Truth file', command=lambda : gtFile(finestra, textGT))
    el = Button(frameEL, text='Exp. Concat file', command=lambda: elfile(finestra, textEL))
    dn = Button(frameDN, text='Normalization file', command=lambda: dnfile(finestra, textDN))
    openB.grid(row=0,sticky="W")
    save.grid(row=0,sticky="W")
    gt.grid(row=0,sticky="W")
    el.grid(row=0,sticky="W")
    dn.grid(row=0,sticky="W")
    start = Button(finestra, text='Start', command=lambda e=entry: comp_Default(cont, root, status, entry[0][1].get(), str(textOpen.get("1.0","end-1c")), str(textSave.get("1.0","end-1c")), str(textGT.get("1.0","end-1c")), str(textDN.get("1.0","end-1c"))))
    start.grid(row=2)
    status.grid(row=0,sticky="WENS")
  
def TSNE_GUI(finestra, cont, root):
    frameStatus = Frame(finestra)
    frameStatus.grid(row=3, sticky="WE")
    status= Label(frameStatus, bd=1, relief=SUNKEN, text="Ready")
    status.grid(sticky="WE")
    frameSamples = Frame(finestra)
    frameSamples.grid(row=0, pady=5, padx=5)
    row = Frame(frameSamples)
    row.grid()
    samples = Entry(row)
    samples.grid(row=0,column=1)
    labelS = Label(row, text="N. Samples", anchor="w")
    labelS.grid(row=0,column=0)   
    frameBottoniVari = Frame(finestra)
    frameBottoniVari.grid(row=1)
    frameOpen = Frame(frameBottoniVari)
    frameOpen.grid(row=0,sticky="E")
    frameSave = Frame(frameBottoniVari)
    frameSave.grid(row=1,sticky="E")
    textOpen = Text(frameOpen, height=1)
    textOpen.grid(row=0,column=1,sticky="E")
    textSave = Text(frameSave, height=1)
    textSave.grid(row=0,column=1,sticky="E")    
    openB = Button(frameOpen, text='Select Dataset', command=lambda : openFile(finestra, textOpen))
    save = Button(frameSave, text='Select Saves Directory', command=lambda : saveDirectory(finestra, textSave))
    openB.grid(row=0,column=0,sticky="W")
    save.grid(row=0,column=0,sticky="W")
    start = Button(frameBottoniVari, text="Start", command= lambda: compute_tsne(cont, root, status, textOpen.get("1.0","end-1c"), textSave.get("1.0","end-1c"), samples.get()))
    start.grid(row=2)
    
def KMEANS_GUI(finestra, cont, root):
    frameStatus = Frame(finestra)
    frameStatus.grid(row=3,sticky="WE")
    status= Label(frameStatus, bd=1, relief=SUNKEN, anchor=W, text="Ready")
    status.grid(sticky="WE")
    frameSamples = Frame(finestra)
    frameSamples.grid(row=0, pady=5, padx=5)
    row = Frame(frameSamples)
    row.grid()
    clusters = Entry(row)
    clusters.grid(row=0,column=1)
    labelS = Label(row, text="N. Cluster", anchor="w")
    labelS.grid(row=0,column=0)   
    frameBottoniVari = Frame(finestra)
    frameBottoniVari.grid(row=1,sticky="E")
    """
    frameOpen = Frame(frameBottoniVari)
    frameOpen.grid(r)
    frameSave = Frame(frameBottoniVari)
    frameSave.pack(side=TOP)
    frameGT = Frame(frameBottoniVari)
    frameGT.pack(side=TOP)
    frameEL = Frame(frameBottoniVari)
    #frameEL.pack(side=TOP)
    frameDN = Frame(frameBottoniVari)
    frameDN.pack(side=TOP)
    """
    textOpen = Text(frameBottoniVari, height=1)
    textOpen.grid(row=0,column=1,sticky="E")
    textSave = Text(frameBottoniVari, height=1)
    textSave.grid(row=1,column=1,sticky="E")
    textGT = Text(frameBottoniVari, height=1)
    textGT.grid(row=2,column=1,sticky="E")
    #textEL = Text(frameBottoniVari, height=1)
    #textEL.pack(side=RIGHT, fill=X, expand=1)
    textDN = Text(frameBottoniVari, height=1)
    textDN.grid(row=3,column=1,sticky="E")   
    openB = Button(frameBottoniVari, text='Select Dataset', command=lambda : openFile(finestra, textOpen))
    save = Button(frameBottoniVari, text='Save in', command=lambda : saveDirectory(finestra, textSave))
    gt = Button(frameBottoniVari, text='Ground Truth file', command=lambda : gtFile(finestra, textGT))
    el = Button(frameBottoniVari, text='Exp. Concat file', command=lambda: elfile(finestra, textEL))
    dn = Button(frameBottoniVari, text='Normalization file', command=lambda: dnfile(finestra, textDN))
    openB.grid(row=0,column=0,sticky="E")
    save.grid(row=1,column=0,sticky="E")
    gt.grid(row=2,column=0,sticky="E")
    #el.pack(side=LEFT)
    dn.grid(row=3,column=0,sticky="E")
    start = Button(finestra, text="Start", command= lambda: compute_kmeans(cont, root, status, textOpen.get("1.0","end-1c"), textSave.get("1.0","end-1c"), str(textGT.get("1.0","end-1c")), str(textDN.get("1.0","end-1c")), clusters.get()))
    start.grid(row=2)

def GMM_GUI(finestra, cont, root):
    frameStatus = Frame(finestra)
    frameStatus.grid(row=3, sticky="WE")
    status= Label(frameStatus, bd=1, relief=SUNKEN, anchor=W, text="Ready")
    status.grid()
    frameSamples = Frame(finestra)
    frameSamples.grid(row=0, pady=5, padx=5)
    row = Frame(frameSamples)
    row.grid()
    clusters = Entry(row)
    clusters.grid(row=0,column=1)
    labelS = Label(row, text="N. Cluster", anchor="w")
    labelS.grid(row=0,column=0)   
    row2 = Frame(frameSamples)
    row2.grid()
    iniz = Entry(row2)
    iniz.grid(row=0,column=1)
    labelI = Label(row2, text="N. Init", anchor="w")
    labelI.grid(row=0,column=0)  
    row3 = Frame(frameSamples)
    row3.grid()
    varCOV = StringVar()
    radioDIAG = Radiobutton(row3, text="Diag", variable=varCOV, value="D")
    radioDIAG.grid(row=0,column=0)
    radioFULL = Radiobutton(row3, text="Full", variable=varCOV, value="F")
    radioFULL.grid(row=0,column=1)
    radioTIED = Radiobutton(row3, text="Tied", variable=varCOV, value="T")
    radioTIED.grid(row=0,column=2)
    radioSPHE = Radiobutton(row3, text="Spherical", variable=varCOV, value="S")
    radioSPHE.grid(row=0,column=3)
    frameBottoniVari = Frame(finestra)
    frameBottoniVari.grid(row=1,sticky="E")
    """
    frameOpen = Frame(frameBottoniVari)
    frameOpen.pack(side=TOP)
    frameSave = Frame(frameBottoniVari)
    frameSave.pack(side=TOP)
    frameGT = Frame(frameBottoniVari)
    frameGT.pack(side=TOP)
    frameEL = Frame(frameBottoniVari)
    #frameEL.pack(side=TOP)
    frameDN = Frame(frameBottoniVari)
    frameDN.pack(side=TOP)
    """
    textOpen = Text(frameBottoniVari, height=1)
    textOpen.grid(row=0,column=1,sticky="E")
    textSave = Text(frameBottoniVari, height=1)
    textSave.grid(row=1,column=1,sticky="E")
    textGT = Text(frameBottoniVari, height=1)
    textGT.grid(row=2,column=1,sticky="E")
    #textEL = Text(frameBottoniVari, height=1)
    #textEL.pack(side=RIGHT, fill=X, expand=1)
    textDN = Text(frameBottoniVari, height=1)
    textDN.grid(row=3,column=1,sticky="E")   
    openB = Button(frameBottoniVari, text='Select Dataset', command=lambda : openFile(finestra, textOpen))
    save = Button(frameBottoniVari, text='Save in', command=lambda : saveDirectory(finestra, textSave))
    gt = Button(frameBottoniVari, text='Ground Truth file', command=lambda : gtFile(finestra, textGT))
    el = Button(frameBottoniVari, text='Exp. Concat file', command=lambda: elfile(finestra, textEL))
    dn = Button(frameBottoniVari, text='Normalization file', command=lambda: dnfile(finestra, textDN))
    openB.grid(row=0,column=0,sticky="E")
    save.grid(row=1,column=0,sticky="E")
    gt.grid(row=2,column=0,sticky="E")
    #el.pack(side=LEFT)
    dn.grid(row=3,column=0,sticky="E")
    start = Button(finestra, text="Start", command= lambda: compute_gmm(cont, root, status, textOpen.get("1.0","end-1c"), textSave.get("1.0","end-1c"), str(textGT.get("1.0","end-1c")), str(textDN.get("1.0","end-1c")), clusters.get(), iniz.get(), varCOV.get()))
    start.grid(row=2)
    
def SPECTRAL_GUI(finestra, cont, root):
    frameStatus = Frame(finestra)
    frameStatus.grid(row=3,sticky="WE")
    status= Label(frameStatus, bd=1, relief=SUNKEN, anchor=W, text="Ready")
    status.grid(sticky="WE")
    frameSamples = Frame(finestra)
    frameSamples.grid(row=0, pady=5, padx=5)
    row = Frame(frameSamples)
    row.grid()
    clusters = Entry(row)
    clusters.grid(row=0,column=1)
    labelS = Label(row, text="N. Cluster", anchor="w")
    labelS.grid(row=0,column=0)   
    frameBottoniVari = Frame(finestra)
    frameBottoniVari.grid(row=1,sticky="E")
    """
    frameOpen = Frame(frameBottoniVari)
    frameOpen.grid(r)
    frameSave = Frame(frameBottoniVari)
    frameSave.pack(side=TOP)
    frameGT = Frame(frameBottoniVari)
    frameGT.pack(side=TOP)
    frameEL = Frame(frameBottoniVari)
    #frameEL.pack(side=TOP)
    frameDN = Frame(frameBottoniVari)
    frameDN.pack(side=TOP)
    """
    textOpen = Text(frameBottoniVari, height=1)
    textOpen.grid(row=0,column=1,sticky="E")
    textSave = Text(frameBottoniVari, height=1)
    textSave.grid(row=1,column=1,sticky="E")
    textGT = Text(frameBottoniVari, height=1)
    textGT.grid(row=2,column=1,sticky="E")
    #textEL = Text(frameBottoniVari, height=1)
    #textEL.pack(side=RIGHT, fill=X, expand=1)
    textDN = Text(frameBottoniVari, height=1)
    textDN.grid(row=3,column=1,sticky="E")   
    openB = Button(frameBottoniVari, text='Select Dataset', command=lambda : openFile(finestra, textOpen))
    save = Button(frameBottoniVari, text='Save in', command=lambda : saveDirectory(finestra, textSave))
    gt = Button(frameBottoniVari, text='Ground Truth file', command=lambda : gtFile(finestra, textGT))
    el = Button(frameBottoniVari, text='Exp. Concat file', command=lambda: elfile(finestra, textEL))
    dn = Button(frameBottoniVari, text='Normalization file', command=lambda: dnfile(finestra, textDN))
    openB.grid(row=0,column=0,sticky="E")
    save.grid(row=1,column=0,sticky="E")
    gt.grid(row=2,column=0,sticky="E")
    #el.pack(side=LEFT)
    dn.grid(row=3,column=0,sticky="E")
    start = Button(finestra, text="Start", command= lambda: compute_spectral(cont, root, status, textOpen.get("1.0","end-1c"), textSave.get("1.0","end-1c"), str(textGT.get("1.0","end-1c")), str(textDN.get("1.0","end-1c")), clusters.get()))
    start.grid(row=2)
    
def TICC_GUI(finestra, cont, root):
    frameStatus = Frame(finestra)
    frameStatus.grid(row=3,sticky="WE")
    status= Label(frameStatus, bd=1, relief=SUNKEN, anchor=W, text="Ready")
    status.grid(sticky="WE")
    frameSamples = Frame(finestra)
    frameSamples.grid(row=0, pady=5, padx=5)
    row = Frame(frameSamples)
    row.grid()
    clusters = Entry(row)
    clusters.grid(row=0,column=1)
    labelS = Label(row, text="N. Cluster", anchor="w")
    labelS.grid(row=0,column=0)
    row2 = Frame(frameSamples)
    row2.grid()
    window = Entry(row2)
    window.grid(row=0,column=1)
    labelW = Label(row2, text="Window size", anchor="w")
    labelW.grid(row=0,column=0)
    row3 = Frame(frameSamples)
    row3.grid()
    p_lambda = Entry(row3)
    p_lambda.grid(row=0,column=1)
    labelL = Label(row3, text="Lambda", anchor="w")
    labelL.grid(row=0,column=0)
    row4 = Frame(frameSamples)
    row4.grid()
    beta = Entry(row4)
    beta.grid(row=0,column=1)
    labelB = Label(row4, text="Beta", anchor="w")
    labelB.grid(row=0,column=0)
    frameBottoniVari = Frame(finestra)
    frameBottoniVari.grid(row=1,sticky="E")
    textOpen = Text(frameBottoniVari, height=1)
    textOpen.grid(row=0,column=1,sticky="E")
    textSave = Text(frameBottoniVari, height=1)
    textSave.grid(row=1,column=1,sticky="E")
    textGT = Text(frameBottoniVari, height=1)
    textGT.grid(row=2,column=1,sticky="E")
    #textEL = Text(frameBottoniVari, height=1)
    #textEL.pack(side=RIGHT, fill=X, expand=1)
    textDN = Text(frameBottoniVari, height=1)
    textDN.grid(row=3,column=1,sticky="E")   
    openB = Button(frameBottoniVari, text='Select Dataset', command=lambda : openFile(finestra, textOpen))
    save = Button(frameBottoniVari, text='Save in', command=lambda : saveDirectory(finestra, textSave))
    gt = Button(frameBottoniVari, text='Ground Truth file', command=lambda : gtFile(finestra, textGT))
    el = Button(frameBottoniVari, text='Exp. Concat file', command=lambda: elfile(finestra, textEL))
    dn = Button(frameBottoniVari, text='Normalization file', command=lambda: dnfile(finestra, textDN))
    openB.grid(row=0,column=0,sticky="E")
    save.grid(row=1,column=0,sticky="E")
    gt.grid(row=2,column=0,sticky="E")
    #el.pack(side=LEFT)
    dn.grid(row=3,column=0,sticky="E")
    start = Button(finestra, text="Start", command= lambda: compute_ticc(cont, root, status, textOpen.get("1.0","end-1c"), textSave.get("1.0","end-1c"), str(textGT.get("1.0","end-1c")), str(textDN.get("1.0","end-1c")), clusters.get(), window.get(), p_lambda.get(), beta.get()))
    start.grid(row=2)
    
def saveDirectory(finestra, text):
    
    global percorsoS
    percorsoS =filedialog.askdirectory(title = "Select directory for save function")
    text.delete('1.0', END)
    text.insert(INSERT, percorsoS)
    finestra.lift()
    
def openFile(finestra, text):
    
    global percorsoD
    percorsoD =filedialog.askopenfilename(initialdir = "/home/whitebreeze/Tirocinio/InCatch/DATASETS",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*")))
    text.delete('1.0', END)
    text.insert(INSERT, percorsoD)
    finestra.lift()
  
def gtFile(finestra, text):
    
    global percorsoG
    percorsoG =filedialog.askopenfilename(initialdir = "/home/whitebreeze/Tirocinio/InCatch/DATASETS",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*")))
    text.delete('1.0', END)
    text.insert(INSERT, percorsoG)
    finestra.lift()    
    
def elfile(finestra, text):
    
    global percorsoEL
    percorsoEL =filedialog.askopenfilename(initialdir = "/home/whitebreeze/Tirocinio/InCatch/DATASETS",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*")))
    text.delete('1.0', END)
    text.insert(INSERT, percorsoEL)
    finestra.lift()
    
def dnfile(finestra, text):
    
    global percorsoDN
    percorsoDN =filedialog.askopenfilename(initialdir = "/home/whitebreeze/Tirocinio/InCatch/DATASETS",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*")))
    text.delete('1.0', END)
    text.insert(INSERT, percorsoDN)
    finestra.lift()
    
def makeform(finestra, cont, root, frameBottoniVari, frameEntry, fields, entry, var, status):

    for item in frameEntry.grid_slaves():
            item.destroy()
    frameOp = frameBottoniVari.grid_slaves()[3]
    textOp = frameOp.grid_slaves()[1]
    frameSa = frameBottoniVari.grid_slaves()[2]
    textSa = frameSa.grid_slaves()[1]
    frameGt = frameBottoniVari.grid_slaves()[1]
    textGt = frameGt.grid_slaves()[1]
    #frameEl = frameBottoniVari.pack_slaves()[3]
    #textEl = frameEl.pack_slaves()[0]
    frameDn = frameBottoniVari.grid_slaves()[0]
    textDn = frameDn.grid_slaves()[1]
    if var == True:
        start = Button(finestra, text='Start', command=lambda e=entry: comp_Custom(cont, root, status, entry[0][1].get(), entry[1][1].get(), entry[2][1].get(), str(textOp.get("1.0","end-1c")), str(textSa.get("1.0","end-1c")), str(textGt.get("1.0","end-1c")), str(textDn.get("1.0","end-1c"))))
        start.grid(row=2)
        entry = []
        for field in fields:
           row = Frame(frameEntry)
           lab = Label(row, width=15, text=field, anchor='w')
           ent = Entry(row)
           row.grid(sticky="WE", padx=5, pady=5)
           lab.grid(row=0,column=0)
           ent.grid(row=0,column=1, sticky="WE")
           entry.append((field, ent))
        finestra.update()
    else:
        start = Button(finestra, text='Start', command=lambda e=entry: comp_Default(cont, root, status, entry[0][1].get(), str(textOp.get("1.0","end-1c")), str(textSa.get("1.0","end-1c")), str(textGt.get("1.0","end-1c")),  str(textDn.get("1.0","end-1c"))))
        start.grid(row=2)
        entry = []
        row = Frame(frameEntry)
        lab = Label(row, width=15, text='NbExpectedCluster', anchor='w')
        ent = Entry(row)
        row.grid(sticky="WE", padx=5, pady=5)
        lab.grid(row=0,column=0)
        ent.grid(row=0,column=1, sticky="WE")
        entry.append(('NbExpectedCluster',ent))
        finestra.update()

def comp_Default(finestra, root, status, entry, percorsoD, percorsoS, percorsoG, percorsoDN):
    status.configure(text="Processing")
    status.update()
    print(percorsoS)
    if entry == "":
        messagebox.showwarning("WARNING", "Specify number of clusters")
        status.configure(text="Ready")
        return
    sc.genera_cluster(entry, 0, 0, 0, percorsoD, percorsoS, percorsoG, percorsoDN)
    status.configure(text="Ready")
    messagebox.showinfo("Finish", "The clustering process has ended successfully")
    root.destroy()
    XM.build_up()

def comp_Custom(finestra, root, status, entry1, entry2, entry3, percorsoD, percorsoS, percorsoG, percorsoDN):
    status.configure(text="Processing")
    status.update()
    if entry1 == "":
        messagebox.showwarning("WARNING", "Specify SDMax")
        status.configure(text="Ready")
        return
    if entry2 == "":
        messagebox.showwarning("WARNING", "Specify N")
        status.configure(text="Ready")
        return
    if entry3 == "":
        messagebox.showwarning("WARNING", "Specify NbIter")
        status.configure(text="Ready")
        return
    sc.genera_cluster("-", entry1, entry2, entry3, percorsoD, percorsoS, percorsoG, percorsoDN)
    status.configure(text="Ready")
    messagebox.showinfo("Finish", "The clustering process has ended successfully")
    root.destroy()
    XM.build_up()

def compute_tsne(finestra, root, status, percorsoD, percorsoS, samples):
    status.configure(text="Processing")
    status.update()
    if samples == "":
        messagebox.showwarning("WARNING", "Specify number of samples")
        status.configure(text="Ready")
        return
    sc.tsne(percorsoD, percorsoS, samples)
    status.configure(text="Ready")
    messagebox.showinfo("Finish", "The t-SNE process has ended successfully")
    root.destroy()
    XM.build_up()

def compute_kmeans(finestra, root, status, percorsoD, percorsoS, percorsoG, percorsoDN, clusters):
    status.configure(text="Processing")
    status.update()
    if clusters == "":
        messagebox.showwarning("WARNING", "Specify number of clusters")
        status.configure(text="Ready")
        return
    km.kmeans(clusters, percorsoD, percorsoS, percorsoG, percorsoDN)
    status.configure(text="Ready")
    messagebox.showinfo("Finish", "The KMEANS process has ended successfully")
    root.destroy()
    XM.build_up()
    
def compute_gmm(finestra, root, status, percorsoD, percorsoS, percorsoG, percorsoDN, clusters, iniz, cov):
    status.configure(text="Processing")
    status.update()
    if clusters == "":
        messagebox.showwarning("WARNING", "Specify number of clusters")
        status.configure(text="Ready")
        return
    if iniz == "":
        messagebox.showwarning("WARNING", "Specify number of re-initialization")
        status.configure(text="Ready")
        return
    if cov == "":
        messagebox.showwarning("WARNING", "Select a type of variance")
        status.configure(text="Ready")
        return
    if cov == "D":
        cov = 'diag'
    if cov == "F":
        cov = 'full'
    if cov == "T":
        cov = 'tied'
    if cov == "S":
        cov = 'spherical'
    gm.gmm(clusters, cov, iniz, percorsoD, percorsoS, percorsoG, percorsoDN)
    status.configure(text="Ready")
    messagebox.showinfo("Finish", "The GMM process has ended successfully")
    root.destroy()
    XM.build_up()
    
def compute_spectral(finestra, root, status, percorsoD, percorsoS, percorsoG, percorsoDN, clusters):
    status.configure(text="Processing")
    status.update()
    if clusters == "":
        messagebox.showwarning("WARNING", "Specify number of clusters")
        status.configure(text="Ready")
        return
    spc.spectral(clusters, percorsoD, percorsoS, percorsoG, percorsoDN)
    status.configure(text="Ready")
    messagebox.showinfo("Finish", "The Spectral clustering process has ended successfully")
    root.destroy()
    XM.build_up()
    
def compute_ticc(finestra, root, status, percorsoD, percorsoS, percorsoG, percorsoDN, clusters, window, p_lambda, beta):
    status.configure(text="Processing")
    status.update()
    if clusters == "":
        messagebox.showwarning("WARNING", "Specify number of clusters")
        status.configure(text="Ready")
        return
    ticc.genera_cluster(clusters, window, p_lambda, beta, percorsoD, percorsoS, percorsoG, percorsoDN)
    status.configure(text="Ready")
    messagebox.showinfo("Finish", "The TICC process has ended successfully")
    root.destroy()
    XM.build_up()

def make_continue(method, contCreate):
    
    if len(contCreate.pack_slaves())>2:
        contCreate.pack_slaves()[2].destroy()
    continueB = Button(contCreate, text="Continue", command= lambda: do_gid(method, contCreate))
    continueB.pack(side=BOTTOM)
    
def do_gid(method, contCreate):
    
    if method=="SubCMedians" :
        for item in contCreate.pack_slaves():
            item.destroy()
    if method == "SubCMedians":
        scm(contCreate)

def start():
    finestra = Tk()
    finestra.title("Create")
    chooseM = Frame(finestra, height=200, width=400)
    chooseM.pack(expand=1, side=TOP, fill=BOTH)
    varM = StringVar()
    radioSCM = Radiobutton(chooseM, text="SubCMedians", variable=varM, value="SCM", command= lambda: make_continue("SubCMedians", chooseM))
    radioSCM.pack(side=TOP)
    #radioCLIQUE = Radiobutton(contCreate, text="CLIQUE", variable=varM, value="Q", command= lambda: make_continue("Clique", contCreate))
    #radioCLIQUE.pack(side=TOP)
    varM.set(None)
    radioSCM.deselect()
    finestra.mainloop()
