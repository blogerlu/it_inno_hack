import numpy as np
import pandas as pd
from gensim.models import Word2Vec


def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


def preprocess_column(column: pd.Series) -> pd.Series:
    return column.astype(str).apply(lambda x: x.lower().split())


def train_word2vec_model(
    train_tokens: pd.Series, vector_size: int = 100, window: int = 5, min_count: int = 1, workers: int = 4
) -> Word2Vec:
    model = Word2Vec(
        sentences=train_tokens, vector_size=vector_size, window=window, min_count=min_count, workers=workers
    )
    return model


def save_word2vec_model(model: Word2Vec, filepath: str) -> None:
    model.save(filepath)


def load_word2vec_model(filepath: str) -> Word2Vec:
    return Word2Vec.load(filepath)


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


def main_word2vec_process(filepath: str, model_save_path: str) -> pd.DataFrame:
    df = load_data(filepath)

    # Разделение на 50% для обучения и 50% для инференса
    train_df = df.sample(frac=0.5, random_state=42)
    inference_df = df.drop(train_df.index)

    # Обучение модели Word2Vec
    train_names = preprocess_column(train_df["name"])
    train_addresses = preprocess_column(train_df["address"])
    train_tokens = pd.concat([train_names, train_addresses])
    model = train_word2vec_model(train_tokens)

    # Сохранение модели
    save_word2vec_model(model, model_save_path)

    # Загрузка модели и инференс
    loaded_model = load_word2vec_model(model_save_path)
    inference_names = preprocess_column(inference_df["name"])
    inference_addresses = preprocess_column(inference_df["address"])

    # Преобразование векторов
    inference_name_vectors = get_word_vectors(inference_names.astype(str), loaded_model)
    inference_address_vectors = get_word_vectors(inference_addresses.astype(str), loaded_model)

    # Добавление векторов в DataFrame
    inference_df["name_vector"] = inference_name_vectors
    inference_df["address_vector"] = inference_address_vectors

    return inference_df


if __name__ == "__main__":
    df_with_vectors = main_word2vec_process("../../data/public/main1_clean.csv", "../data/weights/word2vec_model.model")
    print(df_with_vectors[["name", "address", "name_vector", "address_vector"]].head())
