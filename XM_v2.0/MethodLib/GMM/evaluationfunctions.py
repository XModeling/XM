#!/usr/bin/python
import pandas as pd
import numpy as np
from sklearn.utils.linear_assignment_ import linear_assignment
NOT_ZERO_DIVISION_SECURITY = 0.0000000001

def convert_contingency_table_arff_to_true(contingency_table,
                                           true_data_set):
    new_contingency_table = pd.DataFrame(
        np.zeros((len(true_data_set.true_arff_dico.keys()), len(contingency_table.columns))),
        index=true_data_set.true_arff_dico.keys(), columns=contingency_table.columns)
    for k in true_data_set.df_true_dico.keys():
        for t in true_data_set.df_true_dico[k]:
            if k in contingency_table.index:
                new_contingency_table.loc[t, :] += contingency_table.loc[k, :]
    return new_contingency_table

def _validity_cluster_checking(found_clusters_effective,
                               threshold_cluster_validity=0.0):
    return found_clusters_effective >= threshold_cluster_validity


def compute_only_entropy(contingency_table,
                         valid_clusters):
    contingency_table = contingency_table.loc[:, valid_clusters]
    found_clusters_effective = contingency_table.sum(0)
    p_h_in_c = contingency_table * 1. / (found_clusters_effective + NOT_ZERO_DIVISION_SECURITY)
    log_p_h_in_c = np.log(p_h_in_c)
    pre_ec = -1. * p_h_in_c * log_p_h_in_c
    pre_ec = pre_ec.fillna(0)
    ec = pre_ec.sum(0)
    num = (ec * found_clusters_effective).sum()
    denum = found_clusters_effective.sum() * np.log(len(contingency_table.index))
    return 1. - num * 1. / denum


def entropy(cluster_hidden=[],
            cluster_found=[],
            threshold_cluster_validity=0.0):
    contingency_table = pd.crosstab(cluster_hidden, cluster_found)
    valid_clusters = _validity_cluster_checking(contingency_table.sum(0), threshold_cluster_validity)
    return compute_only_entropy(contingency_table, valid_clusters)


def compute_only_accuracy(contingency_table,
                          valid_clusters,
                          found_clusters_effective):
    best_matching_hidden_cluster = contingency_table == contingency_table.max(0)
    best_matching_hidden_cluster_weight = 1. / best_matching_hidden_cluster.sum(0)
    correctly_predicted_objects = contingency_table * best_matching_hidden_cluster * best_matching_hidden_cluster_weight
    correctly_predicted_objects *= valid_clusters
    return sum(correctly_predicted_objects.sum(0)) * 1. / sum(found_clusters_effective)


def accuracy(cluster_hidden=[],
             cluster_found=[],
             threshold_cluster_validity=0.0):
    contingency_table = pd.crosstab(cluster_hidden, cluster_found)
    found_clusters_effective = contingency_table.sum(0)
    valid_clusters = _validity_cluster_checking(found_clusters_effective, threshold_cluster_validity)
    return compute_only_accuracy(contingency_table, valid_clusters, found_clusters_effective)


def _mapped(contingency_table):
    mapped_clusters = (contingency_table.T * 1. / contingency_table.sum(1)).T
    return mapped_clusters == mapped_clusters.max(0)


def compute_only_recall(contingency_table,
                        valid_clusters,
                        mapped_clusters):
    num = mapped_clusters * contingency_table
    num = num.loc[:, valid_clusters]
    num = num.sum(1)
    denum = contingency_table.sum(1)
    return num * 1. / (denum + NOT_ZERO_DIVISION_SECURITY)


def recall(cluster_hidden=[],
           cluster_found=[],
           threshold_cluster_validity=0.0):
    contingency_table = pd.crosstab(cluster_hidden, cluster_found)
    mapped_clusters = _mapped(contingency_table)
    found_clusters_effective = contingency_table.sum(0)
    valid_clusters = _validity_cluster_checking(found_clusters_effective, threshold_cluster_validity)
    return compute_only_recall(contingency_table, valid_clusters, mapped_clusters)


def compute_only_precision(contingency_table,
                           valid_clusters,
                           mapped_clusters):
    num = mapped_clusters * contingency_table
    num = num.loc[:, valid_clusters]
    num = num.sum(1)
    denum = mapped_clusters * contingency_table.sum(0) * valid_clusters
    denum = denum.sum(1)
    return num * 1. / (denum + NOT_ZERO_DIVISION_SECURITY)


def precision(cluster_hidden=[],
              cluster_found=[],
              threshold_cluster_validity=0.0):
    contingency_table = pd.crosstab(cluster_hidden, cluster_found)
    mapped_clusters = _mapped(contingency_table)
    found_clusters_effective = contingency_table.sum(0)
    valid_clusters = _validity_cluster_checking(found_clusters_effective, threshold_cluster_validity)
    return compute_only_precision(contingency_table, valid_clusters, mapped_clusters)


