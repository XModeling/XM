from Definitions.definitions import STD_PRECISION
from scipy import stats
import pickle
import random
import pylab
import pandas as pd
import numpy as np


class DataSetFull:
    def __init__(self, file_name,
                 hidden_cluster=[],
                 found_cluster=[],
                 useless=[],
                 index=None,
                 header=None,
                 comments="#",
                 sep=","):
        self.useless = useless
        self.hidden_cluster = hidden_cluster
        self.found_cluster = found_cluster
        self.df = pd.read_csv(file_name, header=header, index_col=index, sep=sep,comment = comments)
        self.df.columns = [str(x) for x in self.df.columns]
        self.features = [e for e in list(self.df.columns.values) if
                         e not in self.hidden_cluster and e not in self.found_cluster and e not in self.useless]
        self.__cast()
        self.conversion_dico = {}
        self.data = []
        if self.hidden_cluster:
            self.hidden_cluster_membership = list(self.df[self.hidden_cluster[0]])[:]
        if self.found_cluster:
            self.convert_cluster_membership_to_numerical(self.found_cluster)
        if self.hidden_cluster:
            self.convert_cluster_membership_to_numerical(self.hidden_cluster)

    def __drop_useless(self):
        for feature in self.useless:
            self.df = self.df.drop(feature, 1)

    def __cast(self):
        for feature in self.features:
            self.df[feature] = self.df[feature].astype(float)

    def convert_cluster_membership_to_numerical(self, cluster_col):
        self.conversion_cluster_membership_dico(cluster_col)
        for i in self.df.index:
            self.df.loc[i, cluster_col[0]] = self.conversion_dico[cluster_col[0]][self.df.loc[i, cluster_col[0]]]
        self.df[cluster_col[0]] = self.df[cluster_col[0]].astype(int)

    def conversion_cluster_membership_dico(self, cluster_col):
        df_col = self.df[cluster_col[0]]
        self.conversion_dico[cluster_col[0]] = {k: i for i, k in enumerate(df_col.unique())}

    def standardize_table(self):
        self.df[self.features] = stats.zscore(self.df[self.features])
        self.df[self.features] = self.df[self.features].fillna(0)

    def center_table(self):
        self.df[self.features] = pylab.demean(self.df[self.features], axis=1)

    def normalize_table_by_std(self):
        self.df[self.features] = self.df[self.features] / np.std(self.df[self.features], axis=0)
        self.df[self.features] = self.df[self.features].fillna(0)

    def multiply_table_by_precision_and_convert_to_int(self, precision=STD_PRECISION):
        vecfunc = np.vectorize(lambda x: int(x * precision))
        self.df[self.features] = vecfunc(self.df[self.features])

    def shift_table(self, shift):
        self.df[self.features] = self.df[self.features].values + shift

    def logscale_table(self):
        table = self.df[self.features]
        self.df[self.features] = np.log(table * (table > 0) + (table <= 0)) - np.log(
            -table * (table < 0) + (table >= 0))

    def table_to_data(self, features=""):
        if features == "":
            features = self.features
        self.data = []
        i = 0
        while i < len(self.df):
            self.data.append([])
            if not self.hidden_cluster:
                self.data[i].append(-1)
            else:
                self.data[i].append(self.df.loc[self.df.index[i], self.hidden_cluster[0]])
            if not self.found_cluster:
                self.data[i].append(-1)
            else:
                self.data[i].append(self.df.loc[self.df.index[i], self.found_cluster[0]])
            self.data[i] += [[j, e] for j, e in enumerate(self.df.loc[self.df.index[i], features])]
            i += 1
        return self.data

    def table_to_sub_objects_stream(self):
        stream = []
        i = 0
        while i < len(self.df):
            for j, e in enumerate(self.df.loc[i, self.features]):
                stream.append([i, j, e])
            i += 1
        return stream

    def set_column_values(self, values, column):
        for i, e in enumerate(values):
            self.df[column].values[i] = e

    def shuffle(self, shuffled_index=[]):
        if not shuffled_index:
            self.shuffled_index = range(len(self.df.index))
            random.shuffle(self.shuffled_index)
        else:
            self.shuffled_index = shuffled_index[:]
        new_index = [list(self.df.index)[i] for i in self.shuffled_index]
        self.df = self.df.ix[new_index]
        self.df = self.df.reset_index(drop=True)
        if len(self.data) == len(self.shuffled_index):
            self.data = [self.data[i] for i in self.shuffled_index]

    def reorder_dataframe(self, dataframe):
        dataframe.index = self.shuffled_index
        return dataframe.sort()

    def save(self,file_name,conversion_dico_file_name = "CONVERSION_DICT.PICKLE",
             shuffled_index_name="SHUFFLED_INDEXES_ORDER.PICKLE",
             hidden_cluster_memebership_name="HIDDEN_CLUSTER_MEMBERSHIPS.PICKLE"):
        self.df.to_csv(file_name, sep=' ', header=False, index=False, mode='w')
        pickle.dump(self.conversion_dico,open(conversion_dico_file_name,"w"))
        pickle.dump(self.shuffled_index,open(shuffled_index_name,"w"))
        pickle.dump(self.hidden_cluster_membership,open(hidden_cluster_memebership_name,"w"))


def easy_full_dataset_load(load_params,save_params,keep_double):
    data_set = DataSetFull(**load_params)
    data_set.standardize_table()
    if not keep_double:
	    data_set.multiply_table_by_precision_and_convert_to_int()
    data_set.shuffle()
    data_set.save(**save_params)