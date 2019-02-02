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

#from mpl_toolkits.mplot3d import Axes3D
import SU
import seaborn as sns
import pandas as pd
import numpy as np
#import sklearn.metrics as sk
#import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.pylab as pl
import csv
#import re
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
#import numpy as np
from tkinter import Label
#import Silhouette_mem as sm
#import SM2 as SM2
from matplotlib.colors import LinearSegmentedColormap
#import folium
import itertools
import time
#import os
#import subprocess
#from PageSlider import PageSlider as ps
import math



def tabCentroidi(coordinate, coordinateVv, labeltab, labelvar):
    
    cmapC = plt.cm.get_cmap('summer_r')
    colors.Normalize(clip=False)
    cmapC.set_under(color='grey', alpha=1)
    sns.set(font_scale=0.85)
    ax = sns.heatmap(coordinate.T, xticklabels=labeltab, yticklabels=labelvar, fmt=".3f", annot=coordinateVv.T, linewidths=.05, linecolor='black', cbar=True, cmap=cmapC)
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
        ax.set_xlim(left=min(x)-0.05*(max(x)-min(x)), right=max(x)+0.05*(max(x)-min(x)))
        ax.set_ylim(bottom=min(y)-0.05*(max(y)-min(y)), top=max(y)+0.05*(max(y)-min(y)))
        #ax.legend(colorlegend, legendlabel, loc=4, fontsize=8, ncol=len(legendlabel))
        return ax

def do_inverse_cov(mat):
    matrix = pd.DataFrame(mat).copy()
    matrix_f = pd.DataFrame(mat).copy()
    for i in range(matrix.shape[0]):
        for j in range(i,matrix.shape[1]):
            matrix_f.iloc[i,j] = -(matrix.iloc[i,j]/(math.sqrt(matrix.iloc[i,i]*matrix.iloc[j,j])))
    return matrix_f.values

def model_parameters2(meansI, percorsoD, percorsoS, norm, numerocl=0):
    
    gi = pd.read_csv(percorsoS+"generalInfo.csv",error_bad_lines=False, warn_bad_lines=False).values
    if "GMM" in gi:
        comb = pd.read_table(percorsoS+"model_parameters_cov.txt", delim_whitespace=True).T
        means = list(np.copy(meansI))
        labelxF = []
        combF = []
        for j in range(0, comb.shape[1]):
            posa = means.index(max(means))
            combF.append(comb[comb.columns[posa]])
            labelxF.append(posa+1)
            means[posa] = -2
        combF = pd.DataFrame(combF).T
        df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm)
        fig = plt.figure(facecolor='white')
        ax01 = fig.add_subplot(1,1,1)
        ax01 = sns.heatmap(combF, xticklabels=labelxF, cbar=True, cmap='summer_r')
        ax01.set_title("Covariance Matrix")
        ax01.set(xlabel="Model ID", ylabel="Variables")
        return fig
    if "IHMM" in gi:
        comb = pd.read_table(percorsoS+"model_parameters_cov.txt", delim_whitespace=True).T
        means = list(np.copy(meansI))
        labelxF = []
        combF = []
        for j in range(0, comb.shape[1]):
            posa = means.index(max(means))
            combF.append(comb[comb.columns[posa]])
            labelxF.append(posa+1)
            means[posa] = -2
        combF = pd.DataFrame(combF).T
        df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm)
        fig = plt.figure(facecolor='white')
        ax01 = fig.add_subplot(1,2,1)
        ax01 = sns.heatmap(combF, xticklabels=labelxF, cbar=True, cmap='summer_r')
        ax01.set_title("Covariance Matrix")
        ax01.set(xlabel="Model ID", ylabel="Variables")
        
        trans = pd.read_table(percorsoS+"model_parameters_trans.txt", delim_whitespace=True)
        means = list(np.copy(meansI))
        ax01 = fig.add_subplot(1,2,2)
        labels = [i for i in range(1, len(trans)+1)]
        ax01 = sns.heatmap(trans, xticklabels=labels, yticklabels=labels, linecolor='black', cbar=True, cmap='summer_r')
        ax01.set_title("Transition Matrix")
        ax01.set(xlabel="Model ID", ylabel="Variables")
        plt.tight_layout()
        return fig
    if "TICC" in gi:
        w_size = int(gi[6,1])
        n_vars = int(gi[2,1])
        windows = []
        fig = plt.figure(facecolor='white')
        #fig, ax = plt.subplots()
        #fig.subplots_adjust(bottom=0.18)
        ax = fig.add_subplot(111)
        for w in range(w_size):
            mats = []
            for i in range(int(gi[5,1])):
                mat = pd.read_table(percorsoS+"model_parameters"+str(i)+".txt", delim_whitespace=True)
                mats.append(mat.iloc[0+w*n_vars:n_vars+w*n_vars,0+w*n_vars:n_vars+w*n_vars].values)
            indexes = np.triu_indices(len(list(mats[0])),1)
            matr = []
            for mat in mats:
                mat = do_inverse_cov(mat)
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
            #im = ax.imshow(matrF, cmap='summer_r')
            df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm)
            ax = sns.heatmap(matrF, xticklabels=labelxF, cmap="summer_r", cbar=True)
            ax.set_title("Toepliz Matrix")
            ax.set(xlabel="Model ID", ylabel="Combination of Variables")
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
        return fig

