import pandas as pd
import numpy as np
from SubCMediansLib.pySubCMedians import SubCMedians
from SubCMediansLib.EvaluationUtil.evaluationfunctions import accuracy,ce,entropy,f1,rnia
import time
import sys
from scipy import stats
import csv
import re
import os
import SM2

seed=1
np.random.seed(seed)

def silhouette(percorsoD, percorsoS):

    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    df, latitude, longitude, experiment = get_dataset(percorsoD)
    coordinateN = pd.read_table(percorsoS+'/model_parameters.txt', delim_whitespace=True).values
    means = []
    r = 0
    for i in clustergiusti:
        mask = np.copy(cl)
        for m in range(0, len(mask)):
            if mask[m] == i:
                mask[m] = 1
            else:
                mask[m] = 0
        dfP = pd.DataFrame()
        for colonne in range(0, coordinateN.shape[1]):
            if str(coordinateN[r][colonne]) != "nan":
                dfP[str(colonne)] = df[df.columns[colonne]]
        #silhouette = sm.silhouette_samples_memory_saving(dfP, mask)
        #silhouette = sk.silhouette_samples(dfP, mask)
        print "{0:.2f}%".format(float(float(r)/len(clustergiusti))*100)
        silhouette = SM2.silhouette_samples_memory_saving(dfP, mask)
        sumT = 0
        indexes = [i for i,x in enumerate(mask) if x == 1]
        for i in range(0,len(indexes)):
            sumT += silhouette[indexes[i]]
        means.append(sumT/len(indexes))
        r += 1
    print "100%"
    return means

def general_info(righe=0, colonne=0, NbExpClust=0, SDmax=0, N=0, NbIter=0, percorsoD="/", percorsoS="/", accuracy_local="Nan", ce_local="Nan", f1_local="Nan", entropy_local="Nan", nb_clusters=0):
    gi = pd.DataFrame()
    df, latitude, longitude, experiment = get_dataset(percorsoD)
    varU = list(df)
    gi["Parameter"] = [ "Dataset_Path","Results_Path","Number_of_columns","Number_of_rows","Method","NbExpCluster","SDmax","N","NbIter","Accuracy","CE","F1","Entropy","NbClusterFound","Note"]
    gi["Values"] = [percorsoD, percorsoS, colonne, righe, "SubCMedians", NbExpClust, SDmax, N, NbIter, accuracy_local, ce_local, f1_local, entropy_local, nb_clusters,"-"]
    gi.to_csv(path_or_buf=percorsoS+"/generalInfo.csv", columns=["Parameter","Values"], index=False)
    fileG = open(percorsoS+"/generalInfo.csv", 'a')
    fileG.write("Variables,")
    for var in varU:
        fileG.write(var+",")
    fileG.seek(-1, os.SEEK_END)
    fileG.truncate()
    fileG.write("\n")
    print "Computing SILHOUETTE"
    clS = silhouette(percorsoD, percorsoS)
    for cl in clS:
        fileG.write("{0:.3f}".format(cl)+"\n")
    fileG.seek(-1, os.SEEK_END)
    fileG.truncate()
    fileG.close()
    print "General Info generated"
    
def generate_evaluation(clusters_found, clusters_hidden):
    accuracy_local = accuracy(cluster_hidden=clusters_hidden,cluster_found=clusters_found)
    ce_local = ce(cluster_hidden=clusters_hidden,cluster_found=clusters_found)
    #rnia_local = rnia(cluster_hidden=clusters_hidden, cluster_found=clusters_found)
    f1_local = f1(cluster_hidden=clusters_hidden, cluster_found=clusters_found)
    entropy_local = entropy(cluster_hidden=clusters_hidden, cluster_found=clusters_found)
    nb_clusters = np.unique(clusters_found).size
    return [accuracy_local, ce_local, f1_local, entropy_local, nb_clusters]

def get_evaluation_string(evaluations, evaluation_names):
	txt = ""
	for i,evalu in enumerate(evaluations):
		txt += evaluation_names[i]+"="+"{0:.2f}".format(evalu)+" "
	return txt

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

