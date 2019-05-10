#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 12:13:26 2019

@author: francesco
"""
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.pylab as pl
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap
import math
from tkinter import Label


class XM_only_data():
    def __init__(self, pathD):
        self.pathD = pathD
        self.pathS = "/"
        self.pathGT = ""
        self.dataset, self.latitude, self.longitude, self.experiments = self.get_dataset()
        self.usedDataset = pd.DataFrame(self.dataset)
        self.color = [[0,0,1,1] for item in range(self.dataset.shape[0])]
        self.colorset = [0,0,1,1]
        self.usedColor = None
        self.fig = None
        self.exp = None
        self.usedV = [0 for i in range(self.dataset.shape[1]+1)]
        self.numbercl = 0
        
    def get_dataset(self):
        ds = open(self.pathD)
        dialect = csv.Sniffer().sniff(ds.read(10000))
        ds.close()
        df = pd.read_csv(self.pathD, sep=dialect.delimiter)
        labelvar = list(df)
        latitude = []
        longitude = []
        experiment = []
        if "experiment" in labelvar:
            experiment = df[df.columns[labelvar.index('experiment')]]
            df.drop(df.columns[labelvar.index('experiment')],axis=1, inplace=True)
        labelvar = list(df)
        if "latitude" in labelvar:
            latitude = df[df.columns[labelvar.index('latitude')]]
            df.drop(df.columns[labelvar.index('latitude')],axis=1, inplace=True)
        labelvar = list(df)
        if "longitude" in labelvar:
            longitude = df[df.columns[labelvar.index('longitude')]]
            df.drop(df.columns[labelvar.index('longitude')],axis=1, inplace=True)
        try:
            df = df.astype(float)
        except:
            print("[XM]> Non-numerical values in dataset.")
            raise ValueError
        return df, latitude, longitude, experiment   

    def change_df(self, usedV, exp="All", GT=False):
        use = list(np.copy(usedV))
        use = [bool(item) for item in use]
        if len(self.latitude) > 0:
            del(use[0])
        tmp_df = pd.DataFrame(self.dataset).copy()
        used_df = tmp_df.T[use]
        use_lat, use_long = self.latitude, self.longitude
        use_color = np.copy(self.color)
        if exp != "All":
            exps = list(pd.unique(self.experiments))
            delimI = list(self.experiments).index(exp)
            if exps.index(exp)+1 < len(exps):
                delimF = list(self.experiments).index(exps[exps.index(exp)+1])-1
            else:
                delimF = len(self.experiments)
            used_df = used_df.iloc[:,delimI:delimF]
            use_color = use_color[delimI:delimF]
            use_lat, use_long = self.latitude[delimI:delimF], self.longitude[delimI:delimF]
        self.usedDataset = used_df.T
        self.usedColor = use_color
        self.usedLatitude, self.usedLongitude = use_lat, use_long     
        
    def to_scatter(self, ax, x, y, labelx, labely, color, colorlegend, legendlabel):
        ax.scatter(x, y, c=color, edgecolors='face', s=2)
        ax.set_xlabel(labelx)
        ax.set_ylabel(labely)
        ax.grid(True)
        ax.set_xlim(left=min(x)-0.05*(max(x)-min(x)), right=max(x)+0.05*(max(x)-min(x)))
        ax.set_ylim(bottom=min(y)-0.05*(max(y)-min(y)), top=max(y)+0.05*(max(y)-min(y)))
        return ax
    
    def heatmap(self, ax, data, title = None, labelx = None, labely = None, labelxticks = None, labelyticks = None, cmap = None):
        if cmap == None:
            cmap = 'summer_r'
        im = ax.imshow(data, cmap=cmap, aspect='auto', interpolation = 'nearest')
        ax.set_title(title)
        ax.set(xlabel=labelx, ylabel=labely)
        if labelxticks != None:
            ax.set_xticks(range(len(labelxticks)))
            ax.set_xticklabels(labelxticks)
        if labelyticks != None:
            ax.set_yticks(range(len(labelyticks)))
            ax.set_yticklabels(labelyticks, rotation = 0)
        return im 
        
    def add_subplot_zoom(self, figure):
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
        
        
    def heat_ds(self, norm, exp):

        if self.exp != exp:
            self.exp = exp
            self.change_df(self.usedV, exp)
        plt.style.use("default")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white') 
        ds = pd.DataFrame(self.dataset).copy()
        if exp != "All":
            exps = list(pd.unique(self.experiments))
            delimI = list(self.experiments).index(exp)
            if exps.index(exp)+1 < len(exps):
                delimF = list(self.experiments).index(exps[exps.index(exp)+1])-1
            else:
                delimF = len(self.experiments)
            ds = pd.DataFrame(ds.iloc[delimI:delimF,:]).copy()
        ax = self.fig.add_subplot(1,1,1)
        im = self.heatmap(ax, ds.T, title="Dataset Heatmap", labelx="Time [sec]", labely="Variables", labelyticks=list(self.dataset))
        plt.colorbar(im)    
        if len(list(pd.unique(self.experiments))) > 1 and exp == 'All':
            expsI = list(pd.unique(self.experiments))
            delimF = []
            for exp in expsI:
                delimF.append(next((i-1 for i in range(0,len(self.experiments)) if self.experiments[i]==exp)))
            lastF = delimF[0]
            if lastF == -1:
                lastF += len(self.experiments)
            del(delimF[0])
            delimF.append(lastF)
            for xc in delimF:
                plt.axvline(x=xc, color='red')
        plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3, right=1, left=0.15)
        return self.fig
    
    
    def draw_timeseries(self, norm, usedV, exp, GT=False):
        if self.exp != exp or (not (np.array((usedV==self.usedV)).all())):
            self.exp = exp
            self.usedV = usedV
            self.change_df(usedV, exp)
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white') 
        
        geo =  0
        if len(self.latitude) > 0:
            geo = usedV[0]
        seconds = range(self.usedDataset.shape[0])
        labelvar = list(self.usedDataset)
        columns = self.usedDataset.shape[1]
        if exp == 'All':
            expsI = list(pd.unique(self.experiments))
        else:
            expsI = []
        if len(expsI) > 1 :
            delimF = []
            for exp in expsI:
                delimF.append(next((i-1 for i in range(0,len(self.experiments)) if self.experiments[i]==exp)))
            lastF = delimF[0]
            if lastF == -1:
                lastF += len(self.experiments)
            del(delimF[0])
            delimF.append(lastF)
        start = 1
        if  geo == 1:
                ax3 = self.fig.add_subplot(4,3,start)
                ax3 = self.to_scatter(ax3, self.usedLongitude, self.usedLatitude, 'longitude', 'latitude', self.usedColor, "", "")            
                ax3.set_title("Geo-localization")
                start += 1
        for i in range(start, columns+start):
            ax3 = self.fig.add_subplot(4,3,i)
            ax3 = self.to_scatter(ax3, seconds, self.usedDataset[self.usedDataset.columns[i-start]], 'observations', labelvar[i-start], self.usedColor, "", "")
            #ax3.set_title("SU= {0:.3f}".format(float(su[pos])))
            if len(expsI) > 1:
                for xc in delimF:
                    plt.axvline(x=xc, color="red")
        plt.subplots_adjust(top = 0.95, bottom = 0.09, wspace = 0.3, right=0.96, left=0.06, hspace=0.55)
        return self.fig
        
        
    def scatter_2d(self, norm, var1, var2, numbercl=0, exp="All", GT=False):
        if self.exp != exp:
            self.exp = exp
            self.change_df(self.usedV, exp, GT) 
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
        
        color = np.array(self.color, copy=True)
        current_data = pd.DataFrame(self.dataset).copy()
        if exp != "All":
            exps = list(pd.unique(self.experiments))
            delimI = list(self.experiments).index(exp)
            if exps.index(exp)+1 < len(exps):
                delimF = list(self.experiments).index(exps[exps.index(exp)+1])-1
            else:
                delimF = len(self.experiments)
            current_data = pd.DataFrame(self.dataset.iloc[delimI:delimF,:]).copy()
            color = color[delimI:delimF]
        labels = list(self.dataset)
        ax = self.fig.add_subplot(1,1,1)
        ax = self.to_scatter(ax, current_data[labels[var1]], current_data[labels[var2]], labels[var1], labels[var2], color, "", "")
        ax.set_title("2D Scatter plot")
        return self.fig

    def scatter_3d(self, norm, fig, var1, var2, var3, numbercl=0, exp="All", GT=False):
            
        if self.exp != exp:
            self.exp = exp
            self.change_df(self.usedV, exp, GT) 
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
       
        color = np.array(self.color, copy=True)
        
        current_data = pd.DataFrame(self.dataset).copy()
        if exp != "All":
            exps = list(pd.unique(self.experiments))
            delimI = list(self.experiments).index(exp)
            if exps.index(exp)+1 < len(exps):
                delimF = list(self.experiments).index(exps[exps.index(exp)+1])-1
            else:
                delimF = len(self.experiments)
            current_data = pd.DataFrame(self.dataset.iloc[delimI:delimF,:]).copy()
            color = color[delimI:delimF]
        labels = list(self.dataset)
        ax = fig.gca(projection='3d')
        ax.scatter(xs=current_data[labels[var1]], ys=current_data[labels[var2]], zs=current_data[labels[var3]], c=color, edgecolors='face', s=2)
        ax.set_xlabel(labels[var1])
        ax.set_ylabel(labels[var2])
        ax.set_zlabel(labels[var3])
        ax.grid(True)
        ax.set_title("3D Scatter plot")
        return fig
    
    def draw_boxplot(self, meansI, norm, usedV, exp, GT=False):
        if self.exp != exp or (not (np.array((usedV==self.usedV)).all())):
            self.exp = exp
            self.usedV = usedV
            self.change_df(usedV, exp)
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
        
        geo = 0
        if len(self.latitude) > 0:
            geo = usedV[0]
        start = 1
        labelvar = list(self.usedDataset)
        columns = self.usedDataset.shape[1]
        if  geo == 1:
            ax3 = self.fig.add_subplot(4,3,start)
            ax3 = self.to_scatter(ax3, self.usedLongitude, self.usedLatitude, 'longitude', 'latitude', self.usedColor, "", "")            
            ax3.set_title("Geo-localization")
            start += 1
        for i in range(start,columns+start):
            ax0 = self.fig.add_subplot(3,4,i)
            ax0.boxplot(self.usedDataset[self.usedDataset.columns[i-start]])
            ax0.set_ylabel(labelvar[i-start])
            ax0.grid(True)
        plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3, right=0.96, left=0.06)
        return self.fig
    
    def draw_barplot(self, norm, usedV, exp, GT=False):
        if self.exp != exp or (not (np.array((usedV==self.usedV)).all())):
            self.exp = exp
            self.usedV = usedV
            self.change_df(usedV, exp)
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
        
        geo = 0
        if len(self.latitude) > 0:
            geo = usedV[0]
        start = 1
        labelvar = list(self.usedDataset)
        columns = self.usedDataset.shape[1]
        if  geo == 1:
            ax3 = self.fig.add_subplot(4,3,start)
            ax3 = self.to_scatter(ax3, self.usedLongitude, self.usedLatitude, 'longitude', 'latitude', self.usedColor, "", "")            
            ax3.set_title("Geo-localization")
            start += 1
        for i in range(start,columns+start):
            ax0 = self.fig.add_subplot(3,4,i)
            ax0.hist(self.usedDataset[self.usedDataset.columns[i-start]], bins=20, color="green")
            ax0.set_ylabel(labelvar[i-start])
            ax0.grid(True)
        plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3, right=0.96, left=0.06)
        return self.fig
    
    
    def geo_localization(self, usedExp="", numbercl=0, exp="All", GT=False):
        
        if self.exp != exp:
            self.exp = exp
            self.change_df(self.usedV, exp) 
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
        
        
        color = np.array(self.color)
        if exp == 'All':
            if usedExp != "":
                expsI = list(pd.unique(self.experiments))
                exps = []
                for i in range(0,len(usedExp)):
                    if usedExp[i] == 1:
                        exps.append(expsI[i])
            delimI = []
            delimF = []
            for exp in expsI: 
                delimI.append(next((i for i in range(0,len(self.experiments)) if self.experiments[i]==exp)))
            for exp in expsI:
                delimF.append(next((i-1 for i in range(0,len(self.experiments)) if self.experiments[i]==exp)))
            lastF = delimF[0]
            if lastF == -1:
                lastF += len(self.experiments)
            del(delimF[0])
            delimF.append(lastF)
            uDelimI = []
            uDelimF = []
            for i in range(0, len(usedExp)):
                if usedExp[i] == 1:
                    uDelimI.append(delimI[i])
                    uDelimF.append(delimF[i])
            #delim.append(len(experiment)-1)
            for i in range(1, len(uDelimI)+1):
                ax = self.fig.add_subplot(3,2,i)
                ax = self.to_scatter(ax, self.longitude[uDelimI[i-1]:uDelimF[i-1]], self.latitude[uDelimI[i-1]:uDelimF[i-1]], "longitude", "latitude", color[uDelimI[i-1]:uDelimF[i-1]], "colorlegend", "")
                ax.set_title(exps[i-1])
        else:
            ax = self.fig.add_subplot(1,1,1)
            ax = self.to_scatter(ax, self.usedLongitude, self.usedLatitude, "longitude", "latitude", self.usedColor, "", "")
        
        plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3, right=0.96, left=0.1)
        
        return self.fig