def compute_only_f1(contingency_table,
                    valid_clusters,
                    mapped_clusters):
    num = mapped_clusters * contingency_table
    num = num.loc[:, valid_clusters]
    num = num.sum(1)
    denum_recall = contingency_table.sum(1)
    rec = num * 1. / (denum_recall + NOT_ZERO_DIVISION_SECURITY)
    denum_precision = mapped_clusters * contingency_table.sum(0) * valid_clusters
    denum_precision = denum_precision.sum(1)
    precis = num * 1. / (denum_precision + NOT_ZERO_DIVISION_SECURITY)
    denum = rec + precis
    num = 2 * rec * precis
    return sum(num * 1.0 / (denum + NOT_ZERO_DIVISION_SECURITY)) * 1. / (len(num) + NOT_ZERO_DIVISION_SECURITY)


def f1(cluster_hidden=[],
       cluster_found=[],
       threshold_cluster_validity=0.0):
    contingency_table = pd.crosstab(cluster_hidden, cluster_found)
    mapped_clusters = _mapped(contingency_table)
    found_clusters_effective = contingency_table.sum(0)
    valid_clusters = _validity_cluster_checking(found_clusters_effective, threshold_cluster_validity)
    return compute_only_f1(contingency_table, valid_clusters, mapped_clusters)


def compute_only_ce(contingency_table,
                    valid_clusters):
    valid_contingency_table = contingency_table.loc[:, valid_clusters]
    best_hidden_found_couples = linear_assignment(-valid_contingency_table)
    ans = [valid_contingency_table.iloc[couple[0], couple[1]] for couple in best_hidden_found_couples]
    return sum(ans) * 1. / sum(contingency_table.sum(0))


def ce(contingency_table="", cluster_hidden=[],
       cluster_found=[],
       threshold_cluster_validity=0.0):
    if contingency_table == "":
        contingency_table = pd.crosstab(cluster_hidden, cluster_found)
    found_clusters_effective = contingency_table.sum(0)
    valid_clusters = _validity_cluster_checking(found_clusters_effective, threshold_cluster_validity)
    return compute_only_ce(contingency_table, valid_clusters)


def _pairwise_df_subspaces_intersection(points_SS_1,
                                        points_SS_2):
    ans = [[len(points_SS_1[i].intersection(points_SS_2[j])) for j in points_SS_2] for i in points_SS_1]
    return pd.DataFrame(ans, columns=points_SS_2.keys(), index=points_SS_1.keys())


def _pairwise_df_subspaces_union(points_SS_1,
                                 points_SS_2):
    ans = [[len(points_SS_1[i].union(points_SS_2[j])) for j in points_SS_2] for i in points_SS_1]
    return pd.DataFrame(ans, columns=points_SS_2.keys(), index=points_SS_1.keys())


def _sub_objects_contingency_table(objects_contingency_table,
                                   subspaces_contingency_table):
    for i in list(objects_contingency_table.columns):
        if i not in subspaces_contingency_table.columns:
            return pd.DataFrame()
    subspaces_contingency_table = subspaces_contingency_table.loc[:, list(objects_contingency_table.columns)]
    return objects_contingency_table * subspaces_contingency_table

def rnia(cluster_hidden=[],
		 cluster_found=[],
		 SS_hidden=[],
		 SS_found=[],
         threshold_cluster_validity=0.0):
    contingency_table = pd.crosstab(cluster_hidden, cluster_found)
    valid_clusters = _validity_cluster_checking(contingency_table.sum(0), threshold_cluster_validity)
    i = _pairwise_df_subspaces_intersection(SS_hidden, SS_found)
    u = _pairwise_df_subspaces_union(SS_hidden, SS_found)
    i = _sub_objects_contingency_table(contingency_table, i)
    u = _sub_objects_contingency_table(contingency_table, u)
    return compute_only_rnia(i,u,valid_clusters)

def compute_only_rnia(sub_objects_intersection,
                      sub_objects_union,
                      valid_clusters):
    sub_objects_intersection = sub_objects_intersection.loc[:, valid_clusters]
    sub_objects_union = sub_objects_union.loc[:, valid_clusters]
    i = sub_objects_intersection.sum(0).sum()
    u = sub_objects_union.sum(0).sum()
    return i * 1. / (u + NOT_ZERO_DIVISION_SECURITY)

"""
def ssce(cluster_hidden=[],
		 cluster_found=[],
		 SS_hidden=[],
		 SS_found=[],
         threshold_cluster_validity=0.0):
    contingency_table = pd.crosstab(cluster_hidden, cluster_found)
    valid_clusters = _validity_cluster_checking(contingency_table.sum(0), threshold_cluster_validity)
    i = _pairwise_df_subspaces_intersection(SS_hidden, SS_found)
    u = _pairwise_df_subspaces_union(SS_hidden, SS_found)
    i = _sub_objects_contingency_table(contingency_table, i)
    u = _sub_objects_contingency_table(contingency_table, u)
    return compute_only_ssce(i,u,valid_clusters)
"""
def ssce(cluster_hidden=[],
         cluster_found=[],
         SS_hidden=[],
         SS_found=[],
         threshold_cluster_validity=0.0):
    i = _sub_objects_intersection_contingency(cluster_hidden,cluster_found, SS_hidden, SS_found).fillna(0) 
    u = _sub_objects_union_contingency(cluster_hidden,cluster_found, SS_hidden, SS_found).fillna(0) 
    best_hidden_found_couples = linear_assignment(-i)
    return sum([i.iloc[couple[0], couple[1]] for couple in best_hidden_found_couples]) * 1. / (u.sum(0).sum() + NOT_ZERO_DIVISION_SECURITY)  

