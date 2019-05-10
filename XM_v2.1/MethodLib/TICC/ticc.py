import pandas as pd
import numpy as np
from TICC_solver import TICC
from evaluationfunctions import accuracy,ce,entropy,f1,rnia
import time
import sys
from scipy import stats
import csv
import re
import os
import SM2
import sklearn.metrics as sk
from sklearn.manifold import TSNE
import random
from collections import defaultdict

#seed=1
#np.random.seed(seed)
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

def general_info(righe=0, colonne=0, clust=0, window=0, p_lambda=0, beta=0, bic=0, aic=0, ll=0, percorsoD="/", percorsoS="/", accuracy_local="Nan", ce_local="Nan", f1_local="Nan", entropy_local="Nan", purity_local="Nan", nb_clusters_found=0):
    
    df, latitude, longitude, experiment = get_dataset(percorsoD)
    """
    if int(window) > 1:
        for i in range(int(window)-1):
            df.drop(i, inplace=True)
    """
    gi = pd.DataFrame()
    varU = list(df)
    gi["Parameter"] = [ "Dataset_Path","Results_Path","Number_of_columns","Number_of_rows","Method","N.Cluster","Window Size","Lambda","Beta","Accuracy","CE","F1","Entropy","Purity","NbClusterFound","Note"]
    gi["Values"] = [percorsoD, percorsoS, colonne, righe, "TICC", clust, window, p_lambda, beta, accuracy_local, ce_local, f1_local, entropy_local, purity_local, nb_clusters_found,"-"]
    gi.to_csv(path_or_buf=percorsoS+"/generalInfo.csv", columns=["Parameter","Values"], index=False)
    fileG = open(percorsoS+"/generalInfo.csv", 'a')
    fileG.write("Variables,")
    for var in varU:
        fileG.write(var+",")
    fileG.seek(-1, os.SEEK_END)
    fileG.truncate()
    fileG.write("\n")
    fileG.write("BIC,{}\n".format(bic))
    fileG.truncate()
    fileG.write("AIC,{}\n".format(aic)) 
    fileG.truncate()
    fileG.write("LL,{}\n".format(ll))
    #print "[XM]> Computing SILHOUETTE (subspaces)"
    #clSS = silhouette_sub(percorsoD, percorsoS)
    print "[XM]> Computing SILHOUETTE (dataset)"
    clSN = silhouette(percorsoD, percorsoS)
    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    n_points = [list(clusternorm).count(c) for c in set(clusternorm)]
    sil_tot = sum([item*n_points[i] for i,item in enumerate(clSN)])/sum(n_points)
    fileG.write("Silhouette total,{}\n".format(sil_tot))
    #vU = pd.read_table(percorsoS+"/model_parameters.txt", delim_whitespace=True)
    #righeU, colonneU = vU.shape
    use = [len(varU) for i in range(len(clustergiusti))]
    """
    for i in range(0, righeU):
        riga = vU.iloc[i,:]
        use.append(np.count_nonzero(~np.isnan(riga)))
    """
    i = 0
    for clS in clSN:
        fileG.write("{0:.3f}".format(clS)+",{}".format(n_points[i])+",{}\n".format(use[i]))
        i += 1
    fileG.seek(-1, os.SEEK_END)
    fileG.truncate()
    fileG.close()
    print "[XM]> General Info generated"
    
def tsne(percorsoD, percorsoS, samples):
    
    print "[XM]> Computing TSNE results"
    df, latitude, longitude, experiments = get_dataset(percorsoD)
    #labelvar=list(df)
    nSelObs=int(samples) # 4000
    rndSel=random.sample(range(df.shape[0]), nSelObs) # Random selection
    data1=df.iloc[rndSel,:]
    
    clusternorm, clustergiusti, cl = get_cl(percorsoS)
    cl = pd.DataFrame(cl)
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
    data_embedded_TSNE = TSNE(n_components=2,init='pca', verbose=1,random_state=0).fit_transform(data1)
    data_embedded_TSNE.shape
    det = pd.DataFrame(data_embedded_TSNE)
    det["clusters"] = clusternorm
    det.to_csv(path_or_buf=percorsoS+"/tsne.csv", index=False)
    print "[XM]> TSNE results generated"
    
def generate_evaluation(clusters_found, clusters_hidden):
    accuracy_local = accuracy(cluster_hidden=clusters_hidden,cluster_found=clusters_found)
    ce_local = ce(cluster_hidden=clusters_hidden,cluster_found=clusters_found)
    #rnia_local = rnia(cluster_hidden=clusters_hidden, cluster_found=clusters_found)
    f1_local = f1(cluster_hidden=clusters_hidden, cluster_found=clusters_found)
    entropy_local = entropy(cluster_hidden=clusters_hidden, cluster_found=clusters_found)
    purity_local = purity(clusters_found, clusters_hidden)
    nb_clusters = np.unique(clusters_found).size
    return [accuracy_local, ce_local, f1_local, entropy_local, purity_local, nb_clusters]

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

