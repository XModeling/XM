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

import SU
import seaborn as sns
import pandas as pd
import numpy as np
import sklearn.metrics as sk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.pylab as pl
import csv
import re
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
import numpy as np
from Tkinter import Label
#import folium
#import os
#import subprocess




def tabCentroidi(coordinate, coordinateVv, labeltab, labelvar):
    
    """
    Tabella simil imagesc
    """
    
    cmapC = plt.cm.get_cmap('summer_r')
    colors.Normalize(clip=False)
    cmapC.set_under(color='grey', alpha=1)
    ax = sns.heatmap(coordinate.T, xticklabels=labeltab, yticklabels=labelvar, annot=coordinateVv.T, linewidths=.05, linecolor='black', cbar=True, cmap=cmapC)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    return ax

def tabHeatmap(coordinate, coordinateVv, labeltab, labelvar):
    
    cmapC = plt.cm.get_cmap('tab20')
    colors.Normalize(clip=False)
    cmapC.set_under(color='grey')
    ax = sns.heatmap(coordinate.T, xticklabels=labeltab, yticklabels=labelvar, annot=coordinateVv.T, linewidths=.05, linecolor='black', cbar=True, cmap=cmapC)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    return ax

def add_subplot_zoom(figure):

    # temporary store for the currently zoomed axes. Use a list to work around
    # python's scoping rules
    zoomed_axes = [None]
    label = Label(figure.get_tk_widget())
    def over(event):
        ax = event.inaxes
        
        if ax is None:
            label.pack_forget()
            return
        
        label.configure(text="SHIFT+Left Click to zoom in on a graph")
        label.pack()

    def on_click(event):
        ax = event.inaxes

        if ax is None:
            # occurs when a region not in an axis is clicked...
            return

        # we want to allow other navigation modes as well. Only act in case
        # shift was pressed and the correct mouse button was used
        if event.key != 'shift' or event.button != 1:
        #if event.button != 3:
            return

        if zoomed_axes[0] is None:
            # not zoomed so far. Perform zoom

            # store the original position of the axes
            zoomed_axes[0] = (ax, ax.get_position())
            ax.set_position([0.1, 0.1, 0.85, 0.85])

            # hide all the other axes...
            for axis in event.canvas.figure.axes:
                if axis is not ax:
                    axis.set_visible(False)

        else:
            # restore the original state

            zoomed_axes[0][0].set_position(zoomed_axes[0][1])
            zoomed_axes[0] = None

            # make other axes visible again
            for axis in event.canvas.figure.axes:
                axis.set_visible(True)

        # redraw to make changes visible.
        event.canvas.draw()

    figure.mpl_connect('motion_notify_event', over)
    figure.mpl_connect('button_press_event', on_click)


def to_scatter(ax, x, y, labelx, labely, color, colorlegend, legendlabel):

        ax.scatter(x, y, c=color, edgecolors='face', s=2)
        ax.set_xlabel(labelx)
        ax.set_ylabel(labely)
        ax.grid(True)
        ax.legend(colorlegend, legendlabel, loc=4, fontsize=8, ncol=len(legendlabel))
        return ax
    

def model_parameters(percorsoD, percorsoS, numerocl=0):
    
    df, latitude, longitude = get_dataset(percorsoD)
    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    labelvar = list(df)  
    labeltab = list(set(clusternorm))
    new_coN = pd.read_table(percorsoS+"model_parameters.txt", delim_whitespace=True)
    new_coV = pd.read_table(percorsoS+"model_parameters.txt", delim_whitespace=True)
    righe,colonne = new_coN.shape
    coordinateVv = new_coV.values
    coordinateNv = new_coN.values
    if numerocl!=0:       
        for i in range(0, righe):
            if i+1 != numerocl:
                 for j in range(0, colonne):
                     coordinateNv[i][j] = 'nan'
            else:    
                for j in range(0, colonne):
                    if str(coordinateNv[i][j]) != 'nan':
                        if coordinateNv[i][j] != 0:
                            coordinateNv[i][j] = 1 
        for i in range(0, righe):
            if i+1 != numerocl:
                for j in range(0, colonne):
                    coordinateVv[i][j] = 'nan'
    else:
        for i in range(0, righe):
            for j in range(0, colonne):
                if coordinateNv[i][j] != 0:
                    if str(coordinateNv[i][j]) != 'nan':
                        coordinateNv[i][j] = 1
    
    fig = plt.figure()
    ax01 = fig.add_subplot(1,1,1)
    ax01 = tabCentroidi(coordinateNv, coordinateVv, labeltab, labelvar)
    ax01.set_title("Used Variables")
    
    return fig