def model_parameters(meansI, percorsoD, percorsoS, norm, numerocl=0):
    
    """Different behaviour if method == SpectralClustering"""
    gi = pd.read_csv(percorsoS+"generalInfo.csv",error_bad_lines=False, warn_bad_lines=False).values
    if "Spectral Clustering" in gi:
        df = pd.read_table(percorsoS+"model_parameters.txt", delim_whitespace=True)
        fig = plt.figure(facecolor='white')
        ax01 = fig.add_subplot(1,1,1)
        ax01 = sns.heatmap(df, yticklabels=df.shape[0]/10, xticklabels=df.shape[0]/10, cbar=True, cmap="summer_r")
        ax01.set_title("Model parameters")
        ax01.set(xlabel="Time [sec]", ylabel="Variables")
        ax01.set_yticklabels(ax01.get_yticklabels(), rotation=0)
        return fig
    if "TICC" in gi:
        w_size = int(gi[6,1])
        n_vars = int(gi[2,1])
        windows = []
        fig = plt.figure(facecolor='white')
        #fig, ax = plt.subplots()
        #fig.subplots_adjust(bottom=0.18)
        ax = fig.add_subplot(111)
        for w in range(w_size):
            mats = []
            for i in range(int(gi[5,1])):
                mat = pd.read_table(percorsoS+"model_parameters"+str(i)+".txt", delim_whitespace=True)
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
            #im = ax.imshow(matrF, cmap='summer_r')
            df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm)
            ax = sns.heatmap(matrF, xticklabels=labelxF, yticklabels=list(df), cmap="summer_r", cbar=True)
            ax.set_title("Diagonal of Toepliz Matrix")
            ax.set(xlabel="Model ID")
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
        return fig

    if ("IHMM" in gi) or ("GMM" in gi):
        m_means = pd.read_table(percorsoS+"model_parameters.txt", delim_whitespace=True).T
        means = list(np.copy(meansI))
        labelxF = []
        m_meansF = []
        for j in range(0, m_means.shape[1]):
            posa = means.index(max(means))
            m_meansF.append(m_means[m_means.columns[posa]])
            labelxF.append(posa+1)
            means[posa] = -2
        m_meansF = pd.DataFrame(m_meansF).T
        df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm)
        fig = plt.figure(facecolor='white')
        ax01 = fig.add_subplot(1,2,1)
        ax01 = sns.heatmap(m_meansF, xticklabels=labelxF, yticklabels=list(df), linewidths=.05, linecolor='black', cbar=True, cmap='summer_r')
        ax01.set_title("Means Matrix")
        ax01.set(xlabel="Model ID", ylabel="Variables")
        
        m_std = pd.read_table(percorsoS+"model_parameters_std.txt", delim_whitespace=True).T
        means = list(np.copy(meansI))
        labelxF = []
        m_stdF = []
        for j in range(0, m_std.shape[1]):
            posa = means.index(max(means))
            m_stdF.append(m_std[m_std.columns[posa]])
            labelxF.append(posa+1)
            means[posa] = -2
        m_stdF = pd.DataFrame(m_stdF).T
        ax01 = fig.add_subplot(1,2,2)
        ax01 = sns.heatmap(m_stdF, xticklabels=labelxF, yticklabels=list(df), linewidths=.05, linecolor='black', cbar=True, cmap='summer_r')
        ax01.set_title("Std Matrix")
        ax01.set(xlabel="Model ID", ylabel="Variables")
        plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.4)
        #plt.tight_layout()
        return fig
    if "K-Means" in gi:
        m_means = pd.read_table(percorsoS+"model_parameters.txt", delim_whitespace=True).T
        means = list(np.copy(meansI))
        labelxF = []
        m_meansF = []
        for j in range(0, m_means.shape[1]):
            posa = means.index(max(means))
            m_meansF.append(m_means[m_means.columns[posa]])
            labelxF.append(posa+1)
            means[posa] = -2
        m_meansF = pd.DataFrame(m_meansF).T
        df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm)
        fig = plt.figure(facecolor='white')
        ax01 = fig.add_subplot(1,1,1)
        ax01 = sns.heatmap(m_meansF, xticklabels=labelxF, yticklabels=list(df), linewidths=.05, linecolor='black', cbar=True, cmap='summer_r')
        ax01.set_title("Means Matrix")
        ax01.set(xlabel="Model ID", ylabel="Variables")
        return fig
    df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm)
    clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS)
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
                    if str(coordinateNv[i][j]) != 'nan' and coordinateNv[i][j] != 0:
                            coordinateNv[i][j] = 1 
        for i in range(0, righe):
            if i+1 != numerocl:
                for j in range(0, colonne):
                    coordinateVv[i][j] = 'nan'
    else:
        """
        for i in range(0, righe):
            for j in range(0, colonne):
                if coordinateNv[i][j] != 0 and str(coordinateNv[i][j]) != 'nan':
                        coordinateNv[i][j] = 1
        """
        new_coN.fillna(-1, inplace=True)
        new_coN.mask((new_coN != 0) & (new_coN != -1), 1, inplace=True)
        new_coN.mask((new_coN == -1), inplace=True)
        coordinateNv = new_coN.values
    if meansI != 0:
        cNV = pd.DataFrame(pd.DataFrame(coordinateNv).T)
        cVV = pd.DataFrame(pd.DataFrame(coordinateVv).T)
        if norm == False:
            try: 
                fileDN = pd.read_csv(percorsoS+"dataStandardization.csv")
                var = fileDN.shape[0]
                fileDN = fileDN.values
                for i in range(0, var):
                    mean = float(fileDN[i][1])
                    std = float(fileDN[i][2])
                    cVV.T[cVV.T.columns[i]] = cVV.T[cVV.T.columns[i]]*std+mean
                righeVV, colonneVV = cVV.shape
                cVV = cVV.values
                for i in range(0,righeVV):
                    for j in range(0,colonneVV):
                        cVV[i][j] = "{0:.3f}".format(cVV[i][j])
                cVV = pd.DataFrame(cVV)    
            except:
                pass
        cNF = []
        cVF = []
        means = list(np.copy(meansI))
        labelxF = []
        for j in range(0, cNV.shape[1]):
            posa = means.index(max(means))
            cNF.append(cNV[cNV.columns[posa]])
            cVF.append(cVV[cVV.columns[posa]])
            labelxF.append(posa+1)
            means[posa] = -2
        cNF = pd.DataFrame(cNF)
        cVF = pd.DataFrame(cVF)
        fig = plt.figure(facecolor='white')
        try:
            fileCov = pd.read_table(percorsoS+"model_parameters_cov.txt", delim_whitespace=True).T
            if norm == False:
                try: 
                    fileDN = pd.read_csv(percorsoS+"dataStandardization.csv")
                    var = fileDN.shape[0]
                    fileDN = fileDN.values
                    for i in range(0, var):
                        mean = float(fileDN[i][1])
                        std = float(fileDN[i][2])
                        fileCov.T[fileCov.T.columns[i]] = fileCov.T[fileCov.T.columns[i]]*std+mean
                    righeVV, colonneVV = fileCov.shape
                    fileCov = fileCov.values
                    for i in range(0,righeVV):
                        for j in range(0,colonneVV):
                            fileCov[i][j] = "{0:.3f}".format(fileCov[i][j])
                    fileCov = pd.DataFrame(fileCov)    
                except:
                    pass
            fileCovF = []
            means = list(np.copy(meansI))
            for j in range(0, fileCov.shape[1]):
                posa = means.index(max(means))
                fileCovF.append(fileCov[fileCov.columns[posa]])
                means[posa] = -2
            fileCovF = pd.DataFrame(fileCovF)
            ax01 = fig.add_subplot(1,2,1)
            ax01 = sns.heatmap(cVF.T, annot=True, xticklabels=labelxF, yticklabels=labelvar, fmt=".3f", linewidths=.05, linecolor='black', cbar=True, cmap='summer_r')
            ax01.set_title("Means Matrix")
            ax02 = fig.add_subplot(1,2,2)
            if fileCovF.shape[1] != len(labelvar):
                labelvar = list(itertools.combinations_with_replacement(labelvar,2))
            ax02 = sns.heatmap(fileCovF.T.values, xticklabels=labelxF, yticklabels=labelvar, fmt=".3f", annot=True, linewidths=.05, linecolor='black', cbar=True, cmap='summer_r')
            ax02.set_yticklabels(ax02.get_yticklabels(), rotation=0)
            ax02.set_title("Covariance Matrix")
            ax02.set(xlabel="Model ID", ylabel="Variables")
        except:
            ax01 = fig.add_subplot(1,1,1)
            ax01 = tabCentroidi(cNF, cVF, labelxF, labelvar)
            ax01.set_title("Used Variables")
    else:
        cVV = pd.DataFrame(pd.DataFrame(coordinateVv).T)
        if norm == False:
            try: 
                fileDN = pd.read_csv(percorsoS+"dataStandardization.csv")
                var = fileDN.shape[0]
                fileDN = fileDN.values
                for i in range(0, var):
                    mean = float(fileDN[i][1])
                    std = float(fileDN[i][2])
                    cVV.T[cVV.T.columns[i]] = cVV.T[cVV.T.columns[i]]*std+mean
                righeVV, colonneVV = cVV.shape
                cVV = cVV.values
                for i in range(0,righeVV):
                    for j in range(0,colonneVV):
                        cVV[i][j] = "{0:.3f}".format(cVV[i][j])
                cVV = pd.DataFrame(cVV) 
            except:
                pass
        fig = plt.figure(facecolor='white')
        ax01 = fig.add_subplot(1,1,1)
        ax01 = tabCentroidi(coordinateNv, coordinateVv, labeltab, labelvar)
        ax01.set_title("Used Variables")
    ax01.set(xlabel="Model ID", ylabel="Variables")
    return fig

def highlight_model_p(meansI, percorsoD, percorsoS, norm, numerocl=0):
    
    df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm)
    clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS)
    labelvar = list(df)
    gi = pd.DataFrame()
    gi["Parameters"] = ["Model", "Silhouette", "N. points"]
    sC = ["{0:.0f}".format(numerocl)]
    sC.append(meansI[numerocl-1])
    su = compute_su(clusternorm, df, numerocl)
    freq = [[] for x in clustergiusti]
    r = 0
    pos = su.index(max(su))
    for c in clusternorm:
        freq[int(c)-1].append(df.iloc[r,pos])
        r = r+1
    sC.append("{0:.0f}".format(len(freq[numerocl-1])))
    gi["Values"] = sC
    mp = pd.DataFrame()
    mp["Variables"] = labelvar
    centroids = []
    coordN = pd.read_table(percorsoS+"model_parameters.txt", delim_whitespace=True)
    righe, colonne = coordN.shape
    coordN = coordN.values
    for i in range(0, righe):
        if i+1 == numerocl:
            for j in range(0, colonne):
                centroids.append(coordN[i][j])
    
    if norm == False:
        try:
            fileDN = pd.read_csv(percorsoS+"dataStandardization.csv")
            var = fileDN.shape[0]
            fileDN = fileDN.values
            for i in range(0, var):
                #varName = fileDN[i][0]
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

