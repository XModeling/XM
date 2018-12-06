#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 20:37:43 2018

@author: whitebreeze
"""

import pandas as pd
import os
import csv
import re 
import numpy as np
import SM2

def silhouette_sub(percorsoD, percorsoS):

    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    df, latitude, longitude, experiment = get_dataset(percorsoD)
    coordinateN = pd.read_table(percorsoS+'/model_parameters.txt', delim_whitespace=True).values
    means = []
    r = 0
    for i in clustergiusti:
        mask = np.copy(cl)
        """
        for m in range(0, len(mask)):
            if mask[m] == i:
                mask[m] = 1
            else:
                mask[m] = 0
        """
        dfP = pd.DataFrame()
        for colonne in range(0, coordinateN.shape[1]):
            if str(coordinateN[r][colonne]) != "nan":
                dfP[str(colonne)] = df[df.columns[colonne]]
        #silhouette = sm.silhouette_samples_memory_saving(dfP, mask)
        #silhouette = sk.silhouette_samples(dfP, mask)
        print "[XM]> {0:.2f}%".format(float(float(r)/len(clustergiusti))*100)
        silhouette = SM2.silhouette_samples_memory_saving(dfP, mask)
        sumT = 0
        indexes = [j for j,x in enumerate(mask) if x == i]
        for i in range(0,len(indexes)):
            sumT += silhouette[indexes[i]]
        means.append(sumT/len(indexes))
        r += 1
    print "[XM]> 100%"
    return means

def silhouette(percorsoD, percorsoS):
    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    df, latitude, longitude, experiment = get_dataset(percorsoD)
    silhouette = SM2.silhouette_samples_memory_saving(df, cl)
    print "[XM]> Computed"
    means = []
    for item in range(0, len(clustergiusti)):
        sumT = 0
        arraysupp = np.arange(len(cl))
        arraysupp = [(item+1) for i in arraysupp]
        indexes = [i for i,x in enumerate(cl) if x == clustergiusti[item]]
        for i in range(0,len(indexes)):
            sumT += silhouette[indexes[i]]
        means.append(sumT/len(indexes))
    return means

def get_cl(percorsoS, percorsoG=""):
    
    if percorsoG != "":
        cl = open(percorsoG, 'r').readlines()
    else:
        cl = open(percorsoS+'/cl.txt','r').readlines()
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

def get_dataset(percorsoD):

    ds = open(percorsoD)
    dialect = csv.Sniffer().sniff(ds.read(10000))
    ds.close()
    df = pd.read_csv(percorsoD, sep=dialect.delimiter)
    
    labelvar = list(df)
    latitude = []
    longitude = []
    experiment = []
    if "latitude" in labelvar:
        latitude = df[df.columns[labelvar.index('latitude')]]
        df.drop(df.columns[labelvar.index('latitude')],axis=1, inplace=True)
    labelvar = list(df)
    if "longitude" in labelvar:
        longitude = df[df.columns[labelvar.index('longitude')]]
        df.drop(df.columns[labelvar.index('longitude')],axis=1, inplace=True)
    labelvar = list(df)
    if "experiment" in labelvar:
        experiment = df[df.columns[labelvar.index('experiment')]]
        df.drop(df.columns[labelvar.index('experiment')],axis=1, inplace=True)
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
                    raise ValueError("Non-numerical values in dataset") 
        colonne-=1
    return df, latitude, longitude, experiment

def general_info(righe=0, colonne=0, NbExpClust=0, SDmax=0, N=0, NbIter=0, percorsoD="/", percorsoS="/", accuracy_local="Nan", ce_local="Nan", f1_local="Nan", entropy_local="Nan", nb_clusters=0):
    gi = pd.DataFrame()
    df, latitude, longitude, experiment = get_dataset(percorsoD)
    varU = list(df)
    gi["Parameter"] = [ "Dataset_Path","Results_Path","Number_of_columns","Number_of_rows","Method","NbExpCluster","SDmax","N","NbIter","Accuracy","CE","F1","Entropy","NbClusterFound","Note"]
    gi["Values"] = [percorsoD, percorsoS, colonne, righe, "SubCMedians", NbExpClust, SDmax, N, NbIter, accuracy_local, ce_local, f1_local, entropy_local, nb_clusters,"-"]
    gi.to_csv(path_or_buf="/home/whitebreeze/XM_v1.3.4/REDO/generalInfo.csv", columns=["Parameter","Values"], index=False)
    fileG = open("/home/whitebreeze/XM_v1.3.4/REDO/generalInfo.csv", 'a')
    fileG.write("Variables,")
    for var in varU:
        fileG.write(var+",")
    fileG.seek(-1, os.SEEK_END)
    fileG.truncate()
    fileG.write("\n")
    print "[XM]> Computing SILHOUETTE (subspaces)"
    clSS = silhouette_sub(percorsoD, percorsoS)
    print "[XM]> Computing SILHOUETTE (dataset)"
    clSN = silhouette(percorsoD, percorsoS)
    i = 0
    for clS in clSS:
        fileG.write("{0:.3f}".format(clS)+",{0:.3f}".format(clSN[i])+"\n")
        i += 1
    fileG.seek(-1, os.SEEK_END)
    fileG.truncate()
    fileG.close()
    print "[XM]> General Info generated"
    

general_info(20187, 9, "-", 90, 500, 18000, "/home/whitebreeze/GI_REDO/datasets/Test7/ALL_pro_onlySd_std.csv","/home/whitebreeze/GI_REDO/AlbertoFrancesco/TEST7", "NA", "NA", "NA", "NA", 20)