def heat_ds(percorsoD):
    df, latitude, longitude = get_dataset(percorsoD)
    labelvar = list(df)
    fig = plt.figure()
    ax01 = fig.add_subplot(1,1,1)
    ax01 = sns.heatmap(df.T, yticklabels=labelvar, cbar=True, cmap="summer_r")
    ax01.set_title("Heatmap")
    
    return fig

def heat_clust(percorsoD, percorsoS, numerocl=0):
    
    df, latitude, longitude = get_dataset(percorsoD)
    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    labelvar = list(df)  
    new_coN = pd.read_table(percorsoS+"model_parameters.txt", delim_whitespace=True)
    righe,colonne = new_coN.shape
    coordinateNv = new_coN.values
    obs = [item for item in range(0, df.shape[0])]
    coordVere = []
    colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
    if numerocl!=0: 
        for i in range(0, len(obs)):
            coordRiga = []
            if clusternorm[i] != numerocl:
                 for j in range(0, colonne):
                     coordRiga.append(np.nan)
                 coordVere.append(coordRiga)
            else:    
                for j in range(0, colonne):
                    if str(coordinateNv[numerocl-1][j]) != 'nan':
                        if coordinateNv[numerocl-1][j] != 0:
                            coordRiga.append(numerocl)
                        else:
                            coordRiga.append(0)
                    else:
                        coordRiga.append(np.nan)
                coordVere.append(coordRiga)
        
    else:
        for i in range(0, len(obs)):
            coordRiga = []
            for j in range(0, colonne):
                if coordinateNv[int(clusternorm[i])-1][j] != 0:
                    if str(coordinateNv[int(clusternorm[i])-1][j]) != 'nan':
                        coordRiga.append(clusternorm[i])
                    else:
                        coordRiga.append(np.nan)
                else:
                    coordRiga.append(0)
            coordVere.append(coordRiga)
    coordVere = pd.DataFrame(coordVere)
    fig = plt.figure()
    ax01 = fig.add_subplot(1,1,1)
    if numerocl!=0:
        ax01 = sns.heatmap(coordVere.T, yticklabels=labelvar, cmap=colorset)
    else:
        ax01 = sns.heatmap(coordVere.T, yticklabels=labelvar, cbar=True, cmap=colorset)
    ax01.set_yticklabels(ax01.get_yticklabels(), rotation=0)
    ax01.set_title("Heatmap")
    
    return fig