def heat_ds(percorsoD, percorsoS, norm, exp):
    
    df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm, exp)
    labelvar = list(df)
    fig = plt.figure(facecolor='white')
    ax01 = fig.add_subplot(1,1,1)
    ax01 = sns.heatmap(df.T, yticklabels=labelvar, xticklabels="auto", cbar=True, cmap="summer_r")
    ax01.set_title("Heatmap")
    ax01.set(xlabel="Time [sec]", ylabel="Variables")
    ax01.set_yticklabels(ax01.get_yticklabels(), rotation=0)
    if len(list(pd.unique(experiment))) > 1:
        expsI = list(pd.unique(experiment))
        delimF = []
        for exp in expsI:
            delimF.append(next((i-1 for i in range(0,len(experiment)) if experiment[i]==exp)))
        lastF = delimF[0]
        if lastF == -1:
            lastF += len(experiment)
        del(delimF[0])
        delimF.append(lastF)
        for xc in delimF:
            plt.axvline(x=xc, color='red')
    return fig

def heat_clust(percorsoD, percorsoS, percorsoG, norm, numerocl, exp):
    
    df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm, exp)
    if percorsoG != "":
        clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, percorsoG)
    else:
        clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, exp=exp)
    labelvar = list(df) 
    if percorsoG != "":
        new_coN = pd.read_table(percorsoS+"model_parameters_GT.txt", delim_whitespace=True)
    else:
        new_coN = pd.read_table(percorsoS+"model_parameters.txt", delim_whitespace=True)
    righe,colonne = new_coN.shape
    coordinateNv = new_coN.values
    obs = [item for item in range(0, df.shape[0])]
    coordVere = []
    colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
    cmapC = LinearSegmentedColormap.from_list("custom", colorset)
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
    fig = plt.figure(facecolor='white')
    ax01 = fig.add_subplot(1,1,1)
    if numerocl != 0:
        if numerocl not in coordVere.values:
            return 0
    if numerocl!=0:
        ax01 = sns.heatmap(coordVere.T, yticklabels=labelvar, xticklabels="auto", cbar=False, cmap=cmapC)
    else:
        ax01 = sns.heatmap(coordVere.T, yticklabels=labelvar, xticklabels="auto", cbar=True, cmap=cmapC, cbar_kws={'label' : 'Model ID'})
    ax01.set_yticklabels(ax01.get_yticklabels(), rotation=0)
    ax01.set_title("Heatmap")
    ax01.set(xlabel="Time [sec]", ylabel="Variables")
    if len(list(pd.unique(experiment))) > 1:
        expsI = list(pd.unique(experiment))
        delimF = []
        for exp in expsI:
            delimF.append(next((i-1 for i in range(0,len(experiment)) if experiment[i]==exp)))
        lastF = delimF[0]
        if lastF == -1:
            lastF += len(experiment)
        del(delimF[0])
        delimF.append(lastF)
        for xc in delimF:
            plt.axvline(x=xc, color='red')
    return fig


def disegna_grafici(percorsoD, percorsoS, percorsoG, norm, usedV, exp):
    
    """
    Caricamento dati
    """
    #initTime = time.time()
    if percorsoS != "/":
        df, latitude, longitude, experiment = used_df(percorsoD, percorsoS, percorsoG, norm, usedV, exp=exp)
        clust, geo = "", ""
        if len(latitude) > 0:
            clust = usedV.pop(0)
            geo = usedV.pop(0)
        else:
            clust = usedV.pop(0)
        clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, percorsoG, exp=exp)
        color = [pl.cm.jet(item/len(clustergiusti)) for item in clusternorm]
        colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        seconds = range(0, len(clusternorm))
    else:
        df, latitudine, longitudine, experiment = get_dataset(percorsoD, percorsoS, False, exp)
        color = [[0,0,1,1] for item in range(0, df.shape[0])]
        colorset = color
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        seconds = range(0, df.shape[0])
    
    righe, colonne = df.shape
    labelvar = list(df)
    #labeltab = list(set(clusternorm))

    """
    Grafici
    """
    
    plt.style.use("classic")
    fig = plt.figure(facecolor='white')   

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
    #print time.time()-initTime
    #ax1 = to_scatter(ax1, longi, lati, 'longitude', 'latitude', color, colorlegend, set(clusternorm))
    if percorsoS != "/":
        su = compute_su(clusternorm, df)
        j = 0
        expsI = list(pd.unique(experiment))
        if len(expsI) > 1 :
            delimF = []
            for exp in expsI:
                delimF.append(next((i-1 for i in range(0,len(experiment)) if experiment[i]==exp)))
            lastF = delimF[0]
            if lastF == -1:
                lastF += len(experiment)
            del(delimF[0])
            delimF.append(lastF)
        start = 1
        if clust == 1:
            ax2 = fig.add_subplot(4,3,start)
            ax2 = to_scatter(ax2, seconds, clusternorm, 'observations', 'cluster', color, colorlegend, set(clusternorm))
            ax2.set_title("Mapping observation to clusters")
            if len(expsI) > 1:
                for xc in delimF:
                    plt.axvline(x=xc, color="red")
            start += 1
            #print time.time()-initTime
        if  geo == 1:
            ax3 = fig.add_subplot(4,3,start)
            ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, colorlegend, set(clusternorm))            
            ax3.set_title("Geo-localization")
            start += 1
            #print time.time()-initTime
        for i in range(start, colonne+start):
            pos = su.index(max(su))
            ax3 = fig.add_subplot(4,3,i)
            ax3 = to_scatter(ax3, seconds, df[df.columns[j]], 'observations', labelvar[j], color, colorlegend, set(clusternorm))
            ax3.set_title("SU= {0:.3f}".format(float(su[pos])))
            if len(expsI) > 1:
                for xc in delimF:
                    plt.axvline(x=xc, color="red")
            j = j+1
            su[pos] = -1
            #print time.time()-initTime
    else:
        j = 0
        x = 1
        expsI = list(pd.unique(experiment))
        if len(expsI) > 1 :
            delimF = []
            for exp in expsI:
                delimF.append(next((i-1 for i in range(0,len(experiment)) if experiment[i]==exp)))
            lastF = delimF[0]
            if lastF == -1:
                lastF += len(experiment)
            del(delimF[0])
            delimF.append(lastF)
        for i in range(1, colonne+1):
            if usedV[i-1]==1:
                ax3 = fig.add_subplot(4,3,x)
                if len(expsI) > 1:
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
                ax3 = to_scatter(ax3, seconds, df[df.columns[j]], 'observations', labelvar[j], color, colorlegend, "1")
                x += 1
            j = j+1
   
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.55, wspace = 0.3)
    return fig
    

