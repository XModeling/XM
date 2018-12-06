#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 23:59:55 2018

@author: caste
"""
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.pylab as pl
import random
#from ggplot import *


data_file = "/home/whitebreeze/XM_v1.3.3/RESULTS/INT_VARS/ALL_h_std_interestingVars.csv"

sep=","
data=pd.read_csv(data_file, sep=sep) # Load csv
data.shape
data=data.iloc[:,0:(data.shape[1]-3)] # <-- Set variables
labelvar=list(data)
nSelObs=7000 # 4000
rndSel=random.sample(range(data.shape[0]), nSelObs) # Random selection
data1=data.iloc[rndSel,:]

# Load clustering
cl_file = "/home/whitebreeze/XM_v1.3.3/RESULTS/INT_VARS/TEST6/cl.txt"
sep=","
cl=pd.read_csv(cl_file, sep=sep,header=None) # Load csv 
# Sampling
cl1 = cl.iloc[rndSel].values
# Legend preparation
cl1 = list(cl1)
cl1 = [float(item) for item in cl1]
clusternorm = np.copy(cl1)
clustergiusti = sorted(set(cl1))
for item in range(0, len(clustergiusti)):
    arraysupp = np.arange(len(cl1))
    arraysupp = [(item+1) for i in arraysupp]
    indexes = [i for i,x in enumerate(cl1) if x == clustergiusti[item]]
    for i in range(0,len(indexes)):
        clusternorm[indexes[i]] = arraysupp[indexes[i]]

numerocl = 0 #change number to highlight on graph =0->ALL, !=0->selected_model
        
color = []
colorset = []
if numerocl != 0:     
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
else:
    color = [pl.cm.jet(item/len(clustergiusti)) for item in clusternorm]
    colorset = [pl.cm.jet(item/len(clustergiusti)) for item in list(set(clusternorm))]
    colorlegend = []
    for i in range(0,len(colorset)):
        colorlegend.append(mpatches.Rectangle((0,0),1,1,fc=colorset[i]))    

# t-SNE
data_embedded_TSNE = TSNE(n_components=2,init='pca', verbose=1,random_state=0).fit_transform(data1)
data_embedded_TSNE.shape
# Plot
plt.scatter(data_embedded_TSNE[:,0],data_embedded_TSNE[:,1],c=color,edgecolors='face',s=2)
plt.grid(True)
if numerocl != 0:
    plt.legend(colorlegend, a, loc=4, fontsize=6)
else:
    plt.legend(colorlegend, set(clusternorm), loc=4, fontsize=6, ncol=len(set(clusternorm)))
plt.show()
plt.savefig('/media/caste/OS/myDisk/Uni/Research/intcatch/code/subspaceClustering/XM/XM_v1.3.3/RESULTS/SAC2019/TEST6/images/all_r_tsne_initPca_7000samples.png')