def _sub_objects_intersection_contingency(cluster_hidden,cluster_found, SS_hidden, SS_found):
    hidden_clusters = np.unique(cluster_hidden)
    found_clusters = np.unique(cluster_found)
    i = pd.DataFrame(np.zeros((hidden_clusters.size, found_clusters.size)), index=hidden_clusters, columns=found_clusters)
    intersection = np.logical_and(SS_hidden, SS_found).sum(1)
    for idx in xrange(len(cluster_hidden)):
        hc = cluster_hidden[idx]
        fc = cluster_found[idx]
        i[fc][hc] = intersection[idx]
    return i

def _sub_objects_union_contingency(cluster_hidden,cluster_found, SS_hidden, SS_found):
    hidden_clusters = np.unique(cluster_hidden)
    found_clusters = np.unique(cluster_found)
    u = pd.DataFrame(np.zeros((hidden_clusters.size, found_clusters.size)), index=hidden_clusters, columns=found_clusters)
    union = np.logical_or(SS_hidden, SS_found).sum(1)
    for idx in xrange(len(cluster_hidden)):
        hc = cluster_hidden[idx]
        fc = cluster_found[idx]
        u[fc][hc] = union[idx]
    return u 

def compute_only_ssce(sub_objects_intersection,
                      sub_objects_union,
                      valid_clusters):
    sub_objects_intersection = sub_objects_intersection.loc[:, valid_clusters].fillna(0) 
    sub_objects_union = sub_objects_union.loc[:, valid_clusters].fillna(0) 
    best_hidden_found_couples = linear_assignment(-sub_objects_intersection)
    return sum([sub_objects_intersection.iloc[couple[0], couple[1]] for couple in best_hidden_found_couples]) * 1. / (
        sub_objects_union.sum(0).sum() + NOT_ZERO_DIVISION_SECURITY)

def average_dim_not_noise_clusters(subspace_phenotype,clusters):
    avg_dim = 0
    for c in clusters:
        if c in subspace_phenotype.keys():
            avg_dim += len(subspace_phenotype[c])
    return avg_dim *1.0/len(clusters)

def functional_evaluation(subspace_phenotype, cluster_hidden, cluster_found, true_data_set="",
                          threshold_cluster_validity=0.0):
    if not isinstance(true_data_set, str):
        not_noise = [ch not in true_data_set.hidden_noise_clus for ch in cluster_hidden]
        cluster_hidden = cluster_hidden[not_noise]
        cluster_found = cluster_found[not_noise]
    contingency_table = pd.crosstab(cluster_hidden, cluster_found)
    found_clusters_effective = contingency_table.sum(0)
    valid_clusters = _validity_cluster_checking(found_clusters_effective, threshold_cluster_validity)
    if not isinstance(true_data_set, str):
        contingency_table = convert_contingency_table_arff_to_true(contingency_table, true_data_set)
        i = _pairwise_df_subspaces_intersection(true_data_set.clusters_subspaces, subspace_phenotype)
        u = _pairwise_df_subspaces_union(true_data_set.clusters_subspaces, subspace_phenotype)
        i = _sub_objects_contingency_table(contingency_table, i)
        u = _sub_objects_contingency_table(contingency_table, u)
        mapped_clusters = _mapped(contingency_table)
        clusters_not_noise = contingency_table.columns
        evaluation = [compute_only_entropy(contingency_table, valid_clusters),
                      compute_only_accuracy(contingency_table, valid_clusters, found_clusters_effective),
                      compute_only_f1(contingency_table, valid_clusters, mapped_clusters),
                      compute_only_ce(contingency_table, valid_clusters),
                      compute_only_rnia(i, u, valid_clusters),
                      compute_only_ssce(i, u, valid_clusters),
                      len(clusters_not_noise),
                      average_dim_not_noise_clusters(subspace_phenotype,clusters_not_noise)]
    else:
        mapped_clusters = _mapped(contingency_table)
        clusters_not_noise = contingency_table.columns
        evaluation = [compute_only_entropy(contingency_table, valid_clusters),
                      compute_only_accuracy(contingency_table, valid_clusters, found_clusters_effective),
                      compute_only_f1(contingency_table, valid_clusters, mapped_clusters),
                      compute_only_ce(contingency_table, valid_clusters),
                      None,
                      None,
                      compute_coverage(found_clusters_effective, valid_clusters),
                      len(clusters_not_noise),
                      average_dim_not_noise_clusters(subspace_phenotype,clusters_not_noise)]
    return evaluation