def highlight_cluster(percorsoD, percorsoS, percorsoG, norm, numerocl, usedV, exp):
    
    """
    Caricamento dati
    """
    df, latitude, longitude, experiment = used_df(percorsoD, percorsoS, percorsoG, norm, usedV, exp, numerocl)
    clust, geo = "", ""
    if percorsoG != "":
        clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, percorsoG)
        colonne = df.shape[1]
    else:
        clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, exp=exp)
        new_coN, new_coV = used_coord(percorsoD, percorsoS, usedV, norm, numerocl)
        righe, colonne = new_coN.shape
        coordinateNn = new_coN.values
        
        used_variables = []
        for i in range(0, righe):
            if i+1 == numerocl:
                for j in range(0, colonne):
                    if str(coordinateNn[i][j]) == 'nan':
                        used_variables.append(0)
                    else:
                        used_variables.append(1)
                        
    if len(latitude) > 0:
        clust = usedV.pop(0)
        geo = usedV.pop(0)
    else:
        clust = usedV.pop(0)
    seconds = range(0, len(clusternorm))
    labelvar = list(df)

    plt.style.use("classic")
    fig = plt.figure(facecolor='white')
    #plt.suptitle("Time series about {} cluster".format(str(numerocl)), fontsize=16)
    color = []
    #colorset = []
    for item in clusternorm:
        if item == numerocl:
            color.append(pl.cm.jet(item/len(clustergiusti)))
        else:
            color.append([0.07,0.07,0.07,0.07])
    """
    for item in list(set(clusternorm)):
        if item == numerocl:
            colorset.append(pl.cm.jet(item/len(clustergiusti)))
        else:
            colorset.append([0.07,0.07,0.07,0.07])
    colorlegend = []
    colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[numerocl-1]))
    """ 
    a = [numerocl]
    
    su = compute_su(clusternorm, df, numerocl)
    j = 0
    expsI = list(pd.unique(experiment))
    if len(expsI) > 1:
        delimF = []
        for exp in expsI:
            delimF.append(next((i-1 for i in range(0,len(experiment)) if experiment[i]==exp)))
        lastF = delimF[0]
        if lastF == -1:
            lastF += len(experiment)
        del(delimF[0])
        delimF.append(lastF)
    start = 1
    if clust == 1:
        ax2 = fig.add_subplot(4,3,start)
        ax2 = to_scatter(ax2, seconds, clusternorm, 'observations', 'cluster', color, "colorlegend", a)
        ax2.set_title("Mapping observation to clusters")
        if len(expsI) > 1:
            for xc in delimF:
                plt.axvline(x=xc, color="red")
        start += 1
    if geo == 1:
        ax3 = fig.add_subplot(4,3,start)
        ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, "colorlegend", set(clusternorm)) 
        ax3.set_title("Geo-localization")
        start += 1
    for i in range(start, df.shape[1]+start):
        pos = su.index(max(su))
        ax3 = fig.add_subplot(4,3,i)
        ax3 = to_scatter(ax3, seconds, df[df.columns[j]], 'observations', labelvar[j], color, "colorlegend", set(clusternorm))
        ax3.set_title("SU= {0:.3f}".format(float(su[pos])))
        if len(expsI) > 1:
            for xc in delimF:
                plt.axvline(x=xc, color="red")
        ax3 = plt.gca()
        if percorsoG == "":
            if used_variables[j]==1:
                ax3.set_facecolor('#c7fdb5')
            else:
                ax3.set_facecolor('mistyrose')
        su[pos] = -1
        j = j+1
    
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.55, wspace = 0.3)
    return fig

def disegna_boxplot(meansI, percorsoD, percorsoS, percorsoG, norm, usedV, exp):
    
    """
    Caricamento dati
    """
    if percorsoS != "/":
        df, latitude, longitude, experiment = used_df(percorsoD, percorsoS, percorsoG, norm, usedV, exp=exp)
        clust, geo = "", ""
        if len(latitude) > 0:
            clust = usedV.pop(0)
            geo = usedV.pop(0)
        else:
            clust = usedV.pop(0)
        clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, percorsoG, exp=exp)
        color = [pl.cm.jet(item/len(clustergiusti)) for item in clusternorm]
        colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        seconds = range(0, len(clusternorm))
    else:
        df, latitudine, longitudine, experiment = get_dataset(percorsoD, percorsoS, False, exp)
        color = [[0,0,1,1] for item in range(0, df.shape[0])]
        colorset = color
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        seconds = range(0, df.shape[0])

    labelvar = list(df)
    
    righe,colonne = df.shape
    
    plt.style.use("classic")
    fig = plt.figure(facecolor='white')

    expsI = list(pd.unique(experiment))
    if percorsoS != "/":
        su = compute_su(clusternorm, df)
        if meansI != 0:
            #meansI = silhouette(percorsoD, percorsoS)
            if len(expsI) > 1:
                delimF = []
                for exp in expsI:
                    delimF.append(next((i-1 for i in range(0,len(experiment)) if experiment[i]==exp)))
                lastF = delimF[0]
                if lastF == -1:
                    lastF += len(experiment)
                del(delimF[0])
                delimF.append(lastF)
            start = 1
            if clust == 1:
                ax2 = fig.add_subplot(4,3,start)
                ax2 = to_scatter(ax2, seconds, clusternorm, 'observations', 'cluster', color, colorlegend, set(clusternorm))
                ax2.set_title("Mapping observation to clusters")
                if len(expsI) > 1:
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
                start += 1
            if  geo == 1:
                ax3 = fig.add_subplot(4,3,start)
                ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, colorlegend, set(clusternorm))            
                ax3.set_title("Geo-localization")
                start += 1
            r = 0
            freq = [[] for x in clustergiusti]
            for c in clusternorm:
                freq[int(c)-1].append(df.iloc[r,:])
                r = r+1
            #freq = [pd.DataFrame(freq[i]) for i in range(0,len(freq))]
            idx_means = np.argsort(meansI)[::-1][:len(meansI)]
            freqC = [pd.DataFrame(freq[i]) for i in range(0,len(freq))]
            for i in range(start,colonne+start):
                ax0 = fig.add_subplot(4,3,i)
                freq = np.array([freqC[x].iloc[:,i-start] for x in range(0,len(freqC))])
                freqF = freq[idx_means]
                labelF = [item+1 for item in idx_means]
                labelS = [k+1 for k in range(0, len(freq))]
                ax0.boxplot(freqF)
                plt.xticks(labelS, labelF)
                ax0.set_xlabel("SU= {0:.3f}".format(float(su[i-start])))
                ax0.set_ylabel(labelvar[i-start])
                ax0.grid(True)
        else:
            start = 1
            if clust == 1:
                ax2 = fig.add_subplot(4,3,start)
                ax2 = to_scatter(ax2, seconds, clusternorm, 'observations', 'cluster', color, colorlegend, set(clusternorm))
                ax2.set_title("Mapping observation to clusters")
                if len(expsI) > 1:
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
                start += 1
            if  geo == 1:
                ax3 = fig.add_subplot(4,3,start)
                ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, colorlegend, set(clusternorm))            
                ax3.set_title("Geo-localization")
                start += 1
            for i in range(start,colonne+start):
                pos = su.index(max(su))
                ax0 = fig.add_subplot(4,3,i)
                freq = [[] for x in clustergiusti]
                r = 0
                for c in clusternorm:
                    freq[int(c)-1].append(df.iloc[r,pos])
                    r = r+1
                ax0.boxplot(freq)
                ax0.set_xlabel("SU= {0:.3f}".format(float(su[pos])))
                ax0.set_ylabel(labelvar[i-start])
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

