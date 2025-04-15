# summary_module.py
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np

class CommentSummarizer:
    def __init__(self, model_name='all-MiniLM-L6-v2', num_clusters=5):
        self.model = SentenceTransformer(model_name)
        self.num_clusters = num_clusters

    def embed_comments(self, comments):
        return self.model.encode(comments, convert_to_tensor=False)

    def cluster_comments(self, embeddings):
        kmeans = KMeans(n_clusters=self.num_clusters, random_state=42)
        labels = kmeans.fit_predict(embeddings)
        return labels, kmeans.cluster_centers_

    def find_representative_comments(self, comments, embeddings, labels, centers):
        cluster_summaries = []
        for cluster_id in range(self.num_clusters):
            indices = [i for i, label in enumerate(labels) if label == cluster_id]
            cluster_comments = [comments[i] for i in indices]
            cluster_embeddings = [embeddings[i] for i in indices]

            center = centers[cluster_id]
            distances = [np.linalg.norm(embed - center) for embed in cluster_embeddings]
            min_index = np.argmin(distances)
            representative_comment = cluster_comments[min_index]
            example_comments = cluster_comments[:2]

            cluster_summaries.append({
                "topic": f"Küme {cluster_id + 1}",
                "summary": representative_comment,
                "example_comments": example_comments
            })
        return cluster_summaries

    def summarize(self, comments):
        if not comments:
            return []
        embeddings = self.embed_comments(comments)
        labels, centers = self.cluster_comments(embeddings)
        return self.find_representative_comments(comments, embeddings, labels, centers)
