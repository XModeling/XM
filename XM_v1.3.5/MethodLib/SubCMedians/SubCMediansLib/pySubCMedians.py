#!/usr/bin/python
import C.SubCMediansWrapper_c as SubCMediansWrapper_c
from Definitions.definitions import STD_SDmax,STD_D,STD_N,STD_THRESHOLD_CLUSTER_VALIDITY,STD_SEED,STD_OPT_DEL,STD_OPT_INS,STD_FIFO,STD_TRAIN_WITH_LATEST,STD_LAZY_HILL_CLIMBING, STD_LAMBDA,STD_ETA, POINTDESCRIPTORS, NBFEATURES, POINTWEIGHT, DIMID, POINTINDEX, STD_NbIter, POINTCLASSID, DIMPOS
from pandas import DataFrame
from numpy import logical_not, isnan, array, append, ndarray, generic
from EvaluationUtil.evaluationfunctions import functional_evaluation
from timeit import default_timer as timer
import numpy as np
import sys
import pandas as pd
from scipy import special
import funct as f

class SubCMedians_customizable:
    def __init__(self,
                 SDmax=STD_SDmax,
                 D=STD_D,
                 N=STD_N,
                 NbIter = STD_NbIter,
                 threshold_cluster_validity=STD_THRESHOLD_CLUSTER_VALIDITY,
                 seed=STD_SEED,
                 option_deletion=STD_OPT_DEL,
                 option_insertion=STD_OPT_INS,
                 option_FIFO=STD_FIFO,
                 option_train_with_latest=STD_TRAIN_WITH_LATEST,
                 option_lazy_hill_climbing = STD_LAZY_HILL_CLIMBING, 
                 population_size=STD_LAMBDA,
                 nb_generations_generation_update=STD_ETA):
        """
        Creates a SubCMedians customizable object. This version has more options than the one presented in the paper, we suggest to use the SubCMedians object instead.
        """
        self.SDmax = SDmax
        self.D = D
        self.N = N
        self.NbIter = NbIter
        self.threshold_cluster_validity = threshold_cluster_validity
        self.option_deletion = option_deletion
        self.option_insertion = option_insertion
        self.option_FIFO = option_FIFO
        self.option_train_with_latest = option_train_with_latest
        self.seed = seed
        self.population_size = population_size
        self.nb_generations_generation_update = nb_generations_generation_update
        self.option_lazy_hill_climbing = option_lazy_hill_climbing
        self._p_subcmedians_c = SubCMediansWrapper_c.generate_SubCMediansclust(SDmax,
                                                                     D,
                                                                     N,
                                                                     threshold_cluster_validity,
                                                                     seed,
                                                                     option_deletion,
                                                                     option_insertion,
                                                                     option_FIFO,
                                                                     option_train_with_latest,
                                                                     option_lazy_hill_climbing,
                                                                     population_size,
                                                                     nb_generations_generation_update)
        self._model_getter = []
        self._distances_to_cluster_getter = []
        self._lengths = []
        self._features = []
        self._object_class_cluster = []
        self._cluster_getter = []
        self._aggregatedstats = {}
        self._prng = SubCMediansWrapper_c.generate_prng(self.seed)
        self._stream = SubCMediansWrapper_c.generate_array_SubCMedians_point(self._prng, N, D)
        self._data_object = SubCMediansWrapper_c.generate_SubCMedians_point(self._prng, D)
        self._cluster_object = SubCMediansWrapper_c.generate_SubCMedians_point(self._prng, SDmax)
        self.time_start = timer()
        self._parameters = ["SDmax",
                            "D",
                            "N",
                            "M",
                            "option_deletion",
                            "option_insertion",
                            "option_FIFO",
                            "option_train_with_latest",
                            "seed",
                            "option_lazy_hill_climbing",
                            "population_size",
                            "nb_generations_generation_update"]
        self.generation = 0

    def _reallocate_memory(self):
        """
        Create Python lists to allocate memory once at the begining. These objects will be subsequently modified by the C library.
        """
        self._model_getter = [[0.0 for _ in xrange(POINTDESCRIPTORS)] + [[0.0, 0.0, 0.0] for _ in xrange(self.SDmax)] for _ in xrange(self.SDmax)]
        self._cluster_getter = [0.0 for _ in xrange(POINTDESCRIPTORS)]+[[0.0, 0.0, 0.0] for _ in xrange(self.SDmax)] 
        self._distances_to_cluster_getter = [0.0 for _ in xrange(self.D)]
        self._lengths = [0.0 for _ in xrange(self.SDmax + 1)]
        self._features = [0.0 for _ in xrange(NBFEATURES)]
        self._object_class_cluster = [0, 0]

    def _check_consistency_C_params_Py_params(self):
        """
        Check the consistency of the C parameters with respect to Python object parameters
        """
        c_parameters = SubCMediansWrapper_c.get_parameters(self._p_subcmedians_c)
        for i, param in enumerate(self._parameters):
            if getattr(self, param) != c_parameters[i]:
                raise RuntimeError('C capsule parameters and Python parameters are different '
                                   '%s %s != %s' %
                                   (param, str(getattr(self, param)), c_parameters[i]))

    def _check_X_matrix_validity(self,X):
        """
        Check the validity of a matrix before sending it to the SubCMedians algorithm
        """
        if isinstance(X,list) :
            len_row = len(X[0])
            for x in X:
                if len_row != len(x):
                    raise ValueError('Invalid parameter %s for function %s.'
                                     'Each row should have the same length'
                                     'Check the input table X'%(X,self._check_X_matrix_validity))
            return X
        if isinstance(X,DataFrame):
            return X.values
        if isinstance(X,(ndarray, generic)):
            return X
        raise ValueError('Invalid parameter %s for function %s.'
                         'Invalid type'
                         'Check the input table X'%(X,self._check_X_matrix_validity))

    def _send_array(self, x, y=None):
        """
        Send an data object represented as a numpy array or a list to the C library
        """
        scm_py_list = [0 for _ in xrange(POINTDESCRIPTORS)]
        for i, dim_pos in enumerate(x):
            if not isnan(dim_pos):
                scm_py_list.append([i, 1, float(dim_pos)])
        if y is not None:
            scm_py_list[POINTCLASSID] = int(y)
        scm_py_list[POINTWEIGHT] = len(scm_py_list) - POINTDESCRIPTORS
        SubCMediansWrapper_c.py2C_convert_SubCMedianspoint(scm_py_list, self._data_object)


    def _transform_array(self, x):
        """
        Apply the transform function to objects x in order to compute the distance to each candidate center in the model.
        """
        self._send_array(x)
        cluster, distance = SubCMediansWrapper_c.clusterize_SubCMedianspoint_with_model(self._p_subcmedians_c,
                                                                                        self._data_object)
        SubCMediansWrapper_c.get_distances_to_core_point(cluster,
                                                         self._p_subcmedians_c,
                                                         self._data_object,
                                                         self._distances_to_cluster_getter)
        return array(self._distances_to_cluster_getter)

    def _train_on_current_training_set(self,iterations):
        """
        Train the SubCMedians algorithm without updating the dataset sample
        """
        for i in xrange(iterations):
            SubCMediansWrapper_c.train_on_current_D(self._p_subcmedians_c)

    def _print_me(self):
        """
        Print description regarding the current SubCMedians model
        """
        SubCMediansWrapper_c.print_SubCMediansClust(self._p_subcmedians_c)


    def _get_subcmedians_model(self):
        """
        Get SubCMedians current model
        """
        SubCMediansWrapper_c.get_SubCMediansclust_model(self._model_getter, self._lengths, self._p_subcmedians_c)
        local_model = [self._model_getter[i][0:self._lengths[i + 1]] for i in xrange(self._lengths[0])]
        return local_model

    def _get_model_features(self):
        """
        Compute and get the most important features of the current model
        """
        SubCMediansWrapper_c.get_features(self._features, self._p_subcmedians_c)
        return self._features+[self.generation]

    def _get_dimensionality(self,model=None):
        """
        Compute the dimensionality of the current model
        """
        if model is None:
            model = self._get_subcmedians_model()
        max_dim = 0
        for cluster in model:
            for i in xrange(POINTDESCRIPTORS , len(cluster)):
                max_dim = max(max_dim, cluster[i][DIMID])
        return max_dim

    def _get_subspaces_candidate_centers(self, model=None):
        """
        Return the subspace associated to each candidate center in the model
        """
        if model is None:
            model = self._get_subcmedians_model()
        self.subspaces = {model[point_index][POINTINDEX]: set([model[point_index][i][DIMID] for i in range(POINTDESCRIPTORS, len(model[point_index]))]) for point_index in xrange(len(model))}
        return self.subspaces
      
    def _get_class_clusters_current_data_sample(self):
        """
        Get the class / cluster membership of te current data sample
        """
        class_cluster_df = DataFrame(columns=["class", "cluster"])
        size_D = SubCMediansWrapper_c.get_data_window_size(self._p_subcmedians_c)
        for i in xrange(size_D):
            SubCMediansWrapper_c.get_D_point_class_cluster(i, self._p_subcmedians_c, self._object_class_cluster)
            class_cluster_df.loc[i] = self._object_class_cluster
        return class_cluster_df

    def _get_candidate_centers(self, percorsoD, percorsoS):
        """
        Return the candidate center locations
        """
        value_for_empty_dimensions=np.nan
        model = self._get_subcmedians_model()
        D = self._get_dimensionality(model = model)
        clusters = {model[point_index][POINTINDEX]:[value_for_empty_dimensions for _ in xrange(D+1)] for point_index in xrange(len(model))}
        for point_index in xrange(len(model)):
            for i in xrange(POINTDESCRIPTORS, len(model[point_index])):
                clusters[model[point_index][POINTINDEX]][model[point_index][i][DIMID]] = model[point_index][i][DIMPOS]
        """
        Elimino i centroidi in eccesso
        """
        clu = open(percorsoS+'/cl.txt','r').readlines()
        clu = [float(item) for item in clu]
        cluset = set(clu)
        df = pd.DataFrame(clusters).T
        indexes = df.index
        indexes = [float(item) for item in indexes]
        j = len(indexes)-1
        if len(indexes) != len(cluset):
            for i in range(0, len(indexes)):
                if indexes[j] not in cluset:
                    df = df.drop(df.index[j])
                j = j-1
        #df = df.astype(float)
        #valori = df.values
        """
        Aggiusto i valori delle colonne/DENORMALIZZO
        """
        """
        dfN = pd.read_table(percorsoD, comment = "#")
        dfN.drop(dfN.columns[10],axis=1, inplace=True) #longitude
        dfN.drop(dfN.columns[9],axis=1, inplace=True) #latitude
        dfN.drop(dfN.columns[1],axis=1, inplace=True) #seconds
        dfN.drop(dfN.columns[0],axis=1, inplace=True) #data
        dfN = dfN.astype(float)
        dfN = dfN.values
        xmax, xmin= dfN.max(), dfN.min()
        valori = ((xmax-xmin)*(valori-1)/(2-1))+xmin 
        """
        """
        cols = list(df)
        for col in cols:
            df[col] = (df[col]-2)
        """
        """
        Fill delle colonne non presenti
        """
        dfV, latitude, longitude = f.get_dataset(percorsoD)
        colonneTot = dfV.shape[1]
        colonne = df.shape[1]
        if colonne < colonneTot:
            for i in range(colonne+1, colonneTot+1):
                print i
                df[str(i+1)] = ["NaN" for i in range(0, df.shape[0])]
        #valori = pd.DataFrame(valori)
        return df.to_string()

    def _filter_noise_objects(self, class_cluster, noise_classes):
        """
        Filters out the objects that belong to the noise classes
        """
        return class_cluster.loc[logical_not(class_cluster['class'].isin(noise_classes))]


    def _cluster_data_object(self,x, y=None):
        """
        Sends a data objected encoded as a numpy array or a list and cluster it
        """
        self._send_array(x,y)
        cluster, distance = SubCMediansWrapper_c.clusterize_SubCMedianspoint_with_model(self._p_subcmedians_c, self._data_object)
        return [int(y),cluster],distance

    def _cluster_data_frame(self,X,y=None):
        """
        Dataset is encoded as a matrix, each row representing a data objet. Each row is sent to SubMorphoStream and clustered.
        """
        if X is None:
            return None
        X_ = self._check_X_matrix_validity(X)
        class_cluster_df = DataFrame(columns=["class", "cluster"])
        distance = 0
        if len(X_.shape) == 1:
            class_cluster_df.loc[i],distance = self._cluster_data_object(X_,y)
        else:
            for i, x in enumerate(X_):
                distance_local = 0
                if y is not None and len(y)>i:
                    class_cluster_df.loc[i],distance_local = self._cluster_data_object(x,y[i])
                else:
                    class_cluster_df.loc[i],distance_local = self._cluster_data_object(x,-1)
                distance += distance_local
        return class_cluster_df,distance

    def _get_model_complete_evaluation_(self, X, y, true_file):
        """
        Receives a dataset and compute quality evaluation measures, intra-cluster sum of distances, and runtime.
        """
        model_subspace = self._get_subspaces_candidate_centers()
        class_cluster,distance = self._cluster_data_frame(X,y)
        class_cluster = self._filter_noise_objects(class_cluster, true_file.noise_clusters)
        runtime = timer() - self.time_start
        functional_evaluation_result = functional_evaluation(model_subspace,
                                                             class_cluster["class"],
                                                             class_cluster["cluster"],
                                                             true_data_set=true_file,
                                                             threshold_cluster_validity=self.threshold_cluster_validity)
        return [distance] + functional_evaluation_result + [runtime]

    def _get_model_current_evaluation(self, true_file):
        """
        Compute quality evaluation measures, intra-cluster sum of distances, and runtime; on the current sample.
        """
        model_subspace = self._get_subspaces_candidate_centers()
        class_cluster = self._get_class_clusters_current_data_sample()
        class_cluster = self._filter_noise_objects(class_cluster, true.noise_clusters)
        functional_evaluation_result = functional_evaluation(model_subspace,
                                                             class_cluster["class"],
                                                             class_cluster["cluster"],
                                                             true_data_set=true_file,
                                                             threshold_cluster_validity=self.threshold_cluster_validity)
        return functional_evaluation_result + [timer() - self.time_start]

                            


