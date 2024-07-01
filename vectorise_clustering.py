import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

def vectorise_clustering(excel_file, optimal_clusters, if_display):
    df = pd.read_excel(excel_file)

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['Abstract'])

    wcss = []
    silhouette_scores = []

    for i in range(2, 20):
        kmeans = KMeans(n_clusters=i, random_state=30)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X, kmeans.labels_))

    if if_display:
        # Plotting the results
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(range(2, 20), wcss, marker='o')
        plt.title('Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')

        plt.subplot(1, 2, 2)
        plt.plot(range(2, 20), silhouette_scores, marker='o')
        plt.title('Silhouette Scores')
        plt.xlabel('Number of clusters')
        plt.ylabel('Silhouette Score')

        plt.tight_layout()
        plt.show()


    kmeans = KMeans(n_clusters=optimal_clusters, random_state=30)
    kmeans.fit(X)

    df['cluster'] = kmeans.labels_

    # Print Silhouette Score
    silhouette_avg = silhouette_score(X, kmeans.labels_)
    print(f'Silhouette Score: {silhouette_avg}')


    # Output 
    df.to_csv('clustering_results.csv', index=False)

    summary = df.groupby('cluster')['Abstract'].count().reset_index()
    summary.columns = ['Cluster', 'Number of Papers']
    summary['Key Terms'] = summary['Cluster'].apply(lambda x: ', '.join(vectorizer.get_feature_names_out()[kmeans.cluster_centers_[x].argsort()[-5:][::-1]]))

    summary.to_csv('clustering_summary.csv', index=False)