def highlight_cluster(percorsoD, percorsoS, numerocl, usedV):
    
    """
    Caricamento dati
    """
    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    new_coN, new_coV = used_coord(percorsoD, percorsoS, usedV, numerocl)
    righe,colonne = new_coN.shape
    coordinateVv = new_coV.values
    coordinateNn = new_coN.values
    
    used_variables = []
    for i in range(0, righe):
        if i+1 != numerocl:
             for j in range(0, colonne):
                 coordinateNn[i][j] = 'nan'
        else:    
            for j in range(0, colonne):
                if str(coordinateNn[i][j]) == 'nan':
                    used_variables.append(0)
                else:
                    if coordinateNn[i][j] != 0:
                        coordinateNn[i][j] = 1
                    used_variables.append(1)
                #if str(coordinateNn[i][j]) == 'nan':
                    #coordinateNn[i][j] = -1
    """
    for i in range(0, righe):
        for j in range(0, colonne):
            if (abs(coordinateV[list(coordinateV)[j]]).max()) != 0:
                coordinateVv[i][j] = coordinateVv[i][j]/((abs(coordinateV[list(coordinateV)[j]])).max())
            else:
                coordinateVv[i][j] = coordinateVv[i][j]/1
    """
    for i in range(0, righe):
        if i+1 != numerocl:
            for j in range(0, colonne):
                coordinateVv[i][j] = 'nan'
    
    df, latitude, longitude = used_df(percorsoD, percorsoS, usedV, numerocl)

    """
    IntCatch
    
    longi = df[df.columns[10]]
    longi = longi.values
    lati = df[df.columns[9]]
    lati = lati.values
    lati = [(item*20)for item in lati]
    df.drop(df.columns[10],axis=1, inplace=True) #longitude
    df.drop(df.columns[9],axis=1, inplace=True) #latitude
    
    
    df.drop(df.columns[1],axis=1, inplace=True) #seconds
    df.drop(df.columns[0],axis=1, inplace=True) #data
    """
    seconds = [item for item in range(0, df.shape[0])]
    labelvar = list(df)
    
    #labeltab = list(set(clusternorm))
    
    plt.style.use("classic")
    fig = plt.figure()
    #plt.suptitle("Time series about {} cluster".format(str(numerocl)), fontsize=16)
    color = []
    colorset = []
    for item in clusternorm:
        if item == numerocl:
            color.append(pl.cm.jet(item/len(clustergiusti)))
        else:
            color.append([0.07,0.07,0.07,0.07])
    for item in list(set(clusternorm)):
        if item == numerocl:
            colorset.append(pl.cm.jet(item/len(clustergiusti)))
        else:
            colorset.append([0.07,0.07,0.07,0.07])
    colorlegend = []
    colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[numerocl-1]))
        
    #ax0 = fig.add_subplot(5,3,2)
    #ax0 = tabCentroidi(coordinateVv, labeltab, labelvar)
    #ax0.set_title("Graduation")

    a = [numerocl]
    """
    ax1 = fig.add_subplot(5,3,3)             
    ax1 = to_scatter(ax1, longi, lati, 'longitude', 'latitude', color, colorlegend, a)
    ax1.imshow
    """
    ax2 = fig.add_subplot(4,3,1)
    ax2 = to_scatter(ax2, seconds, clusternorm, 'observations', 'cluster', color, colorlegend, a)
    #ax2.set_xlim(xmin=-100)
    ax2.set_title("Mapping observation to clusters")
    
    su = compute_su(clusternorm, df, numerocl)
    
    j = 0
    for i in range(2, df.shape[1]+2):
        
        pos = su.index(max(su))
        ax3 = fig.add_subplot(4,3,i)
        ax3 = to_scatter(ax3, seconds, df[df.columns[j]], 'observations', labelvar[j], color, colorlegend, a)
        j = j+1
        ax3.set_title("SU: {0:.3f}".format(float(su[pos])))
        #ax3.set_xlim(xmin=-100)
        ax3 = plt.gca()
        if used_variables[i-2]==1:
            print 
            ax3.set_facecolor('#c7fdb5')
        else:
            ax3.set_facecolor('mistyrose')
        su[pos] = -1
       
    if  len(latitude) != 0 and len(longitude) != 0:
        latitude = [(item*20)for item in latitude]
        ax3 = fig.add_subplot(4,3,df.shape[1]+2)
        ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, colorlegend, set(clusternorm))
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3)
    return fig