def ordina_boxplot(meansI, percorsoD, percorsoS, percorsoG, norm, numerocl, usedV, exp):
    
    
    df, latitude, longitude, experiment = used_df(percorsoD, percorsoS, percorsoG, norm, usedV, exp, numerocl)
    clust, geo = "", ""
    if percorsoG != "":
        clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, percorsoG)
        colonne = df.shape[1]
    else:
        clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, exp=exp)
        new_coN, new_coV = used_coord(percorsoD, percorsoS, usedV, norm, numerocl)
        righe,colonne = new_coN.shape
        coordinateNn = new_coN.values
        
        used_variables = []
        for i in range(0, righe):
            if i+1 == numerocl:
                for j in range(0, colonne):
                    if str(coordinateNn[i][j]) == 'nan':
                        used_variables.append(0)
                    else:
                        used_variables.append(1)
    if len(latitude) > 0:
        clust = usedV.pop(0)
        geo = usedV.pop(0)
    else:
        clust = usedV.pop(0)
    righe, colonne = df.shape
    
    seconds = range(0, len(clusternorm))
    labelvar = list(df)
    color = []
    #colorset = []
    for item in clusternorm:
        if item == numerocl:
            color.append(pl.cm.jet(item/len(clustergiusti)))
        else:
            color.append([0.07,0.07,0.07,0.07])
    """
    for item in list(set(clusternorm)):
        if item == numerocl:
            colorset.append(pl.cm.jet(item/len(clustergiusti)))
        else:
            colorset.append([0.07,0.07,0.07,0.07])
    colorlegend = []
    colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[numerocl-1]))
    """
    fig = plt.figure(facecolor='white')
    su = compute_su(clusternorm, df, numerocl)
    plt.style.use("classic")
    expsI = list(pd.unique(experiment))
    if meansI != 0:
        if len(expsI) > 1:
            delimF = []
            for exp in expsI:
                delimF.append(next((i-1 for i in range(0,len(experiment)) if experiment[i]==exp)))
            lastF = delimF[0]
            if lastF == -1:
                lastF += len(experiment)
            del(delimF[0])
            delimF.append(lastF)
        start = 1
        if clust == 1:
            ax2 = fig.add_subplot(4,3,start)
            ax2 = to_scatter(ax2, seconds, clusternorm, 'observations', 'cluster', color, "colorlegend", set(clusternorm))
            ax2.set_title("Mapping observation to clusters")
            if len(expsI) > 1:
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
            start += 1
        if  geo == 1:
            ax3 = fig.add_subplot(4,3,start)
            ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, "colorlegend", set(clusternorm))            
            ax3.set_title("Geo-localization")
            start += 1
        r = 0
        freq = [[] for x in clustergiusti]
        for c in clusternorm:
            freq[int(c)-1].append(df.iloc[r,:])
            r = r+1
        idx_means = np.argsort(meansI)[::-1][:len(meansI)]
        freqC = [pd.DataFrame(freq[i]) for i in range(0,len(freq))]
        for i in range(start, colonne+start):
            ax0 = fig.add_subplot(4,3,i)
            freq = np.array([freqC[x].iloc[:,i-start] for x in range(0,len(freqC))])
            freqF = freq[idx_means]
            labelF = [item+1 for item in idx_means]
            labelS = [k+1 for k in range(0, len(freq))]
            ax0.boxplot(freqF)
            plt.xticks(labelS, labelF)
            ax0.set_xlabel("SU= {0:.3f}".format(float(su[i-start])))
            ax0.set_ylabel(labelvar[i-start])
            ax0.grid(True)
            ax0 = plt.gca()
            if percorsoG == "":
                if used_variables[i-start] == 1:
                    ax0.set_facecolor('#c7fdb5')
                else:
                    ax0.set_facecolor('mistyrose')
    else:
        start = 1
        if clust == 1:
            ax2 = fig.add_subplot(4,3,start)
            ax2 = to_scatter(ax2, seconds, clusternorm, 'observations', 'cluster', color, "colorlegend", set(clusternorm))
            ax2.set_title("Mapping observation to clusters")
            if len(expsI) > 1:
                    for xc in delimF:
                        plt.axvline(x=xc, color="red")
            start += 1
        if  geo == 1:
            ax3 = fig.add_subplot(4,3,start)
            ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, "colorlegend", set(clusternorm))            
            ax3.set_title("Geo-localization")
            start += 1
        for i in range(start, colonne+start):
            pos = su.index(max(su))
            ax0 = fig.add_subplot(4,3,i)
            freq = [[] for x in clustergiusti]
            r = 0
            for c in clusternorm:
                freq[int(c)-1].append(df.iloc[r,pos])
                r = r+1
            ax0.boxplot(freq)
            ax0.set_xlabel("SU= {0:.3f}".format(float(su[pos])))
            ax0.set_ylabel(labelvar[i-start])
            ax0.grid(True)
            ax0 = plt.gca()
            if percorsoG == "":
                if used_variables[i-start] == 1:
                    ax0.set_facecolor('#c7fdb5')
                else:
                    ax0.set_facecolor('mistyrose')
            su[pos] = -1
        
    points = list(clusternorm).count(numerocl)
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3)
    return fig, points, len(clusternorm)
     
def disegna_barplot(percorsoD, percorsoS, percorsoG, norm, usedV, exp):
    
    if percorsoS != "/":
        df, latitude, longitude, experiment = used_df(percorsoD, percorsoS, percorsoG, norm, usedV, exp=exp)
        clust, geo = "", ""
        if len(latitude) > 0:
            clust = usedV.pop(0)
            geo = usedV.pop(0)
        else:
            clust = usedV.pop(0)
        clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, percorsoG, exp=exp)
        color = [pl.cm.jet(item/len(clustergiusti)) for item in clusternorm]
        colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        seconds = range(0, len(clusternorm))
    else:
        df, latitudine, longitudine, experiment = get_dataset(percorsoD, percorsoS, False, exp)
        color = [[0,0,1,1] for item in range(0, df.shape[0])]
        colorset = color
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        seconds = range(0, df.shape[0])
        
    labelvar = list(df)
    righe,colonne = df.shape
    
    """
    Grafici
    """
    
    plt.style.use("classic")
    fig = plt.figure(facecolor='white')
    expsI = list(pd.unique(experiment))
    if percorsoS != "/":
        su = compute_su(clusternorm, df)
        if len(expsI) > 1:
            delimF = []
            for exp in expsI:
                delimF.append(next((i-1 for i in range(0,len(experiment)) if experiment[i]==exp)))
            lastF = delimF[0]
            if lastF == -1:
                lastF += len(experiment)
            del(delimF[0])
            delimF.append(lastF)
        start = 1
        if clust == 1:
            ax2 = fig.add_subplot(4,3,start)
            ax2 = to_scatter(ax2, seconds, clusternorm, 'observations', 'cluster', color, colorlegend, set(clusternorm))
            ax2.set_title("Mapping observation to clusters")
            start += 1
            if len(expsI) > 1:
                for xc in delimF:
                    plt.axvline(x=xc, color="red")
        if  geo == 1:
            ax3 = fig.add_subplot(4,3,start)
            ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, colorlegend, set(clusternorm))            
            ax3.set_title("Geo-localization")
            start += 1
        for i in range(start,colonne+start):
            pos = su.index(max(su))
            ax0 = fig.add_subplot(4,3,i)
            ax0.hist(x=df[df.columns[pos]], bins=10, color="green")
            plt.title(labelvar[i-start]+"  SU= {0:.3f}".format(float(su[pos])))
            plt.grid(True)
            su[pos] = -1
    else:
        start = 1
        if clust == 1:
            ax2 = fig.add_subplot(4,3,start)
            ax2 = to_scatter(ax2, seconds, clusternorm, 'observations', 'cluster', color, colorlegend, set(clusternorm))
            ax2.set_title("Mapping observation to clusters")
            start += 1
            if len(expsI) > 1:
                for xc in delimF:
                    plt.axvline(x=xc, color="red")
        if  geo == 1:
            ax3 = fig.add_subplot(4,3,start)
            ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, colorlegend, set(clusternorm))            
            ax3.set_title("Geo-localization")
            start += 1
        for i in range(start, colonne+start):
            if usedV[i-start]==1:
                ax0 = fig.add_subplot(4,3,i)
                ax0.hist(x=df[df.columns[i-start]], bins=10, color="green")
                plt.title(labelvar[i-start])
                plt.grid(True)
    
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.55, wspace = 0.3)
    return fig

