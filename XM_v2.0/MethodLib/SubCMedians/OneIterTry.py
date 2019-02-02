#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 15:00:47 2018

@author: francesco
"""

import subc

percorsoD = "/home/francesco/Tirocinio/XM_v1.3.5/DATASETS/Pearsons/dataset_pearson.csv"
percorsoS = "/home/francesco/Tirocinio/XM_v1.3.5/RESULTS/DEMO/"
percorsoG = "/home/francesco/Tirocinio/XM_v1.3.5/DATASETS/Pearsons/GT.txt"
percorsoDN = ""
seed = 0
subc.genera_cluster(0, 50, 10, 1000, percorsoD, percorsoS, "", percorsoDN, seed)