def disegna_grafici(percorsoD, percorsoS, usedV):
    
    """
    Caricamento dati
    """
    if percorsoS != "/":
        df, latitude, longitude = used_df(percorsoD, percorsoS, usedV)
        clusternorm, clustergiusti, cl = get_cl(percorsoS)
        new_coN, new_coV = used_coord(percorsoD, percorsoS, usedV)
        righe, colonne = new_coN.shape
        coordinateVv = new_coV.values
        coordinateNv = new_coN.values
        """for i in range(0, righe):
            for j in range(0, colonne):
                if (abs(coordinateV[list(coordinateV)[j]]).max()) != 0:
                    coordinateVv[i][j] = coordinateVv[i][j]/((abs(coordinateV[list(coordinateV)[j]])).max())
                else:
                    coordinateVv[i][j] = coordinateVv[i][j]/1
        """        
        for i in range(0, righe):
            for j in range(0, colonne):
                if coordinateNv[i][j] != 0:
                    if str(coordinateNv[i][j]) != 'nan':
                        coordinateNv[i][j] = 1
        color = [pl.cm.jet(item/len(clustergiusti)) for item in clusternorm]
        colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))

    else:
        df, latitudine, longitudine = get_dataset(percorsoD)
        color = [[0,0,1,1] for item in range(0, df.shape[0])]
        colorset = color
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
    
    """
    longi = df[df.columns[10]]
    lati = df[df.columns[9]]
    lati = [(item*20)for item in lati]
    df.drop(df.columns[10],axis=1, inplace=True) #longitude
    df.drop(df.columns[9],axis=1, inplace=True) #latitude
    """
    righe, colonne = df.shape
    seconds = [item for item in range(0, len(df))]
    
    labelvar = list(df)
    #labeltab = list(set(clusternorm))

    """
    Grafici
    """
    
    plt.style.use("classic")
    fig = plt.figure()
    

    #ax02 = fig.add_subplot(6,3,2)
    #ax02 = tabCentroidi(coordinateVv, labeltab, labelvar)
    #ax02.set_title("Graduation")

    #ax1 = fig.add_subplot(5,3,3)   

    #PROVA CON FOLIUM
    """m = folium.Map(location =[np.mean(lati)/10 , np.mean(longi)], zoom_start=16)
    print "points"
    for point in range(0, len(lati)):
        colore = color[point]
        colore = list(colore)
        colore.pop(3)
        colore = [item*255 for item in colore]
        colore = tuple(colore)
        folium.RegularPolygonMarker(location=[lati[point]/10, longi[point]], opacity=0, radius=1, fill_color='#%02x%02x%02x' % colore).add_to(m)
    print "finish"
    m.save(percorsoS+"tmp.html")
    url = "file://"+percorsoS+"tmp.html"
    outfn = percorsoS+"outfig.png"
    subprocess.check_call(["cutycapt","--url={}".format(url), "--out={}".format(outfn)])
    img = plt.imread(percorsoS+"outfig.png")
    ax1.imshow(img)"""
    
    #ax1 = to_scatter(ax1, longi, lati, 'longitude', 'latitude', color, colorlegend, set(clusternorm))
    if percorsoS != "/":
        ax2 = fig.add_subplot(4,3,1)
        ax2 = to_scatter(ax2, seconds, clusternorm, 'observations', 'cluster', color, colorlegend, set(clusternorm))
        #ax2.set_xlim(xmin=-100)
        ax2.set_title("Mapping observation to clusters")
    
        su = compute_su(clusternorm, df)
    
        j = 0
        for i in range(2, colonne+2):
            pos = su.index(max(su))
            ax3 = fig.add_subplot(4,3,i)
            ax3 = to_scatter(ax3, seconds, df[df.columns[j]], 'observations', labelvar[j], color, colorlegend, set(clusternorm))
            ax3.set_title("SU= {0:.3f}".format(float(su[pos])))
            j = j+1
            su[pos] = -1
            #ax3.set_xlim(xmin=-100)
        if  len(latitude) != 0 and len(longitude) != 0:
            latitude = [(item*20)for item in latitude]
            ax3 = fig.add_subplot(4,3,df.shape[1]+2)
            ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, colorlegend, set(clusternorm))
    else:
        j = 0
        x = 1
        for i in range(1, colonne+1):
            if usedV[i-1]==1:
                ax3 = fig.add_subplot(4,3,x)
                ax3 = to_scatter(ax3, seconds, df[df.columns[j]], 'observations', labelvar[j], color, colorlegend, "1")
                x += 1
            j = j+1
            
    
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3)
    
    return fig
    

def disegna_boxplot(percorsoD, percorsoS, usedV):
    
    """
    Caricamento dati
    """
    if percorsoS != "/":
        clusternorm, clustergiusti, cl = get_cl(percorsoS)
        df, latitude, longitude = used_df(percorsoD, percorsoS, usedV)
    else:
        df, latitude, longitude = get_dataset(percorsoD)
    """
    df.drop(df.columns[10],axis=1, inplace=True) #longitude
    df.drop(df.columns[9],axis=1, inplace=True) #latitude
    df.drop(df.columns[1],axis=1, inplace=True) #seconds
    df.drop(df.columns[0],axis=1, inplace=True) #data
    """
    labelvar = list(df)
    
    righe,colonne = df.shape
    
    plt.style.use("classic")
    fig = plt.figure()

    if percorsoS != "/":
        su = compute_su(clusternorm, df)
    
        for i in range(1,colonne+1):
            
            pos = su.index(max(su))
            ax0 = fig.add_subplot(3,4,i)
            freq = [[] for x in clustergiusti]
            r = 0
            for c in clusternorm:
                freq[int(c)-1].append(df.iloc[r,pos])
                r = r+1
            ax0.boxplot(freq)
            ax0.set_xlabel("SU= {0:.3f}".format(float(su[pos])))
            ax0.set_ylabel(labelvar[i-1])
            ax0.grid(True)
            su[pos] = -1
    else:
        x = 1
        for i in range(1,colonne+1):
            if usedV[i-1] == 1:
                ax0 = fig.add_subplot(3,4,x)
                ax0.boxplot(df[df.columns[i-1]])
                ax0.set_ylabel(labelvar[i-1])
                ax0.grid(True)
                x += 1
        
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3)
        
    return fig