def highlight_barplot(percorsoD, percorsoS, percorsoG, norm, numerocl, usedV, exp):
    
    clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, percorsoG, exp=exp)
    df, latitude, longitude, experiment = used_df(percorsoD, percorsoS, percorsoG, norm, usedV, exp, numerocl)
    righe,colonne = df.shape
    
    new_coN, new_coV = used_coord(percorsoD, percorsoS, usedV, norm, numerocl)
    coordinateNn = new_coN.values
    
    used_variables = []
    for i in range(0, new_coN.shape[0]):
        if i+1 == numerocl:
            for j in range(0, new_coN.shape[1]):
                if str(coordinateNn[i][j]) == 'nan':
                    used_variables.append(0)
                else:
                    used_variables.append(1)
          
    clust, geo = "", ""
    if len(latitude) > 0:
        clust = usedV.pop(0)
        geo = usedV.pop(0)
    else:
        clust = usedV.pop(0)
    labelvar = list(df)
    seconds = range(0, len(clusternorm))
    
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
    
    fig = plt.figure(facecolor='white')  
    plt.style.use("classic")
    
    su = compute_su(clusternorm, df, numerocl)
    expsI = list(pd.unique(experiment))
    if len(expsI) > 1:
        delimF = []
        for exp in expsI:
            delimF.append(next((i-1 for i in range(0,len(experiment)) if experiment[i]==exp)))
        lastF = delimF[0]
        if lastF == -1:
            lastF += len(experiment)
        del(delimF[0])
        delimF.append(lastF)
    start = 1
    if clust == 1:
        ax2 = fig.add_subplot(4,3,start)
        ax2 = to_scatter(ax2, seconds, clusternorm, 'observations', 'cluster', color, colorlegend, set(clusternorm))
        ax2.set_title("Mapping observation to clusters")
        start += 1
        if len(expsI) > 1:
            for xc in delimF:
                plt.axvline(x=xc, color="red")
    if  geo == 1:
        ax3 = fig.add_subplot(4,3,start)
        ax3 = to_scatter(ax3, longitude, latitude, 'longitude', 'latitude', color, colorlegend, set(clusternorm))            
        ax3.set_title("Geo-localization")
        start += 1
    for i in range(start,colonne+start):
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
        ax0.set_title(labelvar[i-start]+"  SU={0:.3f}".format(float(su[pos])))
        plt.grid(True)
        ax0.bar(abins[:-1], ahist, width=w, color='green')
        ax0.bar(abins[:-1], bhist[1]-ahist, width=w, color='yellow')
        ax0 = plt.gca()
        if percorsoG == "":
            if used_variables[i-start] == 1:
                ax0.set_facecolor('#c7fdb5')
            else:
                ax0.set_facecolor('mistyrose')
        su[pos] = -1
    
    punti = list(clusternorm).count(numerocl)
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.55, wspace = 0.3)
    return fig, punti, len(clusternorm)

def scatter_2d(percorsoD, percorsoS, percorsoG, norm, var1, var2, numerocl=0, exp="All"):
        
    if percorsoS != "/":
        if percorsoG != "":
            clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, percorsoG)
        else:
            clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, exp=exp)
        df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm, exp)
        if numerocl == 0:
            color = [pl.cm.jet(item/len(clustergiusti)) for item in clusternorm]
            colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
            colorlegend = []
            for i in range(0,len(colorset)):
                colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        else:
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
    else:
        df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm, exp)
        color = [[0,0,1,1] for item in range(0, df.shape[0])]
        colorset = color
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
    labels = list(df)
    plt.style.use("classic")
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(1,1,1)
    if percorsoS != "/":
        if numerocl == 0:
            ax = to_scatter(ax, df[df.columns[var1]], df[df.columns[var2]], labels[var1], labels[var2], color, colorlegend, set(clusternorm))
        else:
            ax = to_scatter(ax, df[df.columns[var1]], df[df.columns[var2]], labels[var1], labels[var2], color, colorlegend, str(numerocl))
    else:
        ax = to_scatter(ax, df[df.columns[var1]], df[df.columns[var2]], labels[var1], labels[var2], color, colorlegend, ["1"])        
    ax.set_title("2D Scatter plot")
    return fig

def scatter_3d(percorsoD, percorsoS, percorsoG, norm, fig, var1, var2, var3, numerocl=0, exp="All"):
        
    if percorsoS != "/":
        if percorsoG != "":
            clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, percorsoG)
        else:
            clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, exp=exp)
        df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm, exp)
        if numerocl == 0:
            color = [pl.cm.jet(item/len(clustergiusti)) for item in clusternorm]
            colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
            colorlegend = []
            for i in range(0,len(colorset)):
                colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
        else:
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
    else:
        df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm, exp)
        color = [[0,0,1,1] for item in range(0, df.shape[0])]
        colorset = color
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
            
    labels = list(df)
    
    #plt.style.use("classic")
    #fig = plt.figure(facecolor='white')
    ax = fig.gca(projection='3d')
    #ax = fig.add_subplot(111, projection="3d")
    if percorsoS != "/":
        ax.scatter(xs=df[df.columns[var1]], ys=df[df.columns[var2]], zs=df[df.columns[var3]], c=color, edgecolors='face', s=2)
        ax.set_xlabel(labels[var1])
        ax.set_ylabel(labels[var2])
        ax.set_zlabel(labels[var3])
        ax.grid(True)
        #if numerocl == 0:
            #ax.legend(colorlegend, set(clusternorm), loc=4, fontsize=8, ncol=len(set(clusternorm)))
        #else:
            #ax.legend(colorlegend, str(numerocl), loc=4, fontsize=8, ncol=len(set(clusternorm)))
    else:
        ax.scatter(xs=df[df.columns[var1]], ys=df[df.columns[var2]], zs=df[df.columns[var3]], c=color, edgecolors='face', s=2)
        ax.set_xlabel(labels[var1])
        ax.set_ylabel(labels[var2])
        ax.set_zlabel(labels[var3])
        ax.grid(True)
        #ax.legend(colorlegend, ["1"], loc=4, fontsize=8, ncol=1)
    ax.set_title("3D Scatter plot")
    #plt.ion()
    return fig

def tsne(percorsoD, percorsoS, norm, numerocl=0):
        
    res = pd.read_csv(percorsoS+"/tsne.csv")
    clusters = res[res.columns[2]]
    df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm)
    if numerocl == 0:
        color = [pl.cm.jet(item/len(set(clusters))) for item in clusters]
        colorset = [pl.cm.jet(item/len(set(clusters))) for item in list(set(clusters))]
        colorlegend = []
        for i in range(0,len(colorset)):
            colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
    else:
        color = []
        colorset = []
        for item in clusters:
            if item == numerocl:
                color.append(pl.cm.jet(item/len(set(clusters))))
            else:
                color.append([0.07,0.07,0.07,0.07])
        for item in list(set(clusters)):
            if item == numerocl:
                colorset.append(pl.cm.jet(item/len(set(clusters))))
            else:
                colorset.append([0.07,0.07,0.07,0.07])
        colorlegend = []
        colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[numerocl-1]))
        a = [numerocl]
    plt.style.use("classic")
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(1,1,1)
    ax.scatter(res[res.columns[0]],res[res.columns[1]],c=color,edgecolors='face',s=2)
    ax.grid(True)
    if numerocl != 0:
        ax.legend(colorlegend, a, loc=4, fontsize=6)
    else:
        ax.legend(colorlegend, set(clusters), loc=4, fontsize=6, ncol=len(set(clusters)))
        
    return fig

