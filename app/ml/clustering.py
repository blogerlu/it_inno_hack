import time

import numpy as np
import pandas as pd
from sklearn.cluster import MiniBatchKMeans


def prepare_vectors_for_clustering(df: pd.DataFrame, name_vector_col: str, address_vector_col: str) -> np.ndarray:
    name_vectors = np.array(df[name_vector_col].tolist())
    address_vectors = np.array(df[address_vector_col].tolist())
    return name_vectors + address_vectors  # Можно выбрать разные способы комбинирования векторов


def apply_mini_batch_kmeans(vector_values: np.ndarray, n_clusters: int, batch_size: int) -> np.ndarray:
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, batch_size=batch_size)
    start_time = time.time()
    kmeans.fit(vector_values)
    labels = kmeans.predict(vector_values)
    end_time = time.time()
    print(f"Время работы MiniBatchKMeans: {end_time - start_time:.2f} секунд")
    return labels


def main_clustering_process(
    df: pd.DataFrame,
    name_vector_col: str = "name_vector",
    address_vector_col: str = "address_vector",
    n_clusters: int = 100,
    batch_size: int = 10000,
) -> pd.DataFrame:
    vector_values = prepare_vectors_for_clustering(df, name_vector_col, address_vector_col)
    vector_values = vector_values[~np.all(vector_values == 0, axis=1)]
    labels = apply_mini_batch_kmeans(vector_values, n_clusters=n_clusters, batch_size=batch_size)
    df["cluster"] = labels
    return df


if __name__ == "__main__":
    df_with_vectors = pd.read_csv("inference_with_vectors.csv")
    df_with_clusters = main_clustering_process(df_with_vectors)
    print(df_with_clusters[["name", "address", "cluster"]].head())