def ordina_boxplot(percorsoD, percorsoS, numerocl, usedV):
    
    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    df, latitude, longitude = used_df(percorsoD, percorsoS, usedV, numerocl)
    righe, colonne = df.shape
    new_coN, new_coV = used_coord(percorsoD, percorsoS, usedV, numerocl)
    coordinateNn = new_coN.values
    
    used_variables = []
    for i in range(0, new_coN.shape[0]):
        if i+1 != numerocl:
             for j in range(0, new_coN.shape[1]):
                 coordinateNn[i][j] = 'nan'
        else:    
            for j in range(0, new_coN.shape[1]):
                if str(coordinateNn[i][j]) == 'nan':
                    used_variables.append(0)
                else:
                    used_variables.append(1)
    """
    df.drop(df.columns[10],axis=1, inplace=True) #longitude
    df.drop(df.columns[9],axis=1, inplace=True) #latitude
    df.drop(df.columns[1],axis=1, inplace=True) #seconds
    df.drop(df.columns[0],axis=1, inplace=True) #data
    """
    labelvar = list(df)
    
    righe,colonne = df.shape
    
    su = compute_su(clusternorm, df, numerocl)
    
    plt.style.use("classic")
    fig = plt.figure()
    for i in range(1, colonne+1):

        pos = su.index(max(su))
        ax0 = fig.add_subplot(4,3,i)
        freq = [[] for x in clustergiusti]
        r = 0
        for c in clusternorm:
            freq[int(c)-1].append(df.iloc[r,pos])
            r = r+1
        ax0.boxplot(freq)
        ax0.set_xlabel("SU= {0:.3f}".format(float(su[pos])))
        ax0.set_ylabel(labelvar[i-1])
        ax0.grid(True)
        ax0 = plt.gca()
        if used_variables[i-1] == 1:
            ax0.set_facecolor('#c7fdb5')
        else:
            ax0.set_facecolor('mistyrose')
        su[pos] = -1
        
    points = len(freq[numerocl-1])
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3)
    
    return fig, points, righe
     
def disegna_barplot(percorsoD, percorsoS, usedV):
    
    
    """
    longi = df[df.columns[10]]
    lati = df[df.columns[9]]
    lati = [(item*20)for item in lati]
    df.drop(df.columns[10],axis=1, inplace=True) #longitude
    df.drop(df.columns[9],axis=1, inplace=True) #latitude
    df.drop(df.columns[1],axis=1, inplace=True) #seconds
    df.drop(df.columns[0],axis=1, inplace=True) #data
    """
    if percorsoS != "/":
        clusternorm, clustergiusti, cl = get_cl(percorsoS)
        df, latitude, longitude = used_df(percorsoD, percorsoS, usedV)
        color = [pl.cm.jet(item/len(clustergiusti)) for item in clusternorm]
        colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
    else:
        df, latitute, longitude = get_dataset(percorsoD)
        color = [[0,0,1,1] for item in range(0, df.shape[0])]
        colorset = color
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        
    labelvar = list(df)
    
    righe,colonne = df.shape
    seconds = [item for item in range(0, righe)]
    
    #labeltab = list(set(clusternorm))
    
    """
    Grafici
    """
    
    plt.style.use("classic")
    fig = plt.figure()
    
    
    fig = plt.figure()
    
    if percorsoS != "/":
        su = compute_su(clusternorm, df)
        
        for i in range(1, colonne+1):
            
            pos = su.index(max(su))
            ax0 = fig.add_subplot(4,3,i)
            ax0.hist(x=df[df.columns[pos]], bins=10, color="green")
            plt.title(labelvar[i-1]+"  SU= {0:.3f}".format(float(su[pos])))
            plt.grid(True)
            su[pos] = -1
        ax2 = fig.add_subplot(4,3,colonne+1)
        ax2 = to_scatter(ax2, seconds, clusternorm, 'elements', 'cluster', color, colorlegend, set(clusternorm))
        #ax2.set_xlim(xmin=-100)
        if  len(latitude) != 0 and len(longitude) != 0:
            latitude = [(item*20)for item in latitude]
            ax3 = fig.add_subplot(4,3,df.shape[1]+2)
            ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, colorlegend, set(clusternorm))
        ax2.set_title("Mapping observation to clusters")
    else:
        x = 1
        for i in range(1, colonne+1):
            if usedV[i-1]==1:
                ax0 = fig.add_subplot(4,3,x)
                ax0.hist(x=df[df.columns[i-1]], bins=10, color="green")
                plt.title(labelvar[i-1])
                plt.grid(True)
                x += 1
    #ax1 = fig.add_subplot(4,3,colonne+1)
    #ax1 = to_scatter(ax1, longi, lati, 'longitude', 'latitude', color, colorlegend, set(clusternorm))
    
    
    
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3)
    
    return fig