def general_info(percorsoD, percorsoS, norm):
    
    clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS)
    df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm)
    righe,colonne = df.shape
    clusters = sorted(set(clusternorm))
    clusters = [int(item) for item in clusters]
    dfEle = pd.DataFrame()
    """
    for i in range(1,colonne+1):
        
        freq = [[] for x in clustergiusti]
        r = 0
        for c in clusternorm:
            freq[int(c)-1].append(df.iloc[r,i-1])
            r = r+1
    elementi = [len(item) for item in freq]
    dfEle = pd.DataFrame()
    
    vU = pd.read_table(percorsoS+"model_parameters.txt", delim_whitespace=True)
    righeU, colonneU = vU.shape
    vU = vU.values
    use = np.zeros(righeU)
    for i in range(0, righeU):
        for j in range(0, colonneU):
            if str(vU[i][j]) != 'nan':
                use[i] += 1
    #means = silhouette(percorsoD, percorsoS)
    """
    """OLD SILHOUETTE
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
    """
    
    """
    evalu = script.generate_evaluation(cl, np.full(len(cl), -1))
    dfEvalu = pd.DataFrame()
    listName = ["Accuracy", "CE", "F1", "Entropy", "NbCluster"]
    i=0
    for item in listName:
        dfEvalu[item] = [evalu[i]]
        i += 1
    """
    #dfGeneral = pd.read_csv(percorsoS+"generalInfo.csv", index_col=False)
    firstC = []
    secondC = []
    fileGeneral = open(percorsoS+"generalInfo.csv", 'r')
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
            method = lines.split(",")[1].strip()
            secondC.append(method)
        if l > 6 and l < 16 and method == "IHMM":
            firstC.append(lines.split(",")[0])
            secondC.append(lines.split(",")[1].strip())
        if l == 16 and method == "IHMM":
            riga = lines.split(",")
            firstC.append(riga[0])
            del riga[0]
            riga = [item.strip() for item in riga]
            secondC.append(str(riga))
        if (l == 17 or l == 18) and method == "IHMM":
            firstC.append(lines.split(",")[0])
            secondC.append(lines.split(",")[1].strip())
        if l > 18 and method == "IHMM":
            meansN.append(lines.split(",")[0].strip())
            elementi.append(lines.split(",")[1].strip())
            use.append(lines.split(",")[2].strip())
        if l > 6 and l <= 16 and method == "SubCMedians":
            firstC.append(lines.split(",")[0])
            secondC.append(lines.split(",")[1].strip())
        if l == 18 and method == "SubCMedians":
            riga = lines.split(",")
            firstC.append(riga[0])
            del riga[0]
            riga = [item.strip() for item in riga]
            secondC.append(str(riga))
        if (l == 19 or l == 20) and method == "SubCMedians":
            firstC.append(lines.split(",")[0])
            secondC.append(lines.split(",")[1].strip())
        if l > 20 and method == "SubCMedians":
            meansI.append(lines.split(",")[0])
            meansN.append(lines.split(",")[1].strip())
            elementi.append(lines.split(",")[2].strip())
            use.append(lines.split(",")[3].strip())
        if l > 6 and l < 14 and (method == "K-Means" or method == "GMM" or method == "Spectral Clustering"):
            firstC.append(lines.split(",")[0])
            secondC.append(lines.split(",")[1].strip())
        if l == 15 and method == "K-Means":
            riga = lines.split(",")
            firstC.append(riga[0])
            del riga[0]
            riga = [item.strip() for item in riga]
            secondC.append(str(riga))
        if (l == 16 or l == 17) and method == "K-Means":
            firstC.append(lines.split(",")[0])
            secondC.append(lines.split(",")[1].strip())
        if l > 17 and method == "K-Means":
            meansN.append(lines.split(",")[0].strip())
            elementi.append(lines.split(",")[1].strip())
            use.append(lines.split(",")[2].strip())
        if l == 16 and method == "GMM":
            riga = lines.split(",")
            firstC.append(riga[0])
            del riga[0]
            riga = [item.strip() for item in riga]
            secondC.append(str(riga))
        if (l == 17 or l == 18) and method == "GMM":
            firstC.append(lines.split(",")[0])
            secondC.append(lines.split(",")[1].strip())
        if l > 18 and method == "GMM":
            meansN.append(lines.split(",")[0].strip())
            elementi.append(lines.split(",")[1].strip())
            use.append(lines.split(",")[2].strip())
        if l == 15 and method == "Spectral Clustering":
            riga = lines.split(",")
            firstC.append(riga[0])
            del riga[0]
            riga = [item.strip() for item in riga]
            secondC.append(str(riga))
        if l == 16 and method == "Spectral Clustering":
            firstC.append(lines.split(",")[0])
            secondC.append(lines.split(",")[1].strip())
        if l > 16 and method == "Spectral Clustering":
            meansN.append(lines.split(",")[0].strip())
            elementi.append(lines.split(",")[1].strip())
            use.append(lines.split(",")[2].strip())
        if l > 6 and l < 18 and method == "TICC":
            firstC.append(lines.split(",")[0])
            secondC.append(lines.split(",")[1].strip())
        if l == 18 and method == "TICC":
            riga = lines.split(",")
            firstC.append(riga[0])
            del riga[0]
            riga = [item.strip() for item in riga]
            secondC.append(str(riga))
        if l == 19 and method == "TICC":
            firstC.append(lines.split(",")[0])
            secondC.append(lines.split(",")[1].strip())
        if l > 19 and method == "TICC":
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
    if method == "SubCMedians":
        """
        clustersF = []
        elementiF = []
        meansF = []
        meansNF = []
        useF = []
        means = list(np.copy(meansI))
        for i in range(0, len(clusters)):
            pos = means.index(max(means))
            useF.append(int(use[pos]))
            clustersF.append(int(clusters[pos]))
            elementiF.append(elementi[pos])
            meansF.append(means[pos])
            meansNF.append(meansN[pos])
            means[pos] = -2
        """   
        dfEle["Model"] = clusters
        dfEle["N. points"] = elementi
        dfEle["Sil. in Subspace"] = meansI
        dfEle["Silhouette"] = meansN
        dfEle["N. variables"] = use
        dfEle = dfEle.sort_values("Sil. in Subspace", ascending=False)
    if method == "K-Means" or method == "GMM" or method == "Spectral Clustering" or method == "TICC" or method == "IHMM":
        """
        clustersF = []
        elementiF = []
        meansF = []
        meansNF = []
        useF = []
        means = list(np.copy(meansN))
        for i in range(0, len(clusters)):
            pos = means.index(max(means))
            useF.append(int(use[pos]))
            clustersF.append(int(clusters[pos]))
            elementiF.append(elementi[pos])
            meansF.append(means[pos])
            means[pos] = -2
        """    
        dfEle["Model"] = clusters
        dfEle["N. points"] = elementi
        dfEle["Silhouette"] = meansN
        dfEle["N. variables"] = use
        dfEle = dfEle.sort_values("Silhouette", ascending=False)
        #dfEle["N. variables"] = useF

    return dfEle, dfGeneral

def geo_localization(percorsoD, percorsoS, usedExp="", numerocl=0, exp="All"):
        
    clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, exp=exp)
    df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, False, exp)
    plt.style.use("classic")
    fig = plt.figure(facecolor='white')
    if numerocl == 0:
        color = [pl.cm.jet(item/len(clustergiusti)) for item in clusternorm]
        #colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
        #colorlegend = []
    else:
        color = []
        #colorset = []
        for item in clusternorm:
            if item == numerocl:
                color.append(pl.cm.jet(item/len(clustergiusti)))
            else:
                color.append([0.07,0.07,0.07,0.07])
        """
        for item in list(set(clusternorm)):
            if item == numerocl:
                colorset.append(pl.cm.jet(item/len(clustergiusti)))
            else:
                colorset.append([0.07,0.07,0.07,0.07])
        colorlegend = []
        colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[numerocl-1]))
        
    for i in range(0,len(colorset)):
        colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))
    """
    if len(list(pd.unique(experiment))) > 1:
        if usedExp != "":
            expsI = list(pd.unique(experiment))
            exps = []
            for i in range(0,len(usedExp)):
                if usedExp[i] == 1:
                    exps.append(expsI[i])
        delimI = []
        delimF = []
        for exp in expsI: 
            delimI.append(next((i for i in range(0,len(experiment)) if experiment[i]==exp)))
        for exp in expsI:
            delimF.append(next((i-1 for i in range(0,len(experiment)) if experiment[i]==exp)))
        lastF = delimF[0]
        if lastF == -1:
            lastF += len(experiment)
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
            ax = fig.add_subplot(3,2,i)
            ax = to_scatter(ax, longitude[uDelimI[i-1]:uDelimF[i-1]], latitude[uDelimI[i-1]:uDelimF[i-1]], "longitude", "latitude", color[uDelimI[i-1]:uDelimF[i-1]], "colorlegend", set(clusternorm))
            ax.set_title(exps[i-1])
            """
            m = folium.Map(location =[np.mean(latitude[uDelimI[i-1]:uDelimF[i-1]]) , np.mean(longitude[uDelimI[i-1]:uDelimF[i-1]])], zoom_start=20)
            for point in range(uDelimI[i-1], uDelimF[i-1]):
                colore = color[point]
                colore = list(colore)
                colore.pop(3)
                colore = [item*255 for item in colore]
                colore = tuple(colore)
                folium.RegularPolygonMarker(location=[latitude[point], longitude[point]], opacity=0, radius=1, fill_color='#%02x%02x%02x' % colore).add_to(m)
            print "finish"
            m.fit_bounds(bounds=[[min(latitude[uDelimI[i-1]:uDelimF[i-1]]),min(longitude[uDelimI[i-1]:uDelimF[i-1]])], [max(latitude[uDelimI[i-1]:uDelimF[i-1]]), max(longitude[uDelimI[i-1]:uDelimF[i-1]])]])
            m.save(percorsoS+"tmp{}.html".format(i))
            """
    else:
        ax = fig.add_subplot(1,1,1)
        ax = to_scatter(ax, longitude, latitude, "longitude", "latitude", color, "colorlegend", set(clusternorm))
    
    plt.subplots_adjust(top = 0.95, bottom = 0.09, hspace = 0.4, wspace = 0.3)
    
    return fig

