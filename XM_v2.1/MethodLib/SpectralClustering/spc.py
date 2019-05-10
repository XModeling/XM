#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 14:58:28 2018

@author: whitebreeze
"""

from sklearn.cluster import SpectralClustering
import pandas as pd
import csv
import SM2
import numpy as np
import re
import os
from evaluationfunctions import accuracy,ce,entropy,f1,rnia
from collections import defaultdict

def purity(clusters_found, clusters_hidden):
    labels_conc = list(clusters_hidden)
    cl = list(clusters_found)
    labels = list(set(labels_conc))
    numb = defaultdict()
    label_tmp = defaultdict()
    for label in labels:
        numb[label] = []
    for c in list(set(cl)):
        indexes = [i for i, m in enumerate(cl) if m == c]
        for label in labels:
            label_tmp[label] = 0
        for index in indexes:
            label_tmp[labels_conc[index]] += 1
        for label in labels:
            numb.get(label).append(float(label_tmp.get(label))/len(indexes))
    data = pd.DataFrame()
    for label in labels:
        data[str(label)] = numb[int(label)]
    purity = []
    for i in range(0, data.shape[0]):
        riga = data.iloc[i,:]
        purity.append(max(riga))
    return np.mean(purity)

def silhouette_sub(percorsoD, percorsoS):

    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    df, latitude, longitude, experiment = get_dataset(percorsoD)
    coordinateN = pd.read_table(percorsoS+'/model_parameters.txt', delim_whitespace=True).values
    means = []
    r = 0
    for i in clustergiusti:
        mask = np.copy(cl)
        """  Così coincide senza mascherare
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
        print dfP.shape
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

def generate_evaluation(clusters_found, clusters_hidden):
    accuracy_local = accuracy(cluster_hidden=clusters_hidden,cluster_found=clusters_found)
    ce_local = ce(cluster_hidden=clusters_hidden,cluster_found=clusters_found)
    #rnia_local = rnia(cluster_hidden=clusters_hidden, cluster_found=clusters_found)
    f1_local = f1(cluster_hidden=clusters_hidden, cluster_found=clusters_found)
    entropy_local = entropy(cluster_hidden=clusters_hidden, cluster_found=clusters_found)
    purity_local = purity(clusters_found, clusters_hidden)
    nb_clusters = np.unique(clusters_found).size
    return [accuracy_local, ce_local, f1_local, entropy_local, purity_local, nb_clusters]

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

def general_info(righe=0, colonne=0, nclust=0, percorsoD="/", percorsoS="/", accuracy_local="Nan", ce_local="Nan", f1_local="Nan", entropy_local="Nan", purity_local='Nan', nb_clusters=0):
    gi = pd.DataFrame()
    df, latitude, longitude, experiment = get_dataset(percorsoD)
    varU = list(df)
    gi["Parameter"] = [ "Dataset Path","Results Path","Number of columns","Number of rows","Method","N. Cluster","Accuracy","CE","F1","Entropy","Purity","NbClusterFound","Note"]
    gi["Values"] = [percorsoD, percorsoS, colonne, righe, "Spectral Clustering", nclust, accuracy_local, ce_local, f1_local, entropy_local, purity_local, nb_clusters,"-"]
    gi.to_csv(path_or_buf=percorsoS+"/generalInfo.csv", columns=["Parameter","Values"], index=False)
    fileG = open(percorsoS+"/generalInfo.csv", 'a')
    fileG.write("Variables,")
    for var in varU:
        fileG.write(var+",")
    fileG.seek(-1, os.SEEK_END)
    fileG.truncate()
    fileG.write("\n")
    #print "[XM]> Computing SILHOUETTE (subspaces)"
    #clSS = silhouette_sub(percorsoD, percorsoS)
    print "[XM]> Computing SILHOUETTE (dataset)"
    clSN = silhouette(percorsoD, percorsoS)
    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    n_points = [list(clusternorm).count(c) for c in set(clusternorm)]
    sil_tot = sum([item*n_points[i] for i,item in enumerate(clSN)])/sum(n_points)
    fileG.write("Silhouette total,{}\n".format(sil_tot))
    i = 0
    for clS in clSN:
        fileG.write("{0:.3f}".format(clS)+",{}".format(n_points[i])+",{}\n".format(len(varU)))
        i += 1
    fileG.seek(-1, os.SEEK_END)
    fileG.truncate()
    fileG.close()
    print "[XM]> General Info generated"

def spectral(numerocl, percorsoD="", percorsoS="", percorsoG="", percorsoDN=""):

    percorsoS = percorsoS+"/SpectralClustering"
    if not os.path.exists(percorsoS):
        os.makedirs(percorsoS)
    df, latitude, longitude, experiments = get_dataset(percorsoD)
    spc = SpectralClustering(n_clusters=int(numerocl), n_jobs=-1, n_init=300)
    print "[XM]> ====== Creating Spectral Clustering Model ======"
    spc = spc.fit(df)
    results = spc.labels_
    print "[XM]> Generating results files"
    fileClusters = open(percorsoS+"/cl.txt","w")
    for item in results:
        fileClusters.write("%s\n"% item)
    fileClusters.close()
    print "[XM]> Clustering generated"
    centroids = spc.affinity_matrix_
    centroids = pd.DataFrame(centroids).to_string()
    centri = open(percorsoS+"/model_parameters.txt","w")
    centri.write("{}".format(centroids))
    centri.close()
    print "[XM]> Model parameters generated"
    if percorsoG != "":
        y = open(percorsoG,'r').readlines()
        y = [float(item) for item in y]
        df_evaluation = pd.DataFrame()
        df_evaluation["clusters_found"] = list(spc.labels_)
        df_evaluation["clusters_hidden"] = list(y)
        clusters_found = df_evaluation["clusters_found"]
        clusters_hidden = df_evaluation["clusters_hidden"]
        evaluation_temp =generate_evaluation(clusters_found, clusters_hidden)
        general_info(righe=df.shape[0], colonne=df.shape[1], nclust=numerocl, percorsoD=percorsoD, percorsoS=percorsoS, accuracy_local=evaluation_temp[0], ce_local=evaluation_temp[1], f1_local=evaluation_temp[2], entropy_local=evaluation_temp[3], purity_local=evaluation_temp[4], nb_clusters=pd.unique(results).size)
        if percorsoDN != "":
            fileDN = open(percorsoDN, 'r')
            fileDND = open(percorsoS+"/dataStandardization.csv", 'w')
            for line in fileDN:
                fileDND.write(line)
            fileDN.close()
            fileDND.close()
    else:
        general_info(righe=df.shape[0], colonne=df.shape[1], nclust=numerocl, percorsoD=percorsoD, percorsoS=percorsoS, accuracy_local="NA", ce_local="NA", f1_local="NA", entropy_local="NA", purity_local="NA", nb_clusters=pd.unique(results).size)
        if percorsoDN != "":
            fileDN = open(percorsoDN, 'r')
            fileDND = open(percorsoS+"/dataStandardization.csv", 'w')
            for line in fileDN:
                fileDND.write(line)
            fileDN.close()
            fileDND.close()


#kmeans(5, "/home/whitebreeze/XM_v1.3.4/RESULTS/CASTE/SubCMedians/ALL_pro_std.csv", "/home/whitebreeze/XM_v1.3.4/RESULTS/CASTE/K-Means/", "", "/home/whitebreeze/XM_v1.3.4/RESULTS/CASTE/SubCMedians/dataStandardization.csv" )