def highlight_barplot(percorsoD, percorsoS, numerocl, usedV):
    
    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    df, latitude, longitude = used_df(percorsoD, percorsoS, usedV, numerocl)
    righe,colonne = df.shape
    
    new_coN, new_coV = used_coord(percorsoD, percorsoS, usedV, numerocl)
    coordinateNn = new_coN.values
    
    used_variables = []
    for i in range(0, new_coN.shape[0]):
        if i+1 != numerocl:
             for j in range(0, new_coN.shape[1]):
                 coordinateNn[i][j] = 'nan'
        else:    
            for j in range(0, new_coN.shape[1]):
                if str(coordinateNn[i][j]) == 'nan':
                    used_variables.append(0)
                else:
                    used_variables.append(1)
    """
    longi = df[df.columns[10]]
    longi = longi.values
    lati = df[df.columns[9]]
    lati = lati.values
    lati = [(item*20)for item in lati]
    df.drop(df.columns[10],axis=1, inplace=True) #longitude
    df.drop(df.columns[9],axis=1, inplace=True) #latitude
    df.drop(df.columns[1],axis=1, inplace=True) #seconds
    df.drop(df.columns[0],axis=1, inplace=True) #data
    """
    labelvar = list(df)
    
    seconds = [item for item in range(0, righe)]
    
    color = []
    colorset = []
    for item in clusternorm:
        if item == numerocl:
            color.append(pl.cm.jet(item/len(clustergiusti)))
        else:
            color.append([0.07,0.07,0.07,0.07])
    for item in list(set(clusternorm)):
        if item == numerocl:
            colorset.append(pl.cm.jet(item/len(clustergiusti)))
        else:
            colorset.append([0.07,0.07,0.07,0.07])
    colorlegend = []
    colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[numerocl-1]))
    
    fig = plt.figure()  
    plt.style.use("classic")
    
    su = compute_su(clusternorm, df, numerocl)
    
    for i in range(1, colonne+1):
        
        pos = su.index(max(su))
        ax0 = fig.add_subplot(4,3,i)
        bins=10
        ahist, abins = np.histogram(df[df.columns[pos]], bins)
        freq = [[] for x in clustergiusti]
        r = 0
        for c in clusternorm:
            freq[int(c)-1].append(df.iloc[r, pos])
            r = r+1
        bhist, bbins, _ = ax0.hist(x=[freq[numerocl-1], df[df.columns[pos]]], color=[(0,0,0,0), (0,0,0,0)], bins=bins, rwidth=1, edgecolor="none", stacked=True)
        w = (bbins[1] - bbins[0])
        ax0.remove()
        ax0 = fig.add_subplot(4,3,i)
        ax0.set_title(labelvar[i-1]+"  SU={0:.3f}".format(float(su[pos])))
        plt.grid(True)
        ax0.bar(abins[:-1], ahist, width=w, color='green')
        ax0.bar(abins[:-1], bhist[1]-ahist, width=w, color='yellow')
        ax0 = plt.gca()
        if used_variables[i-1] == 1:
            ax0.set_facecolor('#c7fdb5')
        else:
            ax0.set_facecolor('mistyrose')
        su[pos] = -1
    
    punti = len(freq[numerocl-1])
    #ax1 = fig.add_subplot(4,3,colonne+1)
    #ax1 = to_scatter(ax1, longi, lati, 'longitude', 'latitude', color, colorlegend, [numero])
    
    ax2 = fig.add_subplot(4,3,colonne+1)
    ax2 = to_scatter(ax2, seconds, clusternorm, 'elements', 'cluster', color, colorlegend, [numerocl])    
    #ax2.set_xlim(xmin=-100)
    ax2.set_title("Mapping observation to clusters")
    if  len(latitude) != 0 and len(longitude) != 0:
        latitude = [(item*20)for item in latitude]
        ax3 = fig.add_subplot(4,3,df.shape[1]+2)
        ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, colorlegend, set(clusternorm))
    
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3)
    
    return fig, punti, righe

