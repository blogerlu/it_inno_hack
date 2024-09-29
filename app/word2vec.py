import numpy as np
import pandas as pd
from gensim.models import Word2Vec

df = pd.read_csv("../data/public/")

train_df = df.sample(frac=0.5, random_state=42)
inference_df = df.drop(train_df.index)


def preprocess_column(column: pd.Series) -> pd.Series:
    return column.astype(str).apply(lambda x: x.lower().split())


def get_word_vectors(column: pd.Series, model: Word2Vec) -> list:
    vectors = []
    for sentence in column:
        tokens = sentence.split()
        sentence_vectors = [model.wv[token] for token in tokens if token in model.wv]
        if sentence_vectors:
            avg_vector = np.mean(sentence_vectors, axis=0)
            vectors.append(avg_vector)
        else:
            vectors.append(np.zeros(model.vector_size))
    return vectors


train_names = preprocess_column(train_df["name"])
train_addresses = preprocess_column(train_df["address"])

train_tokens = pd.concat([train_names, train_addresses])

model = Word2Vec(sentences=train_tokens, vector_size=100, window=5, min_count=1, workers=4)

model.save("../data/weights/word2vec_model.model")

loaded_model = Word2Vec.load("word2vec_model.model")

inference_names = inference_df["name"].astype(str)
inference_addresses = inference_df["address"].astype(str)

inference_name_vectors = get_word_vectors(inference_names, loaded_model)
inference_address_vectors = get_word_vectors(inference_addresses, loaded_model)

inference_df["name_vector"] = inference_name_vectors
inference_df["address_vector"] = inference_address_vectors

print(inference_df[["name", "address", "name_vector", "address_vector"]].head())
