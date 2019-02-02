#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 20:32:56 2018

@author: francesco
"""
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.pylab as pl
import SU
from Tkinter import Label

class XM_clustering_results():
    def __init__(self, pathD, pathS, pathGT):
        self.pathD = pathD
        self.pathS = pathS
        self.pathGT = pathGT
        self.pathDS = ""
        try:
            pd.read_csv(pathS+"dataStandardization.csv")
            self.pathDS = pathS+"dataStandardization.csv"
        except:
            pass
        self.dataset, self.latitude, self.longitude, self.experiments = self.get_dataset()
        self.clusternorm, self.clusterset, self.cl = self.get_cl()
        if self.pathGT != "":
            self.clusternormGT, self.clustersetGT, self.cl = self.get_cl(True)
        self.usedDataset = pd.DataFrame(self.dataset)
        self.usedClusternorm, self.usedClusterset, self.usedCl = self.clusternorm, self.clusterset, self.cl
        self.color = [pl.cm.jet(item/len(self.clusterset)) for item in self.clusternorm]
        self.colorset = [pl.cm.jet(item/len(self.clusterset)) for item in list(set(self.clusternorm))]
        self.colorlegend = []
        for i in range(0,len(self.colorset)):
            self.colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=self.colorset[i]))
        self.usedColor = []
        self.method = ""
    
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
            print "Non-numerical values in dataset"
            raise ValueError
        return df, latitude, longitude, experiment
    
    def get_cl(self, GT=False):
        if GT:
            cl = open(self.pathGT, 'r').readlines()
        else:
            cl = open(self.pathS+'cl.txt','r').readlines()
        cl = [float(item) for item in cl]
        clusternorm = np.copy(cl)
        clusterset = sorted(set(cl))
        for item in range(0, len(clusterset)):
            arraysupp = np.arange(len(cl))
            arraysupp = [(item+1) for i in arraysupp]
            indexes = [i for i,x in enumerate(cl) if x == clusterset[item]]
            for i in range(0,len(indexes)):
                clusternorm[indexes[i]] = arraysupp[indexes[i]]
        return clusternorm, clusterset, cl
    
    def change_df(self, norm, usedV, exp="All", numbercl=0, GT=False):
        use = list(np.copy(usedV))
        use = [bool(item) for item in use]
        if len(self.latitude) > 0:
            del(use[0])
        if self.pathS != "":
            del(use[0])
        order = self.sort_var(GT, numbercl)
        ord_df = self.dataset[self.dataset.columns[order]].T
        used_df = ord_df[use]
        use_cn, use_cs, use_cl = self.clusternorm, self.clusterset, self.cl
        use_color = self.color
        if exp != "All":
            exps = list(pd.unique(self.experiments))
            delimI = list(self.experiments).index(exp)
            if exps.index(exp)+1 < len(exps):
                delimF = list(self.experiments).index(exps[exps.index(exp)+1])-1
            else:
                delimF = len(self.experiments)
            used_df = used_df[delimI:delimF]
            use_cn, use_cs, use_cl = self.clusternorm[delimI:delimF],self.clusterset[delimI:delimF],self.cl[delimI:delimF]
            use_color = self.color[delimI:delimF]
        if numbercl != 0:
            use_color[np.argwhere(use_cn != numbercl)] = [0.07,0.07,0.07,0.07]
        self.usedDataset = used_df
        self.usedClusternorm, self.usedClusterset, self.usedCl = use_cn, use_cs, use_cl
        self.usedColor = use_color
    
    def sort_var(self, GT=False, numbercl=0):
        if GT:
            su = self.compute_su(self.clusternormGT, self.dataset, numbercl)
        else:
            su = self.compute_su(self.clusternorm, self.dataset, numbercl)
        return np.argsort(su)[::-1][:len(su)] #descending
    
    def compute_su(self, clusternorm, df, numbercl=0):
        su = []
        mask = np.copy(clusternorm)
        if numbercl != 0:
            for i in range(0, len(mask)):
                if mask[i] == numbercl:
                    mask[i] = 1
                else:
                    mask[i] = 0
        for i in range(0, df.shape[1]):
            colonna = np.array(df[df.columns[i]])
            su.append(SU.SU(i, feature=colonna, solution=mask))
        return su
    
    def general_info(self):
        clusters = sorted(set(self.clusternorm))
        clusters = [int(item) for item in clusters]
        dfEle = pd.DataFrame()
        firstC = []
        secondC = []
        fileGeneral = open(self.pathS+"generalInfo.csv", 'r')
        l = 0
        meansI = []
        meansN = []
        elementi = []
        use = []
        for lines in fileGeneral:
            l += 1
            if l < 6:
                firstC.append(lines.split(",")[0])
                secondC.append(lines.split(",")[1].strip())
            if l == 6:
                firstC.append(lines.split(",")[0])
                self.method = lines.split(",")[1].strip()
                secondC.append(self.method)
            if l > 6 and l <= 16 and self.method == "SubCMedians":
                firstC.append(lines.split(",")[0])
                secondC.append(lines.split(",")[1].strip())
            if l == 18 and self.method == "SubCMedians":
                line = lines.split(",")
                firstC.append(line[0])
                del line[0]
                line = [item.strip() for item in line]
                secondC.append(str(line))
            if (l == 19 or l == 20) and self.method == "SubCMedians":
                firstC.append(lines.split(",")[0])
                secondC.append(lines.split(",")[1].strip())
            if l > 20 and self.method == "SubCMedians":
                meansI.append(lines.split(",")[0])
                meansN.append(lines.split(",")[1].strip())
                elementi.append(lines.split(",")[2].strip())
                use.append(lines.split(",")[3].strip())
            if l > 6 and l < 14 and (self.method == "K-Means" or self.method == "GMM" or self.method == "Spectral Clustering"):
                firstC.append(lines.split(",")[0])
                secondC.append(lines.split(",")[1].strip())
            if l == 15 and self.method == "K-Means":
                line = lines.split(",")
                firstC.append(line[0])
                del line[0]
                line = [item.strip() for item in line]
                secondC.append(str(line))
            if (l == 16 or l == 17) and self.method == "K-Means":
                firstC.append(lines.split(",")[0])
                secondC.append(lines.split(",")[1].strip())
            if l > 17 and self.method == "K-Means":
                meansN.append(lines.split(",")[0].strip())
                elementi.append(lines.split(",")[1].strip())
                use.append(lines.split(",")[2].strip())
            if l == 16 and self.method == "GMM":
                line = lines.split(",")
                firstC.append(line[0])
                del line[0]
                line = [item.strip() for item in line]
                secondC.append(str(line))
            if (l == 17 or l == 18) and self.method == "GMM":
                firstC.append(lines.split(",")[0])
                secondC.append(lines.split(",")[1].strip())
            if l > 18 and self.method == "GMM":
                meansN.append(lines.split(",")[0].strip())
                elementi.append(lines.split(",")[1].strip())
                use.append(lines.split(",")[2].strip())
            if l == 15 and self.method == "Spectral Clustering":
                line = lines.split(",")
                firstC.append(line[0])
                del line[0]
                line = [item.strip() for item in line]
                secondC.append(str(line))
            if l == 16 and self.method == "Spectral Clustering":
                firstC.append(lines.split(",")[0])
                secondC.append(lines.split(",")[1].strip())
            if l > 16 and self.method == "Spectral Clustering":
                meansN.append(lines.split(",")[0].strip())
                elementi.append(lines.split(",")[1].strip())
                use.append(lines.split(",")[2].strip())
        dfGeneral = pd.DataFrame()
        nameF = firstC[0]
        nameS = secondC[0]
        del firstC[0]
        del secondC[0]
        dfGeneral[str(nameF)] = firstC
        dfGeneral[str(nameS)] = secondC
        meansI = [float(item) for item in meansI]
        meansN = [float(item) for item in meansN]
        if self.method == "SubCMedians":
            dfEle["Model"] = clusters
            dfEle["N. points"] = elementi
            dfEle["Sil. in Subspace"] = meansI
            dfEle["Silhouette"] = meansN
            dfEle["N. variables"] = use
            dfEle = dfEle.sort_values("Sil. in Subspace", ascending=False)
        if self.method == "K-Means" or self.method == "GMM" or self.method == "Spectral Clustering":
            dfEle["Model"] = clusters
            dfEle["N. points"] = elementi
            dfEle["Silhouette"] = meansN
            dfEle["N. variables"] = use
            dfEle = dfEle.sort_values("Silhouette", ascending=False)
        return dfEle, dfGeneral
    
    def to_scatter(self, ax, x, y, labelx, labely, color, colorlegend, legendlabel):
        ax.scatter(x, y, c=color, edgecolors='face', s=2)
        ax.set_xlabel(labelx)
        ax.set_ylabel(labely)
        ax.grid(True)
        ax.set_xlim(xmin=min(x)-0.05*(max(x)-min(x)), xmax=max(x)+0.05*(max(x)-min(x)))
        ax.set_ylim(ymin=min(y)-0.05*(max(y)-min(y)), ymax=max(y)+0.05*(max(y)-min(y)))
        #ax.legend(colorlegend, legendlabel, loc=4, fontsize=8, ncol=len(legendlabel))
        return ax
    
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
    
    def draw_timeseries(self, norm, usedV, exp):
        plt.style.use("classic")
        fig = plt.figure(facecolor='white') 
        
        clust, geo = "", ""
        if len(self.latitude) > 0:
            geo = usedV.pop(1)
        if self.pathS != "/":
            clust = usedV.pop(0)
            seconds = range(0, len(self.usedClusternorm))
            righe, colonne = self.usedDataset.shape
            labelvar = list(self.usedDataset)
            
            su = self.compute_su(self.usedClusternorm, self.usedDataset)
            j = 0
            expsI = list(pd.unique(self.experiments))
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
            if clust == 1:
                ax2 = fig.add_subplot(4,3,start)
                ax2 = self.to_scatter(ax2, seconds, self.usedClusternorm, 'observations', 'cluster', self.color, self.colorlegend, set(self.clusternorm))
                ax2.set_title("Mapping observation to clusters")
                if len(expsI) > 1:
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
                start += 1
            if  geo == 1:
                ax3 = fig.add_subplot(4,3,start)
                ax3 = self.to_scatter(ax3, self.longitude, self.latitude, 'longitude', 'latitude', self.color, self.colorlegend, set(self.clusternorm))            
                ax3.set_title("Geo-localization")
                start += 1
            for i in range(start, colonne+start):
                pos = su.index(max(su))
                ax3 = fig.add_subplot(4,3,i)
                ax3 = self.to_scatter(ax3, seconds, self.usedDataset[self.usedDataset.columns[j]], 'observations', labelvar[j], self.color, self.colorlegend, set(self.clusternorm))
                ax3.set_title("SU= {0:.3f}".format(float(su[pos])))
                if len(expsI) > 1:
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
                j = j+1
                su[pos] = -1
        else:
            color = [[0,0,1,1] for item in range(0, self.dataset.shape[0])]
            colorset = color
            colorlegend = []
            for i in range(0,len(colorset)):
                colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
            seconds = range(0, self.dataset.shape[0])
            righe, colonne = self.dataset.shape
            labelvar = list(self.dataset)
        """
        Grafici
        """
        """  
        #ax1 = to_scatter(ax1, longi, lati, 'longitude', 'latitude', color, colorlegend, set(clusternorm))
        if self.pathS != "/":
            su = self.compute_su(self.clusternorm, self.usedDataset)
            j = 0
            expsI = list(pd.unique(self.experiments))
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
            if clust == 1:
                ax2 = fig.add_subplot(4,3,start)
                ax2 = self.to_scatter(ax2, seconds, self.clusternorm, 'observations', 'cluster', color, colorlegend, set(self.clusternorm))
                ax2.set_title("Mapping observation to clusters")
                if len(expsI) > 1:
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
                start += 1
            if  geo == 1:
                ax3 = fig.add_subplot(4,3,start)
                ax3 = self.to_scatter(ax3, self.longitude, self.latitude, 'longitude', 'latitude', color, colorlegend, set(self.clusternorm))            
                ax3.set_title("Geo-localization")
                start += 1
            for i in range(start, colonne+start):
                pos = su.index(max(su))
                ax3 = fig.add_subplot(4,3,i)
                ax3 = self.to_scatter(ax3, seconds, self.usedDataset[self.usedDataset.columns[j]], 'observations', labelvar[j], color, colorlegend, set(self.clusternorm))
                ax3.set_title("SU= {0:.3f}".format(float(su[pos])))
                if len(expsI) > 1:
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
                j = j+1
                su[pos] = -1
        else:
            j = 0
            x = 1
            expsI = list(pd.unique(self.experiments))
            if len(expsI) > 1 :
                delimF = []
                for exp in expsI:
                    delimF.append(next((i-1 for i in range(0,len(self.experiments)) if self.experiments[i]==exp)))
                lastF = delimF[0]
                if lastF == -1:
                    lastF += len(self.experiment)
                del(delimF[0])
                delimF.append(lastF)
            for i in range(1, colonne+1):
                if usedV[i-1]==1:
                    ax3 = fig.add_subplot(4,3,x)
                    if len(expsI) > 1:
                        for xc in delimF:
                            plt.axvline(x=xc, color="red")
                    ax3 = self.to_scatter(ax3, seconds, self.usedDataset[self.usedDataset.columns[j]], 'observations', labelvar[j], color, colorlegend, "1")
                    x += 1
                j = j+1
        """
        plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3)
        return fig