def scatter_2d(percorsoD, percorsoS, var1, var2):
    
    if percorsoS != "/":
        clusternorm, clustergiusti, cl = get_cl(percorsoS)
        df, latitude, longitude = get_dataset(percorsoD)
        color = [pl.cm.jet(item/len(clustergiusti)) for item in clusternorm]
        colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
    else:
        df, latitude, longitude = get_dataset(percorsoD)
        color = [[0,0,1,1] for item in range(0, df.shape[0])]
        colorset = color
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
    labels = list(df)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    if percorsoS != "/":
        ax = to_scatter(ax, df[df.columns[var1]], df[df.columns[var2]], labels[var1], labels[var2], color, colorlegend, set(clusternorm))
    else:
        ax = to_scatter(ax, df[df.columns[var1]], df[df.columns[var2]], labels[var1], labels[var2], color, colorlegend, ["1"])        
    ax.set_title("2D Scatter plot")
    return fig

def scatter_3d(percorsoD, percorsoS, var1, var2, var3):
    
    if percorsoS != "/":
        clusternorm, clustergiusti, cl = get_cl(percorsoS)
        df, latitude, longitude = get_dataset(percorsoD)
        color = [pl.cm.jet(item/len(clustergiusti)) for item in clusternorm]
        colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
    else:
        df, latitude, longitude = get_dataset(percorsoD)
        color = [[0,0,1,1] for item in range(0, df.shape[0])]
        colorset = color
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
            
    labels = list(df)
    
     
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    if percorsoS != "/":
        ax.scatter(xs=df[df.columns[var1]], ys=df[df.columns[var2]], zs=df[df.columns[var3]], c=color, edgecolors='face', s=2)
        ax.set_xlabel(labels[var1])
        ax.set_ylabel(labels[var2])
        ax.set_zlabel(labels[var3])
        ax.grid(True)
        ax.legend(colorlegend, set(clusternorm), loc=4, fontsize=8, ncol=len(set(clusternorm)))
    else:
        ax.scatter(xs=df[df.columns[var1]], ys=df[df.columns[var2]], zs=df[df.columns[var3]], c=color, edgecolors='face', s=2)
        ax.set_xlabel(labels[var1])
        ax.set_ylabel(labels[var2])
        ax.set_zlabel(labels[var3])
        ax.grid(True)
        ax.legend(colorlegend, ["1"], loc=4, fontsize=8, ncol=1)
    ax.set_title("3D Scatter plot")
    return fig

def general_info(percorsoD, percorsoS):
    try:
        clusternorm, clustergiusti, cl = get_cl(percorsoS)
        df, latitude, longitude = get_dataset(percorsoD)
        """
        df.drop(df.columns[10],axis=1, inplace=True) #longitude
        df.drop(df.columns[9],axis=1, inplace=True) #latitude
        df.drop(df.columns[1],axis=1, inplace=True) #seconds
        df.drop(df.columns[0],axis=1, inplace=True) #data
        """ 
        righe,colonne = df.shape
        
        for i in range(1,colonne+1):
            
            freq = [[] for x in clustergiusti]
            r = 0
            for c in clusternorm:
                freq[int(c)-1].append(df.iloc[r,i-1])
                r = r+1
        elementi = [len(item) for item in freq]
        dfEle = pd.DataFrame()
        dfEle["Cluster"] = sorted(set(clusternorm))
        dfEle["N. points"] = elementi
        silhouette = sk.silhouette_samples(df, cl)
        means = []
        
        for item in range(0, len(clustergiusti)):
            sumT = 0
            arraysupp = np.arange(len(cl))
            arraysupp = [(item+1) for i in arraysupp]
            indexes = [i for i,x in enumerate(cl) if x == clustergiusti[item]]
            for i in range(0,len(indexes)):
                sumT += silhouette[indexes[i]]
            means.append(sumT/len(indexes))
        dfEle["Silhouette"] = means
        
        """
        evalu = script.generate_evaluation(cl, np.full(len(cl), -1))
        dfEvalu = pd.DataFrame()
        listName = ["Accuracy", "CE", "F1", "Entropy", "NbCluster"]
        i=0
        for item in listName:
            dfEvalu[item] = [evalu[i]]
            i += 1
        """
        dfGeneral = pd.read_csv(percorsoS+"generalInfo.csv", index_col=False)
    except:
        raise ValueError
    return dfEle, dfGeneral
  
def sort_var(percorsoD, percorsoS, numerocl=0):
    
    clusternorm, clustergiusti, cl= get_cl(percorsoS)
    df, latitude, longitude = get_dataset(percorsoD)
    su = compute_su(clusternorm, df, numerocl)
    new_order = []
    for i in range(0, df.shape[1]):
        pos = su.index(max(su))
        new_order.append(pos)
        su[pos] = -1
    return new_order

