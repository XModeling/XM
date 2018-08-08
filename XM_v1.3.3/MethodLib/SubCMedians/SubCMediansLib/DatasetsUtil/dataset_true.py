import pandas as pd

class true_file:
	def __init__(self,file_name,hidden_cluster_membership,conversion_dico,hidden_cluster_dim,dim_i="",noise_clusters=[-1]):
		self.file_name = file_name
		self.noise_clusters = noise_clusters
		self.hidden_noise_clus = [666]
		f = file(file_name, "r")
		dim = f.readline().split(";")[0].split("=")
		if len(dim) > 1:
			dim = int(dim[1])
		else:
			dim = dim_i
		self.clusters_subspaces = {}
		self.clusters_membership = []
		for i,line in enumerate(f):
			l = map(int,line.split(" "))
			self.clusters_subspaces[i]=[]
			for j,element in enumerate(l[0:dim]):
				if element:
					self.clusters_subspaces[i].append(j)
			self.clusters_subspaces[i] = set(self.clusters_subspaces[i])
			self.clusters_membership.append(l[dim+1:len(l)])
		f.close()
		self.true_arff_dico = {}
		self.arff_true_dico = {}
		self.df_true_dico = {}
		self.generate_dico_arff_true_clusters(hidden_cluster_membership)
		self.compute_df_true_dico(conversion_dico[hidden_cluster_dim[0]])
		self.compute_hidden_noise_clus(conversion_dico[hidden_cluster_dim[0]])

	def generate_dico_arff_true_clusters(self, arff_membership):
		self.true_arff_dico = {}
		self.arff_true_dico = {}
		for i, hidden_cluster_true in enumerate(self.clusters_membership):
			self.true_arff_dico[i] = []
			for point in hidden_cluster_true:
				if arff_membership[point] not in self.true_arff_dico[i]:
					self.true_arff_dico[i].append(arff_membership[point])
		self.arff_true_dico = self.invert_dict(self.true_arff_dico)
		return self.check_arff_true_dico(arff_membership)

	def invert_dict(self,dico):
		inv_map = {}
		for k, v in dico.iteritems():
			for vi in v:
				inv_map[vi] = inv_map.get(vi, [])
				inv_map[vi].append(k)
		return inv_map

	def check_arff_true_dico(self, arff_membership):
		for i, arff_i in enumerate(arff_membership):
			if arff_i not in self.noise_clusters:
				for true_cluster in self.arff_true_dico[arff_i]:
					if i not in self.clusters_membership[true_cluster]:
						return 0
		return 1

	def compute_df_true_dico(self, arff_df_dico):
		self.df_true_dico = {}
		for arff_i in self.arff_true_dico.keys():
			self.df_true_dico[arff_df_dico[arff_i]] = self.arff_true_dico[arff_i]

	def compute_hidden_noise_clus(self,arff_df_dico):
		self.hidden_noise_clus = []
		for k in self.noise_clusters:
			if k in arff_df_dico.keys():
				self.hidden_noise_clus.append(arff_df_dico[k])
		if not len(self.hidden_noise_clus):
			self.hidden_noise_clus = [666]