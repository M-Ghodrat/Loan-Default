from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np

class Dim_Red():

    def __init__(self, data, target):

        self.target = target
        self.data = data.copy()
        self.features = list(set(self.data.columns) - set([self.target]))
        self.target_numpy = self.data[self.target].to_numpy()
        self.features_numpy = self.data[self.features].to_numpy()
        self.feature_scores = None

    def DT(self, criterion='gini', splitter='best', max_depth=None, min_samples_split=2, 
            min_samples_leaf=1, max_features=None,  max_leaf_nodes=None, min_impurity_decrease=0.0, 
            min_impurity_split=None, num_feature = None):

        if num_feature == None:
            num_feature = len(self.features)

        dtree = DecisionTreeClassifier(criterion=criterion, splitter=splitter, max_depth=max_depth,
                                       min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                       max_features=max_features,  max_leaf_nodes=max_leaf_nodes,
                                       min_impurity_decrease=min_impurity_decrease, min_impurity_split=min_impurity_split)

        dtree.fit(self.features_numpy, self.target_numpy)
        self.feature_scores = pd.Series(dtree.feature_importances_, index=self.features).sort_values(ascending=False).index
        return self.data[self.feature_scores[:num_feature]]

    def RF(self, ):
        pass

    def PCA(self, n_components=2):
        pca = PCA(n_components=n_components)
        transformed = pca.fit_transform(self.features_numpy)
        self.explained_variance_ratio = pca.explained_variance_ratio_
        self.singular_values = pca.singular_values_
        return transformed

    def LDA(self, n_components=1):
        clf = LinearDiscriminantAnalysis(n_components=n_components)
        transformed = clf.fit_transform(self.features_numpy, self.target_numpy)
        return transformed
    
    def SvdTrunc(self, n_components):
        
        svd =  TruncatedSVD(n_components)
        transformed = svd.fit_transform(self.data)
        self.singular_values = svd.singular_values_
        column_names = [f"feature{i+1}" for i in range(n_components)]
        self.data = pd.DataFrame(transformed, columns=column_names)
        return self.data, svd

    def delete(self, axis, percent):

        if axis==1:
            cols = self.data.columns.values.tolist()
            for col in cols:
                if self.data[col].isna().sum() > self.data.shape[0]*(percent/100):
                    del self.data[col]

        if axis ==0:
            rows = self.data.shape[1]
            for row in range(rows):
                if self.data.iloc[row].isna().sum() > rows*(percent/100):
                    self.data.drop(self.data.index[row], inplace=True)

        return self.data