def compute_su(clusternorm, df, numerocl=0):
    
    su = []
    mask = np.copy(clusternorm)
    if numerocl != 0:
        for i in range(0, len(mask)):
            if mask[i] == numerocl:
                mask[i] = 1
            else:
                mask[i] = 0
    for i in range(0, df.shape[1]):
        colonna = np.array(df[df.columns[i]])
        su.append(SU.SU(i, feature=colonna, solution=mask))
    return su

def get_dataset(percorsoD):

    ds = open(percorsoD)
    dialect = csv.Sniffer().sniff(ds.read(10000))
    ds.close()
    df = pd.read_csv(percorsoD, sep=dialect.delimiter)
    
    labelvar = list(df)
    latitude = []
    longitude = []
    if "latitude" in labelvar:
        latitude = df[df.columns[labelvar.index('latitude')]]
        df.drop(df.columns[labelvar.index('latitude')],axis=1, inplace=True)
    if "longitude" in labelvar:
        longitude = df[df.columns[labelvar.index('longitude')-1]]
        df.drop(df.columns[labelvar.index('latitude')],axis=1, inplace=True)
    colonne = df.shape[1]-1
    for column in range(0, df.shape[1]):
        colonna = df[df.columns[colonne]]
        boolD = False
        for value in colonna:
            if re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', str(value)) != None:
                if boolD != True:
                    boolD = True
        if boolD == True:
            df.drop(df.columns[colonne], axis=1, inplace=True)
                #break
        colonne-=1
    colonne = df.shape[1]-1    
    for column in range(0, df.shape[1]):
        colonna = df[df.columns[colonne]]
        for value in colonna:
                foo = re.search('[a-zA-Z]', str(value))
                if re.search('[a-zA-Z]', str(value)) != None and foo.string[foo.start():foo.end()] != 'e' :
                    print foo.string[foo.start():foo.end()]
                    raise ValueError("Non-literal values in dataset") 
        colonne-=1
    return df, latitude, longitude

def get_cl(percorsoS):
    
    cl = open(percorsoS+'cl.txt','r').readlines()
    cl = [float(item) for item in cl]
    clusternorm = np.copy(cl)
    clustergiusti = sorted(set(cl))
    for item in range(0, len(clustergiusti)):
        arraysupp = np.arange(len(cl))
        arraysupp = [(item+1) for i in arraysupp]
        indexes = [i for i,x in enumerate(cl) if x == clustergiusti[item]]
        for i in range(0,len(indexes)):
            clusternorm[indexes[i]] = arraysupp[indexes[i]]
    return clusternorm, clustergiusti, cl

def used_df(percorsoD, percorsoS, usedV, numero=0):
    
    df, latitude, longitude = get_dataset(percorsoD)
    if numero !=0:
        order = sort_var(percorsoD, percorsoS, numero)
    else:
        order = sort_var(percorsoD, percorsoS)
    ord_df = []
    for i in range(0, len(order)):
       ord_df.append(df[df.columns[order[i]]])
    ord_df = pd.DataFrame(ord_df).T
    new_df = []
    for i in range(0, len(usedV)):
        if usedV[i] == 1:
            new_df.append(ord_df[ord_df.columns[i]])
    new_df = pd.DataFrame(new_df).T
    return new_df, latitude, longitude

def used_coord(percorsoD, percorsoS, usedV, numero=0):
    
    coordinateN = pd.read_table(percorsoS+'model_parameters.txt', delim_whitespace=True)
    if numero != 0:
        order = sort_var(percorsoD, percorsoS, numero)
    else:
        order = sort_var(percorsoD, percorsoS)
    ord_coN = []
    for i in range(0, len(order)):
       ord_coN.append(coordinateN[coordinateN.columns[order[i]]])
    ord_coN = pd.DataFrame(ord_coN).T
    new_coN = []
    for i in range(0, len(usedV)):
        if usedV[i] == 1:
            new_coN.append(ord_coN[ord_coN.columns[i]])
    new_coN = pd.DataFrame(new_coN).T
    coordinateV = pd.read_table(percorsoS+'model_parameters.txt', delim_whitespace=True)
    #order = sort_var(percorsoD, percorsoS)
    ord_coV = []
    for i in range(0, len(order)):
       ord_coV.append(coordinateV[coordinateV.columns[order[i]]])
    ord_coV = pd.DataFrame(ord_coV).T
    new_coV = []
    for i in range(0, len(usedV)):
        if usedV[i] == 1:
            new_coV.append(ord_coV[ord_coV.columns[i]])
    new_coV = pd.DataFrame(new_coV).T
    return new_coN, new_coV