class SubCMedians(SubCMedians_customizable):
    """
    Creates a SubCMedians object. The main parameters are the maximal model size SDmax, the sample size N and the number of iterations NbIter. The dataset dimensionality D is also requiered. 
    # SDmax maximal model size
    # D dimensionality
    # N size of the sample
    # NbIter number of iterations
    """
    def __init__(self, **params):
        SubCMedians_customizable.__init__(self,**params)
        self.set_params(**params)
        self.data_objects_index_in_sample = []
        self.data_objects_index_not_in_sample = []

    def set_params(self, **params):
        """
        Set the parameters provided to the construtor
        """
        if not params:
            self._reallocate_memory()
            return self
        for name in params:
            if not hasattr(self, name):
                raise ValueError('Invalid parameter %s for estimator %s.'
                                 'Check the list of available parameters '
                                 'with `KymerClust.get_params().keys()`.' %
                                 (name, self))
            setattr(self, name, params[name])

        SubCMediansWrapper_c.set_parameters(self._p_subcmedians_c,
                                       self.SDmax,
                                       self.D,
                                       self.N,
                                       self.threshold_cluster_validity,
                                       self.seed,
                                       self.option_deletion,
                                       self.option_insertion,
                                       self.option_FIFO,
                                       self.option_train_with_latest,
                                       self.option_lazy_hill_climbing,
                                       self.population_size,
                                       self.nb_generations_generation_update)
        self._reallocate_memory()
        return self

    def get_params(self, deep=True):
        """
        Get the current parameters
        """
        params = {param: getattr(self, param) for param in self._parameters}
        return params

    def _set_data_sample(self, X, y = None):
        """
        Set the data sample objects drawing randomly objects from the dataset X
        """
        self.data_objects_index_in_sample = []
        self.data_objects_index_not_in_sample = range(len(X))
        for _ in xrange(self.N):
            random_element = np.random.randint(0,len(self.data_objects_index_not_in_sample))
            random_index = self.data_objects_index_not_in_sample.pop(random_element)
            self.data_objects_index_in_sample.append(random_index)
            if y:
                self._send_array(X[random_index,:], y[random_index])
            else:
                self._send_array(X[random_index,:])
            SubCMediansWrapper_c.insert_SubCMedians_point_in_D(self._p_subcmedians_c, self._data_object)

    def fit_online_mode(self, X, y=None):
        """
        Sklearn-like fit function, receives a dataset and build the subspace clustering that models the data.
        This function has been created to deal with streams of data, in this case the dataset provided as an input will never appear again, so it does not make sense to keep record of the sample used or not
        """
        print "ONLINE"
        if X is None:
            return None
        X_ = self._check_X_matrix_validity(X)
        if len(X_.shape) == 1:
            self._send_array(X_, y)
            SubCMediansWrapper_c.train_model_with_SubCMedianspoint(self._p_subcmedians_c, self._data_object)
            self.generation += 1
        else:
            for i, x in enumerate(X_):
                if y:
                    self._send_array(x, y[i])
                else:
                    self._send_array(x)
                SubCMediansWrapper_c.train_model_with_SubCMedianspoint(self._p_subcmedians_c, self._data_object)
                self.generation += 1

    def fit(self, X, y=None, verbose=0):
        """
        sklearn-like fit function, receives a dataset and build the subspace clustering that models the data
        """
        print ""
        if X is None:
            return None
        if X.size < self.N:
            raise RuntimeError('The dataset provided is smaller than the sample size, use instead the fit_online function')
        X_ = self._check_X_matrix_validity(X)
        self._set_data_sample(X_, y)
        for iteration in xrange(self.NbIter):
            random_element = np.random.randint(0,len(self.data_objects_index_not_in_sample))
            random_index = self.data_objects_index_not_in_sample.pop(random_element)
            data_object_index_removed_from_sample = self.data_objects_index_in_sample.pop(0)
            self.data_objects_index_in_sample.append(random_index)
            self.data_objects_index_not_in_sample.append(data_object_index_removed_from_sample)
            if y:
                self._send_array(X_[random_index,:], y[random_index])
            else:
                self._send_array(X_[random_index,:])
            SubCMediansWrapper_c.train_model_with_SubCMedianspoint(self._p_subcmedians_c, self._data_object)
            self.generation += 1
            if verbose:
                sys.stdout.write("\r"+str(iteration)+"/"+str(self.NbIter))
                sys.stdout.flush()
        print ""

    def predict(self, X):
        """
        sklearn-like predict function, receives a dataset and compute the cluster membership of its data objects
        """
        X_ = self._check_X_matrix_validity(X)
        Y_ = array([])
        for i, x in enumerate(X_):
            self._send_array(x)
            cluster, distance = SubCMediansWrapper_c.clusterize_SubCMedianspoint_with_model(self._p_subcmedians_c,
                                                                                  self._data_object)
            Y_ = append(Y_, cluster)
        return Y_

    def fit_predict(self, X, y=None):
        """
        sklearn-like fit_predict function, applies fit and the predict functions over dataset X
        """
        self.fit(X, y)
        return self.predict(X)

    def score(self, X):
        """
        Compute the mean intra-cluster distance
        """
        X_ = self._check_X_matrix_validity(X)
        scores = []
        for i, x in enumerate(X_):
            self._send_array(x)
            cluster, distance = SubCMediansWrapper_c.clusterize_SubCMedianspoint_with_model(self._p_subcmedians_c,
                                                                                  self._data_object)
            scores.append(distance)
        return np.asarray(scores).mean()

    def transform(self, X):
        """
        Sklearn-like transform function, computes the distance between each data point and the current candidate centers
        """
        X_ = self._check_X_matrix_validity(X)
        X_new = []
        for x in X_:
            X_new.append(self._transform_array(x))
        return array(X_new)

    def fit_transform(self, X, y=None):
        """
        Sklearn-like fit_transform function, first applies the fit function and the the transform one
        """
        self.fit(X, y)
        return self.transform(X)