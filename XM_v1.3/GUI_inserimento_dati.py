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
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
from MethodLib.SubCMedians import subc as sc



def scm(finestra):
        
    frameStatus = Frame(finestra)
    frameStatus.pack(side=BOTTOM, fill=X)
    status= Label(frameStatus, bd=1, relief=SUNKEN, anchor=W, text="Ready")
    status.pack(fill=X)
    frameEntryRadio = Frame(finestra)
    frameEntryRadio.pack(side=TOP)
    frameEntry = Frame(frameEntryRadio)
    frameEntry.pack(side=LEFT)
    frameRadio = Frame(frameEntryRadio)
    frameRadio.pack(side=RIGHT)
    frameBottoniVari = Frame(finestra)
    frameBottoniVari.pack(side=BOTTOM)
    row = Frame(frameEntry)
    lab = Label(row, width=15, text='NbExpectedCluster', anchor='w')
    ent = Entry(row)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    entry = []
    entry.append(('NbExpectedCluster', ent))
    var = IntVar()
    radioDefault = Radiobutton(frameRadio, text="Default parameters", variable=var, value=1, command= lambda: makeform(finestra, frameBottoniVari, frameEntry, fields, entry, False, status))
    radioDefault.select()
    radioDefault.pack()
    radioCustom = Radiobutton(frameRadio, text="Custom parameters", variable=var, value=2, command= lambda: makeform(finestra, frameBottoniVari, frameEntry, fields, entry, True, status))
    radioCustom.pack()
    frameOpen = Frame(frameBottoniVari)
    frameOpen.pack(side=BOTTOM)
    frameSave = Frame(frameBottoniVari)
    frameSave.pack(side=BOTTOM)
    frameGT = Frame(frameBottoniVari)
    frameGT.pack(side=BOTTOM)
    textOpen = Text(frameOpen, height=1)
    textSave = Text(frameSave, height=1)
    textSave.pack(side=RIGHT, fill=X, expand=1)
    textOpen.pack(side=RIGHT, fill=X, expand=1)
    textGT = Text(frameGT, height=1)
    textGT.pack(side=RIGHT, fill=X, expand=1)
    #entry = makeform(frameEntry, fields, True)
    fields = 'NbExpectedCluster', 'SDmax', 'N', 'NbIter'
    openB = Button(frameOpen, text='Select Dataset', command=lambda : openFile(finestra, textOpen))
    save = Button(frameSave, text='Save in', command=lambda : saveDirectory(finestra, textSave))
    gt = Button(frameGT, text='Ground Truth', command=lambda : gtFile(finestra, textGT))
    openB.pack(side=LEFT)
    save.pack(side=LEFT)
    gt.pack(side=LEFT)
    start = Button(frameBottoniVari, text='Start', command=lambda e=entry: comp_Default(status, entry[0][1].get(), str(textOpen.get("1.0","end-1c")), str(textSave.get("1.0","end-1c")), str(textGT.get("1.0","end-1c"))))
    start.pack(side=BOTTOM)
                
def saveDirectory(finestra, text):
    
    global percorsoS
    percorsoS = tkFileDialog.askdirectory(title = "Select directory for save function")
    text.delete('1.0', END)
    text.insert(INSERT, percorsoS)
    finestra.lift()
    
def openFile(finestra, text):
    
    global percorsoD
    percorsoD = tkFileDialog.askopenfilename(initialdir = "/home/whitebreeze/Tirocinio/InCatch/DATASETS",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*")))
    text.delete('1.0', END)
    text.insert(INSERT, percorsoD)
    finestra.lift()
  
def gtFile(finestra, text):
    
    global percorsoG
    percorsoG = tkFileDialog.askopenfilename(initialdir = "/home/whitebreeze/Tirocinio/InCatch/DATASETS",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*")))
    text.delete('1.0', END)
    text.insert(INSERT, percorsoG)
    finestra.lift()    
    
def makeform(finestra, frameBottoniVari, frameEntry, fields, entry, var, status):

    if var == True:
        for item in frameEntry.pack_slaves():
            item.destroy()
        frameBottoniVari.pack_slaves()[3].destroy()
        frameOp = frameBottoniVari.pack_slaves()[0]
        textOp = frameOp.pack_slaves()[0]
        frameSa = frameBottoniVari.pack_slaves()[1]
        textSa = frameSa.pack_slaves()[0]
        frameGt = frameBottoniVari.pack_slaves()[2]
        textGt = frameGt.pack_slaves()[0]
        start = Button(frameBottoniVari, text='Start', command=lambda e=entry: comp_Custom(status, entry[0][1].get(), entry[1][1].get(), entry[2][1].get(), entry[3][1].get(), str(textOp.get("1.0","end-1c")), str(textSa.get("1.0","end-1c")), str(textGt.get("1.0","end-1c"))))
        start.pack(side=BOTTOM)
        entry = []
        for field in fields:
           row = Frame(frameEntry)
           lab = Label(row, width=15, text=field, anchor='w')
           ent = Entry(row)
           row.pack(side=TOP, fill=X, padx=5, pady=5)
           lab.pack(side=LEFT)
           ent.pack(side=RIGHT, expand=YES, fill=X)
           entry.append((field, ent))
        finestra.update()
    else:
        for item in frameEntry.pack_slaves():
            item.destroy()
        frameBottoniVari.pack_slaves()[3].destroy()
        frameOp = frameBottoniVari.pack_slaves()[0]
        textOp = frameOp.pack_slaves()[0]
        frameSa = frameBottoniVari.pack_slaves()[1]
        textSa = frameSa.pack_slaves()[0]
        frameGt = frameBottoniVari.pack_slaves()[2]
        textGt = frameGt.pack_slaves()[0]
        start = Button(frameBottoniVari, text='Start', command=lambda e=entry: comp_Default(status, entry[0][1].get(), str(textOp.get("1.0","end-1c")), str(textSa.get("1.0","end-1c")), str(textGt.get("1.0","end-1c"))))
        start.pack(side=BOTTOM)
        entry = []
        row = Frame(frameEntry)
        lab = Label(row, width=15, text='NbExpectedCluster', anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entry.append(('NbExpectedCluster',ent))
        finestra.update()

def comp_Default(status, entry, percorsoD, percorsoS, percorsoG):
    status.configure(text="Processing")
    status.update()
    sc.genera_cluster(entry, 0, 0, 0, percorsoD, percorsoS, percorsoG)
    status.configure(text="Ready")

def comp_Custom(status, entry1, entry2, entry3, entry4, percorsoD, percorsoS, percorsoG):
    status.configure(text="Processing")
    status.update()
    sc.genera_cluster(entry1, entry2, entry3, entry4, percorsoD, percorsoS, percorsoG)
    status.configure(text="Ready")

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