def genera_cluster(cluster=0, window=0, p_lambda=0, beta=0, percorsoD="/", percorsoS="/", percorsoG="", percorsoDN="", seed=102):
    
    percorsoS = percorsoS+"/TICC"
    if not os.path.exists(percorsoS):
        os.makedirs(percorsoS)
    
    # Read the dataset
    base_name = percorsoD
    file_name = base_name
    df, latitude, longitude, experiment = get_dataset(file_name)
    df = df.astype(float)

    ticc = TICC(window_size=int(window), number_of_clusters=int(cluster), lambda_parameter=float(p_lambda),
                 beta=int(beta), seed=seed)

    print "[XM]> ========= Generating TICC clustering model ==========="
    
    cluster_assignment, cluster_MRFs, bic, aic, ll = ticc.fit(input_file=percorsoD)
    cluster_assignment = [int(item) for item in cluster_assignment]
    surplus = []
    if int(window) > 1:
        for i in range(int(window)-1):
            surplus.append(cluster_assignment[0])
    cluster_assignment = surplus+cluster_assignment
    if percorsoG != "":
        y = open(percorsoG,'r').readlines()
        y = [float(item) for item in y]
        evaluation_names = ["Acc.", "CE", "F1", "Entropy", "Purity", "NbClust."]
        df_evaluation = pd.DataFrame()
        df_evaluation["clusters_found"] = list(cluster_assignment)
        df_evaluation["clusters_hidden"] = list(y)
        clusters_found = df_evaluation["clusters_found"]
        clusters_hidden = df_evaluation["clusters_hidden"]
        evaluation_temp = generate_evaluation(clusters_found, clusters_hidden)
        print "[XM]> Generating results files"
        fileClusters = open(percorsoS+"/cl.txt","w")
        for item in clusters_found:
            fileClusters.write("%s\n"% item)
        fileClusters.close()
        print "[XM]> Clustering generated"
        coordinate = cluster_MRFs.values()
        #mrf = []
        """
        for mat in coordinate:
            diag = np.diagonal(mat)
            mrf.append(diag)
        mrf = pd.DataFrame(mrf).to_string()
        """
        for cl, mat in enumerate(coordinate):
            centri = open(percorsoS+"/model_parameters"+str(cl)+".txt","w")
            mat = pd.DataFrame(mat).to_string()
            centri.write("{}".format(mat))
            centri.close()
            
        print "[XM]> Model parameters generated"
        general_info(righe=df.shape[0], colonne=df.shape[1], clust=cluster, window=window, p_lambda=p_lambda, beta=beta, bic=bic, aic=aic, ll=ll, percorsoD=percorsoD, percorsoS=percorsoS, accuracy_local=evaluation_temp[0], ce_local=evaluation_temp[1], f1_local=evaluation_temp[2], entropy_local=evaluation_temp[3], purity_local=evaluation_temp[4], nb_clusters_found=evaluation_temp[5])
        if percorsoDN != "":
            fileDN = open(percorsoDN, 'r')
            fileDND = open(percorsoS+"/dataStandardization.csv", 'w')
            for line in fileDN:
                fileDND.write(line)
            fileDN.close()
            fileDND.close()
    else:
        #evaluation_names = ["Acc.", "CE", "F1", "Entropy", "NbClust."]
        df_evaluation = pd.DataFrame()
        df_evaluation["clusters_found"] = list(cluster_assignment)
        #df_evaluation["clusters_hidden"] = list(y)
        clusters_found = df_evaluation["clusters_found"]
        #clusters_hidden = df_evaluation["clusters_hidden"]
        #evaluation_temp =subc.generate_evaluation(clusters_found, clusters_hidden)
        #txt = subc.get_evaluation_string(evaluation_temp, evaluation_names)+" 
        print "[XM]> Generating results files"
        fileClusters = open(percorsoS+"/cl.txt","w")
        for item in clusters_found:
            fileClusters.write("%s\n"% item)
        fileClusters.close()
        print "[XM]> Clustering generated"
        coordinate = cluster_MRFs.values()
        #mrf = []
        """
        for mat in coordinate:
            diag = np.diagonal(mat)
            mrf.append(diag)
        mrf = pd.DataFrame(mrf).to_string()
        centri = open(percorsoS+"/model_parameters.txt","w")
        centri.write("{}".format(mrf))
        centri.close()
        """
        for cl, mat in enumerate(coordinate):
            centri = open(percorsoS+"/model_parameters"+str(cl)+".txt","w")
            mat = pd.DataFrame(mat).to_string()
            centri.write("{}".format(mat))
            centri.close()
        print "[XM]> Model parameters generated"
        general_info(righe=df.shape[0], colonne=df.shape[1], clust=cluster, window=window, p_lambda=p_lambda, beta=beta, bic=bic, aic=aic, ll=ll, percorsoD=percorsoD, percorsoS=percorsoS, accuracy_local="NA", ce_local="NA", f1_local="NA", entropy_local="NA", purity_local="NA", nb_clusters_found=np.unique(clusters_found).size)
        if percorsoDN != "":
            fileDN = open(percorsoDN, 'r')
            fileDND = open(percorsoS+"/dataStandardization.csv", 'w')
            for line in fileDN:
                fileDND.write(line)
            fileDN.close()
            fileDND.close()
