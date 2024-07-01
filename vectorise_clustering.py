import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE

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
    # df['KeyTerms'] = df['cluster'].apply(lambda x: ', '.join(vectorizer.get_feature_names_out()[kmeans.cluster_centers_[x].argsort()[-5:][::-1]]))
    df.reset_index(inplace=True)

    # Print Silhouette Score
    silhouette_avg = silhouette_score(X, kmeans.labels_)
    print(f'Silhouette Score: {silhouette_avg}')


    # t-SNE Visualisation:
    tsne = TSNE(n_components=2, random_state=30, perplexity=20, init='random')
    tsne_results = tsne.fit_transform(X.toarray())

    df['TSNE1'] = tsne_results[:, 0]
    df['TSNE2'] = tsne_results[:, 1]

    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='TSNE1', y='TSNE2', hue='cluster', data=df, palette='tab10')
    
    for i in range(df.shape[0]):
        plt.text(df.TSNE1[i], df.TSNE2[i], str(df.index[i]), fontsize=7)

    plt.title('t-SNE Clustering Papers')
    plt.xlabel('t-SNE 1')
    plt.ylabel('t-SNE 2')
    plt.legend(title='Cluster')
    plt.show()


    # Output 
    df.to_csv('clustering_results.csv', index=False)

    summary = df.groupby('cluster')['Abstract'].count().reset_index()
    summary.columns = ['Cluster', 'Number of Papers']
    summary['Key Terms'] = summary['Cluster'].apply(lambda x: ', '.join(vectorizer.get_feature_names_out()[kmeans.cluster_centers_[x].argsort()[-5:][::-1]]))

    summary.to_csv('clustering_summary.csv', index=False)
