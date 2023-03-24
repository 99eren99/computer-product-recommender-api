from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler 
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer

def cluster_and_label_products(df:pd.DataFrame,numerical_attributes):
    """1-Apply PCA with min n_components with having explained varience>%80\n
       2-Apply Kmeans with min n_clusterss with having explained varience>%80\n
       3-Label products with cluster labels"""
    copy_df_with_numerical_attributes=df[numerical_attributes].copy(deep=True)
    #mode imputing
    copy_df_with_numerical_attributes=copy_df_with_numerical_attributes.fillna(copy_df_with_numerical_attributes.mode().iloc[0])
    #centralize data with standart scaler
    centralized_attributes=StandardScaler().fit_transform(copy_df_with_numerical_attributes)
    #keep %80 of total varience with PCA to get rid of curse of dimensionality
    pca = PCA(n_components=0.8, svd_solver='full')
    reducted_centralized_attributes=pca.fit_transform(centralized_attributes)
    #cluster&label products with Kmeans by search of min n_clusters with explained varience>%80
    explained_varience_ratio=0
    n_clusters=2
    sample_labels=None
    while(explained_varience_ratio<0.80):#increase n cluster till reach %80 varience explanation
        k_means_model=KMeans(n_clusters=n_clusters).fit(reducted_centralized_attributes)
        centroids=k_means_model.cluster_centers_
        distance_between_samples_and_centroids = cdist(reducted_centralized_attributes, centroids, 'euclidean')
        sample_labels= np.argmin(distance_between_samples_and_centroids,axis=1)#label samples wrt nearest centroids
        distance_between_samples_and_assigned_centroids=np.min(distance_between_samples_and_centroids,axis=1)
        within_cluster_ss = sum(distance_between_samples_and_assigned_centroids**2)
        total_ss = sum(pdist(reducted_centralized_attributes)**2)/reducted_centralized_attributes.shape[0]
        explained_ss = total_ss-within_cluster_ss
        explained_varience_ratio=explained_ss/total_ss
        n_clusters+=1
    df["Cluster Label"]=sample_labels

def match_items_with_most_cosine_smilar(df:pd.DataFrame):
    """1-Get copy of product names column and lower it\n
       2-Vectorize product names\n
       3-Compute cosine similarities\n
       4-Add column of the most cosine similar item's index to the input df"""
    copy_df_of_product_name=df["Ürün Adı"].copy(deep=True).apply(lambda x : x.lower())
    vectorizer = CountVectorizer()
    vector_array = vectorizer.fit_transform(copy_df_of_product_name).toarray()
    cosine_similarity_matrix= 1 - cdist(vector_array, vector_array, 'cosine')#cosine similarity=1-cosine of vectors
    cosine_similarity_matrix[np.diag_indices_from(cosine_similarity_matrix)]=0#set 0 to self similarities
    indices_of_max_similarity=np.argmax(cosine_similarity_matrix,axis=1)
    df["Cosine Similar"]=indices_of_max_similarity#add most similar products

def match_items_with_two_nearest_neighbour(df:pd.DataFrame,numerical_attributes):
    """1-Apply PCA with min n_components with having explained varience>%80\n
       2-Apply NearestNeighbor and find nearest two products\n
       3-Add nearest two products' index to the input df"""
    copy_df_with_numerical_attributes=df[numerical_attributes].copy(deep=True)
    #mode imputing
    copy_df_with_numerical_attributes=copy_df_with_numerical_attributes.fillna(copy_df_with_numerical_attributes.mode().iloc[0])
    #scale data with standart scaler
    scaled_attributes=StandardScaler().fit_transform(copy_df_with_numerical_attributes)
    #keep %80 of total varience with PCA to get rid of curse of dimensionality
    pca = PCA(n_components=0.8, svd_solver='full')
    reducted_scaled_attributes=pca.fit_transform(scaled_attributes)
    #find most similar products with nearest neighbors
    nn_model = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(reducted_scaled_attributes)
    _ , indices = nn_model.kneighbors(reducted_scaled_attributes)
    for i in range(1,indices.shape[1]):#add nearest neighbors to df
        df[str(i)+".NearestNeighbor"]=indices[:,i]