def genera_cluster(NbExpClust=0, SDmax=0, N=0, NbIter=0, percorsoD="/", percorsoS="/", percorsoG="/", percorsoDN=""):
    
    # Read the dataset
    base_name = percorsoD
    file_name = base_name
    df, latitude, longitude, experiment = get_dataset(file_name)
    df = df.astype(float)
    """
    XClust
    
    cols = list(df)
    for col in cols:   
        col_pp = col + '_ppscore'
        pp_score = (df[col]+2)
        df[col_pp] = pp_score
    
    j = len(cols)-1 
    for i in range(0, len(cols)):
        df.drop(df.columns[j],axis=1, inplace=True)
        j-=1
    """
    D = df.shape[1]
    if SDmax==0 and N==0 and NbIter==0:
    
        SDmaxC = int(D * int(NbExpClust))
        NC = 25 * int(NbExpClust)
        NbIterC = 10 * SDmaxC * int(NbExpClust)
    else:
        
        SDmaxC = int(SDmax)
        NC = int(N)
        NbIterC = int(NbIter)
    
    # Create SubCMedians Instance
    scm = SubCMedians(D = D,
    				  SDmax = SDmaxC,
    				  N = NC,
    				  NbIter = NbIterC)

    
    print "====== Execution of SubCMedians version 1.1.0 (single threaded version) ======"
    print "====== Parameters ======\n"
    print "Random seed: "+str(seed)
    print "Maximal model size SDmax="+str(scm.SDmax)
    print "Sample size N="+str(scm.N)
    print "Number of iterations NbIter="+str(scm.NbIter)
    sys.stdout.write("====== Creating Subspace Clustering Model ======")
    time0 = time.time()
    
    scm.fit(df)
    if percorsoG != "":
        y = open(percorsoG,'r').readlines()
        y = [float(item) for item in y]
        evaluation_names = ["Acc.", "CE", "F1", "Entropy", "NbClust."]
        df_evaluation = pd.DataFrame()
        df_evaluation["clusters_found"] = list(scm.predict(df.values))
        df_evaluation["clusters_hidden"] = list(y)
        clusters_found = df_evaluation["clusters_found"]
        clusters_hidden = df_evaluation["clusters_hidden"]
        runtime = str(time.time()-time0)
        evaluation_temp =generate_evaluation(clusters_found, clusters_hidden)
        txt = get_evaluation_string(evaluation_temp, evaluation_names)+" Runtime="+runtime
        print txt
        
        fileClusters = open(percorsoS+"/cl.txt","w")
        for item in clusters_found:
            fileClusters.write("%s\n"% item)
        fileClusters.close()
        coordinate = scm._get_candidate_centers(percorsoD, percorsoS)
        centri = open(percorsoS+"/model_parameters.txt","w")
        centri.write("{}".format(coordinate))
        centri.close()
        general_info(righe=df.shape[0], colonne=df.shape[1], NbExpClust=NbExpClust, SDmax=SDmaxC, N=NC, NbIter=NbIterC, percorsoD=percorsoD, percorsoS=percorsoS, accuracy_local=evaluation_temp[0], ce_local=evaluation_temp[1], f1_local=evaluation_temp[2], entropy_local=evaluation_temp[3], nb_clusters=evaluation_temp[4])
        """if percorsoEL != "":
            fileEL = open(percorsoEL, 'r')
            fileELD = open(percorsoS+"/expList.csv", 'w')
            for line in fileEL:
                fileELD.write(line)
            fileEL.close()
            fileELD.close()"""
        if percorsoDN != "":
            fileDN = open(percorsoDN, 'r')
            fileDND = open(percorsoS+"/dataStandardization.csv", 'w')
            for line in fileDN:
                fileDND.write(line)
            fileDN.close()
            fileDND.close()
    else:
        evaluation_names = ["Acc.", "CE", "F1", "Entropy", "NbClust."]
        df_evaluation = pd.DataFrame()
        df_evaluation["clusters_found"] = list(scm.predict(df.values))
        #df_evaluation["clusters_hidden"] = list(y)
        clusters_found = df_evaluation["clusters_found"]
        #clusters_hidden = df_evaluation["clusters_hidden"]
        runtime = str(time.time()-time0)
        #evaluation_temp =subc.generate_evaluation(clusters_found, clusters_hidden)
        #txt = subc.get_evaluation_string(evaluation_temp, evaluation_names)+" 
        print "Runtime="+runtime
        #print txt
        print "Generating results files"
        fileClusters = open(percorsoS+"/cl.txt","w")
        for item in clusters_found:
            fileClusters.write("%s\n"% item)
        fileClusters.close()
        print "Clustering generated"
        coordinate = scm._get_candidate_centers(percorsoD, percorsoS)
        centri = open(percorsoS+"/model_parameters.txt","w")
        centri.write("{}".format(coordinate))
        centri.close()
        print "Model parameters generated"
        general_info(righe=df.shape[0], colonne=df.shape[1], NbExpClust=NbExpClust, SDmax=SDmaxC, N=NC, NbIter=NbIterC, percorsoD=percorsoD, percorsoS=percorsoS, accuracy_local="NA", ce_local="NA", f1_local="NA", entropy_local="NA", nb_clusters=np.unique(clusters_found).size)
        """if percorsoEL != "":
            fileEL = open(percorsoEL, 'r')
            fileELD = open(percorsoS+"/expList.csv", 'w')
            for line in fileEL:
                fileELD.write(line)
            fileEL.close()
            fileELD.close()"""
        if percorsoDN != "":
            fileDN = open(percorsoDN, 'r')
            fileDND = open(percorsoS+"/dataStandardization.csv", 'w')
            for line in fileDN:
                fileDND.write(line)
            fileDN.close()
            fileDND.close()