import pandas as pd
from elasticsearch import Elasticsearch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from elasticsearch import helpers

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Fetch user sessions from ES
def fetch_sessions(index="user_sessions", size=1000):
    query = {
        "query": {
            "match_all": {}
        }
    }

    res = es.search(index=index, body=query, size=size)
    hits = res["hits"]["hits"]
    data = [
        {
            "user_id": hit["_source"]["user_id"],
            "search_query": hit["_source"]["search_query"]
        }
        for hit in hits
    ]
    return pd.DataFrame(data)

# TF-IDF + KMeans clustering
def cluster_users(df, num_clusters=5):
    tfidf = TfidfVectorizer(stop_words="english")
    vectors = tfidf.fit_transform(df["search_query"])

    model = KMeans(n_clusters=num_clusters, random_state=42)
    df["cluster"] = model.fit_predict(vectors)

    return df, model, tfidf


def label_clusters(df):
    segment_labels = {}

    for cluster_id in df["cluster"].unique():
        queries = " ".join(df[df["cluster"] == cluster_id]["search_query"].tolist()).lower()

        if any(word in queries for word in ["gaming", "tech", "laptop", "keyboard"]):
            label = "tech_enthusiast"
        elif any(word in queries for word in ["discount", "cheap", "offer", "deal"]):
            label = "budget_buyer"
        elif any(word in queries for word in ["dress", "style", "fashion", "jacket"]):
            label = "fashion_oriented"
        else:
            label = "other"

        segment_labels[cluster_id] = label

    df["segment"] = df["cluster"].map(segment_labels)
    return df


def save_segmented_users_to_es(df, index="user_segments"):
    actions = [
        {
            "_index": index,
            "_id": row["user_id"],
            "_source": {
                "user_id": row["user_id"],
                "search_query": row["search_query"],
                "segment": row["segment"]
            }
        }
        for _, row in df.iterrows()
    ]

    # Delete old index if it exists
    if es.indices.exists(index=index):
        es.indices.delete(index=index)

    # Bulk insert
    helpers.bulk(es, actions)
    print(f"Saved {len(actions)} segmented users to index '{index}'.")



if __name__ == "__main__":
    df = fetch_sessions()
    clustered_df, model, tfidf = cluster_users(df)
    labeled_df = label_clusters(clustered_df)

    print(labeled_df.groupby("segment").head(3))

    # Save back to ES
    save_segmented_users_to_es(labeled_df)
