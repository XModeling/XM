#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 09:56:06 2019

@author: francesco
"""

from MethodLib.GMM import gmm
from MethodLib.KMeans import km
from MethodLib.SpectralClustering import spc
from MethodLib.SubCMedians import subc
from MethodLib.TICC import ticc
import os

actualPath = str(os.path.dirname(os.path.abspath(__file__)))
pathD = actualPath+"/DATASETS/xm_test_dataset.csv" 
pathS = actualPath+"/RESULTS/XM_TEST_RESULTS/" #eventually change directory path


print("Generating GMM results for test data")
gmm.gmm(5, "full", 10, pathD, pathS)


print("Generating KM results for test data")
km.kmeans(5, pathD, pathS)


print("Generating Spectral clustering results for test data")
spc.spectral(5, pathD, pathS)


print("Generating SubCMedians results for test data")
subc.genera_cluster(5,0,0,0,pathD,pathS)


print("Generating TICC results for test data")
ticc.genera_cluster(5,1,0.5,150,pathD,pathS)