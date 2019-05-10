#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 20:32:56 2018

@author: francesco
"""
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import matplotlib.patches as mpatches
import matplotlib.pylab as pl
#from matplotlib.pyplot import Figure
import SU
from tkinter import Label
#import gc
#import pyximport; pyximport.install(reload_support=True)
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap
import math
#plt.show(block=False)

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
            self.pathDS = None
        self.dataset, self.latitude, self.longitude, self.experiments = self.get_dataset()
        self.clusternorm, self.clusterset, self.cl = self.get_cl()
        if self.pathGT != "":
            self.clusternormGT, self.clustersetGT, self.clGT = self.get_cl(GT=True)
            self.colorGT = [pl.cm.jet(item/len(self.clustersetGT)) for item in self.clusternormGT]
        self.usedDataset = pd.DataFrame(self.dataset)
        self.usedClusternorm, self.usedClusterset, self.usedCl = self.clusternorm, self.clusterset, self.cl
        self.color = [pl.cm.jet(item/len(self.clusterset)) for item in self.clusternorm]
        self.colorset = [pl.cm.jet(item/len(self.clusterset)) for item in list(set(self.clusternorm))]
        self.colorlegend = []
        for i in range(0,len(self.colorset)):
            self.colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=self.colorset[i]))
        #self.usedColor = []
        self.method = ""
        self.fig = None
        self.usedV = [0 for i in range(self.dataset.shape[1]+2)]
        #self.usedV = []
        self.gt = None
        self.numbercl = None
        self.exp = None
        self.norm = None
    
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
        clusterset = sorted(set(clusternorm))
        return clusternorm, clusterset, cl
    
    def change_df(self, norm, usedV, exp="All", GT=False):
        use = list(np.copy(usedV))
        use = [bool(item) for item in use]
        if self.pathS != "":
            del(use[0])
        if len(self.latitude) > 0:
            del(use[0])
        
        order = self.sort_var(GT, self.numbercl)
        tmp_df = pd.DataFrame(self.dataset).copy()
        if norm == False and self.pathDS != None:
            fileDS = pd.read_csv(self.pathDS)
            var = fileDS.shape[0]
            fileDS = fileDS.values
            for i in range(0, var):
                mean = float(fileDS[i][1])
                std = float(fileDS[i][2])
                tmp_df[tmp_df.columns[i]] = tmp_df[tmp_df.columns[i]]*std+mean 
        ord_df = pd.DataFrame(tmp_df[tmp_df.columns[order]].T).copy()
        used_df = ord_df[use]
        use_lat, use_long = self.latitude, self.longitude
        if GT:
            use_cn, use_cs, use_cl = self.clusternormGT, self.clustersetGT, self.clGT
            use_color = np.copy(self.colorGT)
        else:
            use_cn, use_cs, use_cl = self.clusternorm, self.clusterset, self.cl
            use_color = np.copy(self.color)
        if self.numbercl != 0:
            use_color[np.argwhere(use_cn != self.numbercl)] = [0.07,0.07,0.07,0.07]
        if exp != "All":
            exps = list(pd.unique(self.experiments))
            delimI = list(self.experiments).index(exp)
            if exps.index(exp)+1 < len(exps):
                delimF = list(self.experiments).index(exps[exps.index(exp)+1])-1
            else:
                delimF = len(self.experiments)
            used_df = used_df.iloc[:,delimI:delimF]
            use_cn, use_cs, use_cl = use_cn[delimI:delimF],set(use_cn[delimI:delimF]),use_cl[delimI:delimF]
            use_color = use_color[delimI:delimF]
            use_lat, use_long = self.latitude[delimI:delimF], self.longitude[delimI:delimF]
        self.usedDataset = used_df.T
        self.usedClusternorm, self.usedClusterset, self.usedCl = use_cn, use_cs, use_cl
        self.usedColor = use_color
        self.usedLatitude, self.usedLongitude = use_lat, use_long
        #print(len(self.usedClusternorm), len(self.usedLatitude), len(self.usedDataset))
        #print(self.usedDataset)
    
    def used_coord(self, usedV, norm, numbercl=0):
        try:
            coordinateN = pd.read_csv(self.pathS+'model_parameters.txt', delim_whitespace=True)
        except:
            coordinateN = pd.read_csv(self.pathS+'model_parameters0.txt', delim_whitespace=True)
        use = list(np.copy(usedV))
        use = [bool(item) for item in use]
        if len(self.latitude) > 0:
            del(use[0])
            del(use[0])
        else:
            del(use[0])
        if numbercl != 0:
            order = self.sort_var("", numbercl)
        else:
            order = self.sort_var("")
        ord_coN = coordinateN[coordinateN.columns[order]].T
        new_coN = ord_coN[use].T
        return new_coN, new_coN
    
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
    
    def do_inverse_cov(mat):
        matrix = pd.DataFrame(mat).copy()
        matrix_f = pd.DataFrame(mat).copy()
        for i in range(matrix.shape[0]):
            for j in range(i,matrix.shape[1]):
                matrix_f.iloc[i,j] = -(matrix.iloc[i,j]/(math.sqrt(matrix.iloc[i,i]*matrix.iloc[j,j])))
        return matrix_f.values
    
    def check_changes(self, norm, numbercl, usedV, exp, GT):
        if self.numbercl != numbercl or (not (np.array((usedV==self.usedV)).all())) or self.gt != GT or self.exp != exp or self.norm != norm:
            self.numbercl = numbercl
            self.usedV = np.copy(usedV)
            self.gt = GT
            self.exp = exp
            self.norm = norm
            self.change_df(norm, usedV, exp, GT) 
    
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
            if self.method == "SubCMedians":
                if l > 6 and l <= 16:
                    firstC.append(lines.split(",")[0])
                    secondC.append(lines.split(",")[1].strip())
                if l == 18:
                    line = lines.split(",")
                    firstC.append(line[0])
                    del line[0]
                    line = [item.strip() for item in line]
                    secondC.append(str(line))
                if (l == 19 or l == 20):
                    firstC.append(lines.split(",")[0])
                    secondC.append(lines.split(",")[1].strip())
                if l > 20:
                    meansI.append(lines.split(",")[0])
                    meansN.append(lines.split(",")[1].strip())
                    elementi.append(lines.split(",")[2].strip())
                    use.append(lines.split(",")[3].strip())
            if (self.method == "K-Means" or self.method == "GMM" or self.method == "Spectral Clustering"):
                if l > 6 and l < 14:
                    firstC.append(lines.split(",")[0])
                    secondC.append(lines.split(",")[1].strip())
            if self.method == "K-Means":
                if l == 15:
                    line = lines.split(",")
                    firstC.append(line[0])
                    del line[0]
                    line = [item.strip() for item in line]
                    secondC.append(str(line))
                if (l == 16 or l == 17):
                    firstC.append(lines.split(",")[0])
                    secondC.append(lines.split(",")[1].strip())
                if l > 17:
                    meansN.append(lines.split(",")[0].strip())
                    elementi.append(lines.split(",")[1].strip())
                    use.append(lines.split(",")[2].strip())
            if self.method == "GMM":
                if l == 16:
                    line = lines.split(",")
                    firstC.append(line[0])
                    del line[0]
                    line = [item.strip() for item in line]
                    secondC.append(str(line))
                if (l == 17 or l == 18):
                    firstC.append(lines.split(",")[0])
                    secondC.append(lines.split(",")[1].strip())
                if l > 18:
                    meansN.append(lines.split(",")[0].strip())
                    elementi.append(lines.split(",")[1].strip())
                    use.append(lines.split(",")[2].strip())
            if self.method == "Spectral Clustering":
                if l == 15:
                    line = lines.split(",")
                    firstC.append(line[0])
                    del line[0]
                    line = [item.strip() for item in line]
                    secondC.append(str(line))
                if l == 16:
                    firstC.append(lines.split(",")[0])
                    secondC.append(lines.split(",")[1].strip())
                if l > 16:
                    meansN.append(lines.split(",")[0].strip())
                    elementi.append(lines.split(",")[1].strip())
                    use.append(lines.split(",")[2].strip())
            if self.method == "IHMM" or self.method == "HMM":
                if l > 6 and l < 16:
                    firstC.append(lines.split(",")[0])
                    secondC.append(lines.split(",")[1].strip())
                if l == 16:
                    riga = lines.split(",")
                    firstC.append(riga[0])
                    del riga[0]
                    riga = [item.strip() for item in riga]
                    secondC.append(str(riga))
                if (l == 17 or l == 18):
                    firstC.append(lines.split(",")[0])
                    secondC.append(lines.split(",")[1].strip())
                if l > 18:
                    meansN.append(lines.split(",")[0].strip())
                    elementi.append(lines.split(",")[1].strip())
                    use.append(lines.split(",")[2].strip())
            if self.method == "TICC":    
                if l > 6 and l < 18:
                    firstC.append(lines.split(",")[0])
                    secondC.append(lines.split(",")[1].strip())
                if l == 18:
                    riga = lines.split(",")
                    firstC.append(riga[0])
                    del riga[0]
                    riga = [item.strip() for item in riga]
                    secondC.append(str(riga))
                if l >= 19 and l<=22:
                    firstC.append(lines.split(",")[0])
                    secondC.append(lines.split(",")[1].strip())
                if l > 22:
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
        #if self.method == "K-Means" or self.method == "GMM" or self.method == "Spectral Clustering":
        else:
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
        ax.set_xlim(left=min(x)-0.05*(max(x)-min(x)), right=max(x)+0.05*(max(x)-min(x)))
        ax.set_ylim(bottom=min(y)-0.05*(max(y)-min(y)), top=max(y)+0.05*(max(y)-min(y)))
        #ax.legend(colorlegend, legendlabel, loc=4, fontsize=8, ncol=len(legendlabel))
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
        
        
        
    def model_parameters(self, meansI, norm, numbercl=0):
    
        plt.style.use("default")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white') 
        if self.method == "Spectral Clustering":
            params = pd.read_csv(self.pathS+"model_parameters.txt", sep='\s+')
            ax = self.fig.add_subplot(1,1,1)
            im = ax.imshow(params, cmap='summer_r', aspect='auto', interpolation = 'nearest')
            ax.set_title("Model parameters")
            ax.set(xlabel="Time [sec]", ylabel="Variables")
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
            return self.fig
        if self.method == "TICC":
            gi = pd.read_csv(self.pathS+"generalInfo.csv",error_bad_lines=False, warn_bad_lines=False).values
            w_size = int(gi[6,1])
            n_vars = int(gi[2,1])
            windows = []
            ax = self.fig.add_subplot(111)
            for w in range(w_size):
                mats = []
                for i in range(int(gi[5,1])):
                    mat = pd.read_csv(self.pathS+"model_parameters"+str(i)+".txt", sep='\s+')
                    mats.append(mat.iloc[0+w*n_vars:n_vars+w*n_vars,0+w*n_vars:n_vars+w*n_vars].values)
                matr = []
                for mat in mats:
                    matr.append(np.diag(mat))
                matr = pd.DataFrame(matr).T
                matrF = []
                means = list(np.copy(meansI))
                labelxF = []
                for j in range(0, matr.shape[1]):
                    posa = means.index(max(means))
                    matrF.append(matr[matr.columns[posa]])
                    labelxF.append(posa+1)
                    means[posa] = -2
                matrF = pd.DataFrame(matrF).T
                im = self.heatmap(ax, matrF, title="Diagonal of Toepliz Matrix", labelx="Model ID", labely="Variables", labelxticks=labelxF, labelyticks=list(self.dataset))
                plt.colorbar(im)
                windows.append(matrF)
    
            #ax_slider = fig.add_axes([0.1, 0.05, 0.8, 0.04])
            #slider = ps(ax_slider, 'Time', w_size, activecolor="orange")
            """
            def update(val):
                print "Hello"
                i = int(slider.val)
                im.set_data(windows[i])
                #im.canvas.draw()
            """
            #slider.on_changed(update)
            #slider.canvas.mpl_connect('button_press_event', update)
            #slider.connect_event('button_press_event', update)
            #slider.active = True
            #cbar = ax.figure.colorbar(im, ax=ax)
            return self.fig
    
        if (self.method == "IHMM") or (self.method == "GMM") or (self.method == "HMM"):
            m_means = pd.read_csv(self.pathS+"model_parameters.txt", sep='\s+')
            if norm == False:
                try: 
                    fileDN = pd.read_csv(self.pathDS)
                    var = fileDN.shape[0]
                    fileDN = fileDN.values
                    for i in range(0, var):
                        mean = float(fileDN[i][1])
                        std = float(fileDN[i][2])
                        m_means[m_means.columns[i]] = m_means[m_means.columns[i]]*std+mean    
                except:
                    pass
            m_means = pd.DataFrame(m_means).T
            means = list(np.copy(meansI))
            labelxF = []
            m_meansF = []
            for j in range(0, m_means.shape[1]):
                posa = means.index(max(means))
                m_meansF.append(m_means[m_means.columns[posa]])
                labelxF.append(posa+1)
                means[posa] = -2
            m_meansF = pd.DataFrame(m_meansF).T
            ax = self.fig.add_subplot(1,2,1)
            im = self.heatmap(ax, m_meansF, title="Means Matrix", labelx="Model ID", labely="Variables", labelxticks=labelxF, labelyticks=list(self.dataset))
            plt.colorbar(im)
            
            m_std = pd.read_csv(self.pathS+"model_parameters_std.txt", sep='\s+').T
            means = list(np.copy(meansI))
            labelxF = []
            m_stdF = []
            for j in range(0, m_std.shape[1]):
                posa = means.index(max(means))
                m_stdF.append(m_std[m_std.columns[posa]])
                labelxF.append(posa+1)
                means[posa] = -2
            m_stdF = pd.DataFrame(m_stdF).T
            ax = self.fig.add_subplot(1,2,2)
            im1 = self.heatmap(ax, m_stdF, title="Std Matrix", labelx="Model ID", labely="Variables", labelxticks=labelxF, labelyticks=list(self.dataset))
            plt.colorbar(im1)
            plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.4, right=1, left=0.13)
            return self.fig
        if self.method == "K-Means":
            m_means = pd.read_csv(self.pathS+"model_parameters.txt", sep='\s+')
            if norm == False:
                try: 
                    fileDN = pd.read_csv(self.pathDS)
                    var = fileDN.shape[0]
                    fileDN = fileDN.values
                    for i in range(0, var):
                        mean = float(fileDN[i][1])
                        std = float(fileDN[i][2])
                        m_means[m_means.columns[i]] = m_means[m_means.columns[i]]*std+mean    
                except:
                    pass
            m_means = pd.DataFrame(m_means).T
            means = list(np.copy(meansI))
            labelxF = []
            m_meansF = []
            for j in range(0, m_means.shape[1]):
                posa = means.index(max(means))
                m_meansF.append(m_means[m_means.columns[posa]])
                labelxF.append(posa+1)
                means[posa] = -2
            m_meansF = pd.DataFrame(m_meansF).T
            ax = self.fig.add_subplot(1,1,1)
            im = self.heatmap(ax, m_meansF, title="Means Matrix", labelx="Model ID", labely="Variables", labelxticks=labelxF, labelyticks=list(self.dataset))
            plt.colorbar(im)
            plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3, right=1, left=0.15)
            return self.fig
        if self.method == 'SubCMedians':
            centroids = pd.read_csv(self.pathS+"model_parameters.txt", sep='\s+')
            if norm == False:
                try: 
                    fileDN = pd.read_csv(self.pathDS)
                    var = fileDN.shape[0]
                    fileDN = fileDN.values
                    for i in range(0, var):
                        mean = float(fileDN[i][1])
                        std = float(fileDN[i][2])
                        centroids[centroids.columns[i]] = centroids[centroids.columns[i]]*std+mean    
                except:
                    pass
            centroids = pd.DataFrame(centroids).T
            means = list(np.copy(meansI))
            labelxF = []
            centroidsF = []
            for j in range(0, centroids.shape[1]):
                posa = means.index(max(means))
                centroidsF.append(centroids[centroids.columns[posa]])
                labelxF.append(posa+1)
                means[posa] = -2
            centroidsF = pd.DataFrame(centroidsF).T
            cmapC = plt.cm.get_cmap('summer_r')
            colors.Normalize(clip=False)
            cmapC.set_under(color='grey', alpha=1)
            ax = self.fig.add_subplot(1,1,1)
            im = self.heatmap(ax, centroidsF, title="Centroids Matrix", labelx="Model ID", labely="Variables", labelxticks=labelxF, labelyticks=list(self.dataset), cmap=cmapC)
            plt.colorbar(im)
            plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3, right=1, left=0.15)
            return self.fig
            
    def highlight_model_p(self, meansI, norm, numbercl=0):
    
        gi = pd.DataFrame()
        gi["Parameters"] = ["Model", "Silhouette", "N. points"]
        sC = ["{0:.0f}".format(numbercl)]
        sC.append(meansI[numbercl-1])
        su = self.compute_su(self.clusternorm, self.dataset, numbercl)
        sC.append("{0:.0f}".format((self.clusternorm == numbercl-1).sum()))
        gi["Values"] = sC
        mp = pd.DataFrame()
        mp["Variables"] = list(self.dataset)
        try:
            coordN = pd.read_csv(self.pathS+"model_parameters.txt", sep='\s+')
        except:
            coordN = pd.read_csv(self.pathS+"model_parameters"+str(numbercl-1)+".txt", sep='\s+')
        centroids = coordN.iloc[numbercl-1,:]
        if norm == False:
            try:
                fileDN = pd.read_csv(self.pathDS)
                var = fileDN.shape[0]
                fileDN = fileDN.values
                for i in range(0, var):
                    mean = float(fileDN[i][1])
                    std = float(fileDN[i][2])
                    centroids[i] = centroids[i]*std+mean
            except:
                pass
        centroids = ["{0:.3f}".format(item) for item in centroids]
        mp["Centroid"] = centroids
        su = ["{0:.3f}".format(item) for item in su]
        mp["SU"] = su
        return gi, mp    
    
    def model_parameters2(self, meansI, norm, numbercl=0):
    
        plt.style.use("default")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white') 
        if self.method == "GMM":
            comb = pd.read_csv(self.pathS+"model_parameters_cov.txt", sep='\s+').T
            means = list(np.copy(meansI))
            labelxF = []
            combF = []
            for j in range(0, comb.shape[1]):
                posa = means.index(max(means))
                combF.append(comb[comb.columns[posa]])
                labelxF.append(posa+1)
                means[posa] = -2
            combF = pd.DataFrame(combF).T
            ax = self.fig.add_subplot(1,1,1)
            im = self.heatmap(ax, combF, title="Covariance Matrix", labelx="Model ID", labely="Combination of Variables", labelxticks=labelxF)
            plt.colorbar(im)
            return self.fig
        if (self.method == "IHMM") or (self.method == "HMM"):
            comb = pd.read_csv(self.pathS+"model_parameters_cov.txt", sep='\s+').T
            means = list(np.copy(meansI))
            labelxF = []
            combF = []
            for j in range(0, comb.shape[1]):
                posa = means.index(max(means))
                combF.append(comb[comb.columns[posa]])
                labelxF.append(posa+1)
                means[posa] = -2
            combF = pd.DataFrame(combF).T
            ax = self.fig.add_subplot(1,2,1)
            im = self.heatmap(ax, combF, title="Covariance Matrix", labelx="Model ID", labely="Combination of Variables", labelxticks=labelxF)
            plt.colorbar(im)
            
            trans = pd.read_csv(self.pathS+"model_parameters_trans.txt", sep='\s+').values
            idx_diag = np.diag_indices(trans.shape[0])
            trans[idx_diag] = 'nan'
            means = list(np.copy(meansI))
            ax = self.fig.add_subplot(1,2,2)
            cmapC = plt.cm.get_cmap('summer_r')
            colors.Normalize(clip=False)
            cmapC.set_under(color='grey', alpha=1)
            labelsticks = range(1,trans.shape[0]+1)
            im1 = self.heatmap(ax, trans, title="Transition Matrix", labelx="Model ID", labely="States", labelxticks=labelsticks, labelyticks=labelsticks, cmap=cmapC)
            plt.colorbar(im1)
            plt.tight_layout()
            return self.fig
        if self.method == "TICC":
            gi = pd.read_csv(self.pathS+"generalInfo.csv",error_bad_lines=False, warn_bad_lines=False).values
            w_size = int(gi[6,1])
            n_vars = int(gi[2,1])
            windows = []
            ax = self.fig.add_subplot(111)
            for w in range(w_size):
                mats = []
                for i in range(int(gi[5,1])):
                    mat = pd.read_csv(self.pathS+"model_parameters"+str(i)+".txt", sep='\s+')
                    mats.append(mat.iloc[0+w*n_vars:n_vars+w*n_vars,0+w*n_vars:n_vars+w*n_vars].values)
                indexes = np.triu_indices(len(list(mats[0])),1)
                matr = []
                for mat in mats:
                    mat = XM_clustering_results.do_inverse_cov(mat)
                    matr.append(mat[indexes])
                matr = pd.DataFrame(matr).T
                matrF = []
                means = list(np.copy(meansI))
                labelxF = []
                for j in range(0, matr.shape[1]):
                    posa = means.index(max(means))
                    matrF.append(matr[matr.columns[posa]])
                    labelxF.append(posa+1)
                    means[posa] = -2
                matrF = pd.DataFrame(matrF).T
                im = self.heatmap(ax, matrF, title="Toepliz Matrix", labelx="Model ID", labely="Combination of Variables", labelxticks=labelxF)
                plt.colorbar(im)
                """
                fig = plt.figure(facecolor='white')
                ax01 = fig.add_subplot(1,1,1)
                #df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm)
                #labelvar = list(itertools.combinations(list(df),2))
                ax01 = sns.heatmap(matrF.T, xticklabels=labelxF, yticklabels=False, cbar=True, cmap='summer_r')
                ax01.set_title("Toepliz Matrix")
                ax01.set(xlabel="Model ID", ylabel="Combination of Variables")
                """
                windows.append(matrF)
            #datacursor(hover=True)
            #mplcursors.cursor().connect("add", lambda sel: sel.annotation.set_text(str(comb_labels[list(int(sel.target))[1]])))
    
            #ax_slider = fig.add_axes([0.1, 0.05, 0.8, 0.04])
            #slider = ps(ax_slider, 'Time', w_size, activecolor="orange")
            """
            def update(val):
                print "Hello"
                i = int(slider.val)
                im.set_data(windows[i])
                im.canvas.draw()
            """
            #slider.on_changed(update)
            #slider.canvas.mpl_connect('button_press_event', update)
            #slider.connect_event('button_press_event', update)
            #slider.active = True
            #cbar = ax.figure.colorbar(im, ax=ax)
            return self.fig
    
    def heat_ds(self, norm, exp):
    
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
        if norm == False:
            try:
                fileDN = pd.read_csv(self.pathDS)
                var = fileDN.shape[0]
                fileDN = fileDN.values
                for i in range(0, var):
                    varName = fileDN[i][0]
                    mean = float(fileDN[i][1])
                    std = float(fileDN[i][2])
                    ds[varName] = self.dataset[varName]*std+mean
            except:
                pass
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

    def heat_clust(self, norm, numbercl, exp, GT=False):
        
        if self.gt != GT or self.exp != exp:
            self.exp = exp
            self.gt = GT
            self.change_df(norm, self.usedV, exp, GT)
        plt.style.use("default")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white') 
        if GT:
            try:
                new_coN = pd.read_csv(self.pathS+"model_parameters_GT.txt", sep='\s+')
            except:
                new_coN = pd.read_csv(self.pathS+"model_parameters.txt", sep='\s+')
                print("[XM]> No model parameters GT found, now showing model parameters of the result.")
        else:
            try:
                new_coN = pd.read_csv(self.pathS+"model_parameters.txt", sep='\s+')
            except:
                new_coN = pd.read_csv(self.pathS+"model_parameters0.txt", sep='\s+')
        rows,columns = new_coN.shape
        coordinateNv = new_coN.values
        trueCoord = []
        colorset = [pl.cm.jet(item/len(self.usedClusterset)) for item in list(set(self.usedClusternorm))]
        cmapC = LinearSegmentedColormap.from_list("custom", colorset)
        if numbercl!=0: 
            for i in range(0, self.usedDataset.shape[0]):
                coordRow = []
                if self.usedClusternorm[i] != numbercl:
                     for j in range(0, columns):
                         coordRow.append(np.nan)
                     trueCoord.append(coordRow)
                else:    
                    for j in range(0, columns):
                        if str(coordinateNv[numbercl-1][j]) != 'nan':
                            if coordinateNv[numbercl-1][j] != 0:
                                coordRow.append(numbercl)
                            else:
                                coordRow.append(0)
                        else:
                            coordRow.append(np.nan)
                    trueCoord.append(coordRow)
            
        else:
            for i in range(0, self.usedDataset.shape[0]):
                coordRow = []
                for j in range(0, columns):
                    if coordinateNv[int(self.usedClusternorm[i])-1][j] != 0:
                        if str(coordinateNv[int(self.usedClusternorm[i])-1][j]) != 'nan':
                            coordRow.append(self.usedClusternorm[i])
                        else:
                            coordRow.append(np.nan)
                    else:
                        coordRow.append(0)
                trueCoord.append(coordRow)
        trueCoord = pd.DataFrame(trueCoord)
        ax = self.fig.add_subplot(1,1,1)
        if numbercl != 0:
            if numbercl not in trueCoord.values:
                return 0
        im = self.heatmap(ax, trueCoord.T, title="Clustering Heatmap", labelx="Time [sec]", labely="Variables", labelyticks=list(self.dataset), cmap=cmapC)
        if numbercl!=0:
            plt.colorbar(im)
        else:
            plt.colorbar(im, label="Model ID")
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
        plt.subplots_adjust(top = 0.95, bottom = 0.15, hspace = 0.4, wspace = 0.3, right=1, left=0.15)
        return self.fig
    
    def draw_timeseries(self, norm, usedV, exp, GT=False):
        numbercl = 0
        self.check_changes(norm, numbercl, usedV, exp, GT) 
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white') 
        
        clust, geo = 0, 0
        if len(self.latitude) > 0:
            geo = usedV.pop(1)
        if self.pathS != "/":
            clust = usedV.pop(0)
            seconds = range(0, len(self.usedClusternorm))
            rows, columns = self.usedDataset.shape
            labelvar = list(self.usedDataset)
            
            su = self.compute_su(self.clusternorm, self.dataset)
            if exp == 'All':
                expsI = list(pd.unique(self.experiments))
            else:
                expsI = []
            j = 0
            start = 1
            if len(expsI) > 1 :
                delimF = []
                for exp in expsI:
                    delimF.append(next((i-1 for i in range(0,len(self.experiments)) if self.experiments[i]==exp)))
                lastF = delimF[0]
                if lastF == -1:
                    lastF += len(self.experiments)
                del(delimF[0])
                delimF.append(lastF)
            if clust == 1:
                ax2 = self.fig.add_subplot(4,3,start)
                ax2 = self.to_scatter(ax2, seconds, self.usedClusternorm, 'observations', 'cluster', self.usedColor, self.colorlegend, set(self.clusternorm))
                ax2.set_title("Mapping observation to clusters")
                if len(expsI) > 1:
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
                start += 1
            if  geo == 1:
                ax3 = self.fig.add_subplot(4,3,start)
                ax3 = self.to_scatter(ax3, self.usedLongitude, self.usedLatitude, 'longitude', 'latitude', self.usedColor, self.colorlegend, set(self.clusternorm))            
                ax3.set_title("Geo-localization")
                start += 1
            for i in range(start, columns+start):
                pos = su.index(max(su))
                ax3 = self.fig.add_subplot(4,3,i)
                ax3 = self.to_scatter(ax3, seconds, self.usedDataset[self.usedDataset.columns[j]], 'observations', labelvar[j], self.usedColor, self.colorlegend, set(self.clusternorm))
                ax3.set_title("SU= {0:.3f}".format(float(su[pos])))
                if len(expsI) > 1:
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
                j = j+1
                su[pos] = -1

        plt.subplots_adjust(top = 0.95, bottom = 0.09, wspace = 0.3, right=0.96, left=0.06, hspace=0.55)
        return self.fig
    
    def highlight_cluster(self, norm, numbercl, usedV, exp, GT=False):
        self.check_changes(norm, numbercl, usedV, exp, GT)
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
        
        clust, geo = 0, 0

        new_coN, new_coV = self.used_coord(usedV, norm, numbercl)
        rows, columns = new_coN.shape
        coordinateNn = new_coN.values
        
        used_variables = []
        for i in range(0, rows):
            if i+1 == numbercl:
                for j in range(0, columns):
                    if str(coordinateNn[i][j]) == 'nan':
                        used_variables.append(0)
                    else:
                        used_variables.append(1)
                            
        if len(self.latitude) > 0:
            clust = usedV.pop(0)
            geo = usedV.pop(0)
        else:
            clust = usedV.pop(0)
        seconds = range(0, len(self.usedClusternorm))
        labelvar = list(self.usedDataset)
        
        #color = np.full([len(self.usedClusternorm), 4], 0.07)
        #color[np.where(self.usedClusternorm == numbercl)] = pl.cm.jet(float(numbercl)/len(self.clusterset))
        a = [numbercl]
        
        su = self.compute_su(self.clusternorm, self.dataset, numbercl)
        j = 0
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
        if clust == 1:
            ax2 = self.fig.add_subplot(4,3,start)
            ax2 = self.to_scatter(ax2, seconds, self.usedClusternorm, 'observations', 'cluster', self.usedColor, "colorlegend", a)
            ax2.set_title("Mapping observation to clusters")
            if len(expsI) > 1:
                for xc in delimF:
                    plt.axvline(x=xc, color="red")
            start += 1
        if geo == 1:
            ax3 = self.fig.add_subplot(4,3,start)
            ax3 = self.to_scatter(ax3, self.usedLongitude, self.usedLatitude, 'longitude', 'latitude', self.usedColor, "colorlegend", a) 
            ax3.set_title("Geo-localization")
            start += 1
        for i in range(start, self.usedDataset.shape[1]+start):
            pos = su.index(max(su))
            ax3 = self.fig.add_subplot(4,3,i)
            ax3 = self.to_scatter(ax3, seconds, self.usedDataset[self.usedDataset.columns[j]], 'observations', labelvar[j], self.usedColor, "colorlegend", a)
            ax3.set_title("SU= {0:.3f}".format(float(su[pos])))
            if len(expsI) > 1:
                for xc in delimF:
                    plt.axvline(x=xc, color="red")
            ax3 = plt.gca()
            if not GT:
                if used_variables[j]==1:
                    ax3.set_facecolor('#c7fdb5')
                else:
                    ax3.set_facecolor('mistyrose')
            su[pos] = -1
            j = j+1
        
        plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace=0.55, wspace = 0.3, right=0.96, left=0.06)
        return self.fig

    def scatter_2d(self, norm, var1, var2, numbercl=0, exp="All", GT=False):
        
        if self.gt != GT or self.exp != exp:
            self.exp = exp
            self.gt = GT
            self.change_df(False, self.usedV, exp, GT) 
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
        if GT:
            color = np.array(self.colorGT)
            a = self.clustersetGT
        else:
            color = np.array(self.color)
            a = self.clusterset
        if numbercl != 0:
            color[np.where(self.usedClusternorm != numbercl)] = [0.07, 0.07, 0.07, 0.07]
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
        if norm == False:
            try:
                fileDN = pd.read_csv(self.pathDS)
                var = fileDN.shape[0]
                fileDN = fileDN.values
                for i in range(0, var):
                    varName = fileDN[i][0]
                    mean = float(fileDN[i][1])
                    std = float(fileDN[i][2])
                    current_data[varName] = current_data[varName]*std+mean
            except:
                pass
        labels = list(self.dataset)
        ax = self.fig.add_subplot(1,1,1)
        ax = self.to_scatter(ax, current_data[labels[var1]], current_data[labels[var2]], labels[var1], labels[var2], color, "", a)
        ax.set_title("2D Scatter plot")
        return self.fig

    def scatter_3d(self, norm, fig, var1, var2, var3, numbercl=0, exp="All", GT=False):
            
        if self.gt != GT or self.exp != exp:
            self.exp = exp
            self.gt = GT
            self.change_df(False, self.usedV, exp, GT) 
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
        if GT:
            color = np.array(self.colorGT)
        else:
            color = np.array(self.color)
        if numbercl != 0:
            color[np.where(self.usedClusternorm != numbercl)] = [0.07, 0.07, 0.07, 0.07]
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
        if norm == False:
            try:
                fileDN = pd.read_csv(self.pathDS)
                var = fileDN.shape[0]
                fileDN = fileDN.values
                for i in range(0, var):
                    varName = fileDN[i][0]
                    mean = float(fileDN[i][1])
                    std = float(fileDN[i][2])
                    current_data[varName] = current_data[varName]*std+mean
            except:
                pass
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
        numbercl = 0
        self.check_changes(norm, numbercl, usedV, exp, GT)        
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
    
        if len(self.latitude) > 0:
            clust = usedV.pop(0)
            geo = usedV.pop(0)
        else:
            clust = usedV.pop(0)
        
        labelvar = list(self.usedDataset)
        rows, columns = self.usedDataset.shape
        seconds = range(len(self.usedClusternorm))
        
        if exp == 'All':
            expsI = list(pd.unique(self.experiments))
        else:
            expsI = []
        su = self.compute_su(self.clusternorm, self.dataset)
        if meansI != 0:
            start = 1
            if clust == 1:
                ax2 = self.fig.add_subplot(4,3,start)
                ax2 = self.to_scatter(ax2, seconds, self.usedClusternorm, 'observations', 'cluster', self.usedColor, "colorlegend", set(self.usedClusternorm))
                ax2.set_title("Mapping observation to clusters")
                if len(expsI) > 1:
                    delimF = []
                    for exp in expsI:
                        delimF.append(next((i-1 for i in range(0,len(self.experiments)) if self.experiments[i]==exp)))
                    lastF = delimF[0]
                    if lastF == -1:
                        lastF += len(self.experiments)
                    del(delimF[0])
                    delimF.append(lastF)
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
                start += 1
            if  geo == 1:
                ax3 = self.fig.add_subplot(4,3,start)
                ax3 = self.to_scatter(ax3, self.usedLongitude, self.usedLatitude, 'longitude', 'latitude', self.usedColor, "colorlegend", set(self.usedClusternorm))            
                ax3.set_title("Geo-localization")
                start += 1
            freq = np.array([None for x in self.clusterset])
            for c in set(self.usedClusternorm):
                up = self.usedDataset.loc[self.usedClusternorm == c,:]
                freq[int(c)-1] = pd.DataFrame(up)
            idx_means = np.argsort(meansI)[::-1][:len(meansI)]
            freqC = freq[idx_means]
            labelF = [item+1 for item in idx_means]
            #labelS = [k for k in range(0, len(freqC))]
            for i in range(start, columns+start):
                pos = su.index(max(su))
                ax0 = self.fig.add_subplot(4,3,i)
                freqCol = []
                for x in range(len(freqC)):
                    if freqC[x] is not None:
                        freqCol.append(freqC[x].iloc[:,i-start])
                    else:
                        freqCol.append([])
                #freqCol = np.array(freqCol)
                ax0.boxplot(freqCol)
                plt.gca()
                #plt.xticks(labelS, labelF)
                ax0.set_xticklabels(labelF)
                ax0.set_xlabel("SU= {0:.3f}".format(float(su[pos])))
                ax0.set_ylabel(labelvar[i-start])
                ax0.grid(True)
                su[pos] = -1  
        plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3, right=0.96, left=0.06)
        return self.fig
    
    
    def sort_boxplot(self, meansI, norm, numbercl, usedV, exp, GT=False):

        self.check_changes(norm, numbercl, usedV, exp, GT)  
        if numbercl not in self.usedClusterset:
            return 0, 0, 0
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')

        new_coN, new_coV = self.used_coord(usedV, norm, numbercl)
        rows, columns = new_coN.shape
        coordinateNn = new_coN.values
        
        used_variables = []
        for i in range(0, rows):
            if i+1 == numbercl:
                for j in range(0, columns):
                    if str(coordinateNn[i][j]) == 'nan':
                        used_variables.append(0)
                    else:
                        used_variables.append(1)
        a = [numbercl]
        
        if len(self.latitude) > 0:
            clust = usedV.pop(0)
            geo = usedV.pop(0)
        else:
            clust = usedV.pop(0)
        
        rows, columns = self.usedDataset.shape

        seconds = range(len(self.usedClusternorm))
        labelvar = list(self.usedDataset)
        
        if GT:
            su = self.compute_su(self.clusternormGT, self.dataset, numbercl)
        else:
            su = self.compute_su(self.clusternorm, self.dataset, numbercl)
        start = 1
        if clust == 1:
            ax2 = self.fig.add_subplot(4,3,start)
            ax2 = self.to_scatter(ax2, seconds, self.usedClusternorm, 'observations', 'cluster', self.usedColor, "colorlegend", a)
            ax2.set_title("Mapping observation to clusters")
            if exp == 'All':
                expsI = list(pd.unique(self.experiments))
            else:
                expsI = []
            if len(expsI) > 1:
                delimF = []
                for exp in expsI:
                    delimF.append(next((i-1 for i in range(0,len(self.experiments)) if self.experiments[i]==exp)))
                lastF = delimF[0]
                if lastF == -1:
                    lastF += len(self.experiments)
                del(delimF[0])
                delimF.append(lastF)    
                for xc in delimF:
                    plt.axvline(x=xc, color="red")
            start += 1
        if  geo == 1:
            ax3 = self.fig.add_subplot(4,3,start)
            ax3 = self.to_scatter(ax3, self.usedLongitude, self.usedLatitude, 'longitude', 'latitude', self.usedColor, "colorlegend", a)            
            ax3.set_title("Geo-localization")
            start += 1
        r = 0
        freq = np.array([None for x in self.clusterset])
        for c in set(self.usedClusternorm):
            freq[int(c)-1] = self.usedDataset.loc[self.usedClusternorm == c,:]
            r = r+1
        if GT:
            freqC = freq
            labelF = [k+1 for k in range(0, len(freqC))]
        else:
            idx_means = np.argsort(meansI)[::-1][:len(meansI)]
            labelF = [item+1 for item in idx_means]
            freqC = freq[idx_means]
        labelS = [k+1 for k in range(0, len(freqC))]
        for i in range(start, columns+start):
            pos = su.index(max(su))
            ax0 = self.fig.add_subplot(4,3,i)
            freqCol = []
            for x in range(len(freqC)):
                if freqC[x] is not None:
                    freqCol.append(freqC[x].iloc[:,i-start])
                else:
                    freqCol.append([])
            ax0.boxplot(freqCol)
            plt.xticks(labelS, labelF)
            ax0.set_xlabel("SU= {0:.3f}".format(float(su[pos])))
            ax0.set_ylabel(labelvar[i-start])
            ax0.grid(True)
            ax0 = plt.gca()
            if not GT:
                if used_variables[i-start] == 1:
                    ax0.set_facecolor('#c7fdb5')
                else:
                    ax0.set_facecolor('mistyrose')
            su[pos] = -1  
        points = list(self.usedClusternorm).count(numbercl)
        plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3, right=0.96, left=0.06)
        return self.fig, points, len(self.usedClusternorm)
    
    
    def draw_barplot(self, norm, usedV, exp, GT=False):
        numbercl = 0
        self.check_changes(norm, numbercl, usedV, exp, GT)
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
    
        if len(self.latitude) > 0:
            clust = usedV.pop(0)
            geo = usedV.pop(0)
        else:
            clust = usedV.pop(0)
        
        labelvar = list(self.usedDataset)
        rows, columns = self.usedDataset.shape
        seconds = range(len(self.usedClusternorm))
        
        if self.pathS != "/":
            su = self.compute_su(self.clusternorm, self.dataset)
            start = 1
            if clust == 1:
                ax2 = self.fig.add_subplot(4,3,start)
                ax2 = self.to_scatter(ax2, seconds, self.usedClusternorm, 'observations', 'cluster', self.usedColor, "colorlegend", set(self.usedClusternorm))
                ax2.set_title("Mapping observation to clusters")
                start += 1
                if exp == 'All':
                    expsI = list(pd.unique(self.experiments))
                else:
                    expsI = []
                if len(expsI) > 1:
                    delimF = []
                    for exp in expsI:
                        delimF.append(next((i-1 for i in range(0,len(self.experiments)) if self.experiments[i]==exp)))
                    lastF = delimF[0]
                    if lastF == -1:
                        lastF += len(self.experiments)
                    del(delimF[0])
                    delimF.append(lastF)
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
            if  geo == 1:
                ax3 = self.fig.add_subplot(4,3,start)
                ax3 = self.to_scatter(ax3, self.usedLongitude, self.usedLatitude, 'longitude', 'latitude', self.usedColor, "colorlegend", set(self.usedClusternorm))            
                ax3.set_title("Geo-localization")
                start += 1
            for i in range(start,columns+start):
                pos = su.index(max(su))
                ax0 = self.fig.add_subplot(4,3,i)
                ax0.hist(x=self.usedDataset[self.usedDataset.columns[i-start]], bins=20, color="green")
                plt.title(labelvar[i-start]+"  SU= {0:.3f}".format(float(su[pos])))
                plt.grid(True)
                su[pos] = -1
        
        plt.subplots_adjust(top = 0.95, bottom = 0.045, hspace = 0.55, wspace = 0.3, right=0.96, left=0.06)
        return self.fig
    
    def highlight_barplot(self, norm, numbercl, usedV, exp, GT=False):
        
        self.check_changes(norm, numbercl, usedV, exp, GT)  
        if numbercl not in self.usedClusterset:
            return 0, 0, 0
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')

        new_coN, new_coV = self.used_coord(usedV, norm, numbercl)
        rows, columns = new_coN.shape
        coordinateNn = new_coN.values
        
        used_variables = []
        for i in range(0, rows):
            if i+1 == numbercl:
                for j in range(0, columns):
                    if str(coordinateNn[i][j]) == 'nan':
                        used_variables.append(0)
                    else:
                        used_variables.append(1)
        a = [numbercl]
        
        if len(self.latitude) > 0:
            clust = usedV.pop(0)
            geo = usedV.pop(0)
        else:
            clust = usedV.pop(0)
            
        seconds = range(len(self.usedClusternorm))
        labelvar = list(self.usedDataset)
        
        su = self.compute_su(self.clusternorm, self.dataset, numbercl)
        start = 1
        if clust == 1:
            ax2 = self.fig.add_subplot(4,3,start)
            ax2 = self.to_scatter(ax2, seconds, self.usedClusternorm, 'observations', 'cluster', self.usedColor, "colorlegend", a)
            ax2.set_title("Mapping observation to clusters")
            start += 1
            if exp == 'All':
                expsI = list(pd.unique(self.experiments))
            else:
                expsI = []
            if len(expsI) > 1:
                delimF = []
                for exp in expsI:
                    delimF.append(next((i-1 for i in range(0,len(self.experiments)) if self.experiments[i]==exp)))
                lastF = delimF[0]
                if lastF == -1:
                    lastF += len(self.experiments)
                del(delimF[0])
                delimF.append(lastF)
                for xc in delimF:
                    plt.axvline(x=xc, color="red")
        if  geo == 1:
            ax3 = self.fig.add_subplot(4,3,start)
            ax3 = self.to_scatter(ax3, self.usedLongitude, self.usedLatitude, 'longitude', 'latitude', self.usedColor, "colorlegend", a)            
            ax3.set_title("Geo-localization")
            start += 1
        for i in range(start,columns+start):
            pos = su.index(max(su))
            ax0 = self.fig.add_subplot(4,3,i)
            bins=20
            ahist, abins = np.histogram(self.usedDataset[self.usedDataset.columns[i-start]], bins)
            freq = [[] for x in self.clusterset]
            r = 0
            for c in self.usedClusternorm:
                freq[int(c)-1].append(self.usedDataset.iloc[r, i-start])
                r = r+1
            bhist, bbins, _ = ax0.hist(x=[freq[numbercl-1], self.usedDataset[self.usedDataset.columns[i-start]]], color=[(0,0,0,0), (0,0,0,0)], bins=bins, rwidth=1, edgecolor="none", stacked=True)
            w = (bbins[1] - bbins[0])
            ax0.remove()
            ax0 = self.fig.add_subplot(4,3,i)
            ax0.set_title(labelvar[i-start]+"  SU={0:.3f}".format(float(su[pos])))
            plt.grid(True)
            ax0.bar(abins[:-1], ahist, width=w, color='green')
            ax0.bar(abins[:-1], bhist[1]-ahist, width=w, color='yellow')
            ax0 = plt.gca()
            if not GT:
                if used_variables[i-start] == 1:
                    ax0.set_facecolor('#c7fdb5')
                else:
                    ax0.set_facecolor('mistyrose')
            su[pos] = -1
        
        n_points = list(self.usedClusternorm).count(numbercl)
        plt.subplots_adjust(top = 0.95, bottom = 0.045, hspace = 0.55, wspace = 0.3, right=0.96, left=0.06)
        return self.fig, n_points, len(self.usedClusternorm)
    
    
    def geo_localization(self, usedExp="", numbercl=0, exp="All", GT=False):
        
        if self.gt != GT or self.exp != exp:
            self.exp = exp
            self.gt = GT
            self.change_df(False, self.usedV, exp, GT) 
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
        
        if GT:
            color = np.array(self.colorGT)
        else:
            color = np.array(self.color)
        if numbercl != 0:
            color[np.where(self.usedClusternorm != numbercl)] = [0.07, 0.07, 0.07, 0.07]   
        if exp == "All":
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
                ax = self.to_scatter(ax, self.longitude[uDelimI[i-1]:uDelimF[i-1]], self.latitude[uDelimI[i-1]:uDelimF[i-1]], "longitude", "latitude", color[uDelimI[i-1]:uDelimF[i-1]], "colorlegend", set(self.clusternorm))
                ax.set_title(exps[i-1])
        else:
            ax = self.fig.add_subplot(1,1,1)
            ax = self.to_scatter(ax, self.usedLongitude, self.usedLatitude, "longitude", "latitude", self.usedColor, "colorlegend", set(self.clusternorm))
        
        plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3, right=0.96, left=0.1)
        
        return self.fig
    
    
    def tsne(self, norm, numbercl=0):
        
        plt.style.use("classic")
        if self.fig != None:
            self.fig.clear()
        self.fig = plt.figure(facecolor='white')
        
        res = pd.read_csv(self.pathS+"/tsne.csv")
        clusters = res[res.columns[2]]
        clusterset = set(clusters)
        if numbercl == 0:
            color = [pl.cm.jet(item/len(clusterset)) for item in clusters]
            colorset = [pl.cm.jet(item/len(clusterset)) for item in list(clusterset)]
            colorlegend = []
            for i in range(0,len(colorset)):
                colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        else:
            color = []
            colorset = []
            for item in clusters:
                if item == numbercl:
                    color.append(pl.cm.jet(item/len(clusterset)))
                else:
                    color.append([0.07,0.07,0.07,0.07])
            for item in list(set(clusters)):
                if item == numbercl:
                    colorset.append(pl.cm.jet(item/len(clusterset)))
                else:
                    colorset.append([0.07,0.07,0.07,0.07])
            colorlegend = []
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[numbercl-1]))
            a = [numbercl]
        
        ax = self.fig.add_subplot(1,1,1)
        ax.scatter(res[res.columns[0]],res[res.columns[1]],c=color,edgecolors='face',s=2)
        ax.grid(True)
        if numbercl != 0:
            ax.legend(colorlegend, a, loc=4, fontsize=6)
        else:
            ax.legend(colorlegend, set(clusters), loc=4, fontsize=6, ncol=len(set(clusters)))
            
        return self.fig
