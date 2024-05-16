from mtl_metro_data_visualization.categorization.tweets import Tweets


from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

t = Tweets()

print(t.df)

# # Convert the tweets into TF-IDF vectors
# tfidf_vectorizer = TfidfVectorizer(max_features=1000)
# tfidf_matrix = tfidf_vectorizer.fit_transform(t.df.tweet)

# # Apply K-means clustering
# num_clusters = 20  # You can adjust this parameter
# kmeans = KMeans(n_clusters=num_clusters, random_state=42)
# kmeans.fit(tfidf_matrix)

# # Get the cluster labels for each tweet
# cluster_labels = kmeans.labels_

# # df_ = df.copy()
# # df_['cluster'] = 0
# # df_.cluster = cluster_labels
# # df_[df_.cluster==3].tweet.unique()

# # Print the tweets in each cluster
# for cluster_id in range(num_clusters):
#     print(f"Cluster {cluster_id}:")
#     cluster_tweets = [df.tweet.iloc[i] for i, label in enumerate(cluster_labels) if label == cluster_id]
#     print(cluster_tweets[:5])  # Print the first 5 tweets in the cluster
#     print()