def sort_var(percorsoD, percorsoS, percorsoG, numerocl=0):
    
    if percorsoG != "":
        clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS, percorsoG)
    else:
        clusternorm, clustergiusti, cl = get_cl(percorsoD, percorsoS)
    df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, False)
    su = compute_su(clusternorm, df, numerocl)
    """
    new_order = []
    for i in range(0, df.shape[1]):
        pos = su.index(max(su))
        new_order.append(pos)
        su[pos] = -1
    return new_order
    """
    return np.argsort(su)[::-1][:len(su)] #descending

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

def get_dataset(percorsoD, percorsoS="", norm=False, exp="All", timeserie=False):

    ds = open(percorsoD)
    dialect = csv.Sniffer().sniff(ds.read(10000))
    ds.close()
    if norm == False:
        try:
            df = pd.read_csv(percorsoD, sep=dialect.delimiter)
            labels = list(df)
            fileDN = pd.read_csv(percorsoS+"dataStandardization.csv")
            var = fileDN.shape[0]
            fileDN = fileDN.values
            for i in range(0, var):
                varName = fileDN[i][0]
                mean = float(fileDN[i][1])
                std = float(fileDN[i][2])
                df[df.columns[labels.index(str(varName))]] = df[df.columns[labels.index(str(varName))]]*std+mean
        except:
            df = pd.read_csv(percorsoD, sep=dialect.delimiter)
    else:
        df = pd.read_csv(percorsoD, sep=dialect.delimiter)
    labelvar = list(df)
    latitude = []
    longitude = []
    experiment = []
    if "experiment" in labelvar:
        experiment = df[df.columns[labelvar.index('experiment')]]
        df.drop(df.columns[labelvar.index('experiment')],axis=1, inplace=True)
        if exp != "All":
            exps = list(pd.unique(experiment))
            delimI = list(experiment).index(exp)
            if exps.index(exp)+1 < len(exps):
                delimF = list(experiment).index(exps[exps.index(exp)+1])-1
            else:
                delimF = len(experiment)
            df = df[delimI:delimF]
            experiment = experiment[delimI:delimF]
    labelvar = list(df)
    if "latitude" in labelvar:
        latitude = df[df.columns[labelvar.index('latitude')]]
        df.drop(df.columns[labelvar.index('latitude')],axis=1, inplace=True)
    labelvar = list(df)
    if "longitude" in labelvar:
        longitude = df[df.columns[labelvar.index('longitude')]]
        df.drop(df.columns[labelvar.index('longitude')],axis=1, inplace=True)
    """
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
    """
    """
    colonne = df.shape[1]-1    
    for column in range(0, df.shape[1]):
        colonna = df[df.columns[colonne]]
        for value in colonna:
                foo = re.search('[a-zA-Z]', str(value))
                if re.search('[a-zA-Z]', str(value)) != None and foo.string[foo.start():foo.end()] != 'e' :
                    print foo.string[foo.start():foo.end()]
                    raise ValueError("Non-numerical values in dataset") 
        colonne-=1
    """
    date = []
    if timeserie == True:
        date = df.to_datetime(df)
    try:
        df = df.astype(float)
    except:
        print("Non-numerical values in dataset")
        raise ValueError
    if len(date) != 0:
        return df, latitude, longitude, experiment, timeserie
    else:
        return df, latitude, longitude, experiment

def get_cl(percorsoD, percorsoS, percorsoG="", exp="All"):
    
    if percorsoG != "":
        cl = open(percorsoG, 'r').readlines()
    else:
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
    if exp != "All":
        df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, False, "All")
        exps = list(pd.unique(experiment))
        delimI = list(experiment).index(exp)
        if exps.index(exp)+1 < len(exps):
            delimF = list(experiment).index(exps[exps.index(exp)+1])-1
        else:
            delimF = len(experiment)
        return clusternorm[delimI:delimF], clustergiusti, cl[delimI:delimF]
    else:
        return clusternorm, clustergiusti, cl

def used_df(percorsoD, percorsoS, percorsoG, norm, usedV, exp="All", numero=0):
    
    use = list(np.copy(usedV))
    use = [bool(item) for item in use]
    df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm, exp)
    if len(latitude) > 0:
        del(use[0])
        del(use[0])
    else:
        del(use[0])
    if percorsoG != "":
        if numero !=0:
            order = sort_var(percorsoD, percorsoS, percorsoG, numero)
        else:
            order = sort_var(percorsoD, percorsoS, percorsoG)
    else:
        if numero !=0:
            order = sort_var(percorsoD, percorsoS, "", numero)
        else:
            order = sort_var(percorsoD, percorsoS, "")
    ord_df = df[df.columns[order]].T
    """
    ord_df = []
    for i in range(0, len(order)):
       ord_df.append(df[df.columns[order[i]]])
    ord_df = pd.DataFrame(ord_df).T
    """
    """
    new_df = []
    for i in range(0, len(use)):
        if use[i] == 1:
            new_df.append(ord_df[ord_df.columns[i]])
    new_df = pd.DataFrame(new_df).T
    """
    new_df = ord_df[use]
    return new_df.T, latitude, longitude, experiment

def used_coord(percorsoD, percorsoS, usedV, norm, numero=0):
    
    coordinateN = pd.read_table(percorsoS+'model_parameters.txt', delim_whitespace=True)
    use = list(np.copy(usedV))
    use = [bool(item) for item in use]
    df, latitude, longitude, experiment = get_dataset(percorsoD, percorsoS, norm, "All")
    if len(latitude) > 0:
        del(use[0])
        del(use[0])
    else:
        del(use[0])
    if numero != 0:
        order = sort_var(percorsoD, percorsoS, "", numero)
    else:
        order = sort_var(percorsoD, percorsoS, "")
    """
    ord_coN = []
    for i in range(0, len(order)):
       ord_coN.append(coordinateN[coordinateN.columns[order[i]]])
    ord_coN = pd.DataFrame(ord_coN).T
    new_coN = []
    for i in range(0, len(use)):
        if use[i] == 1:
            new_coN.append(ord_coN[ord_coN.columns[i]])
    new_coN = pd.DataFrame(new_coN).T
    """
    ord_coN = coordinateN[coordinateN.columns[order]].T
    new_coN = ord_coN[use].T
    #coordinateV = pd.read_table(percorsoS+'model_parameters.txt', delim_whitespace=True)
    #order = sort_var(percorsoD, percorsoS)
    """
    ord_coV = []
    for i in range(0, len(order)):
       ord_coV.append(coordinateV[coordinateV.columns[order[i]]])
    ord_coV = pd.DataFrame(ord_coV).T
    new_coV = []
    for i in range(0, len(use)):
        if use[i] == 1:
            new_coV.append(ord_coV[ord_coV.columns[i]])
    new_coV = pd.DataFrame(new_coV).T
    """
    return new_coN, new_coN
