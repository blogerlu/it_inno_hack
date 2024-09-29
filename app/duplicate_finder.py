import pandas as pd
import recordlinkage as rl
from recordlinkage.compare import String


class DuplicateFinder:
    def __init__(self):
        self.comparer = rl.Compare(
            [
                String("name", "name", method="jarowinkler", threshold=0.75, label="name"),
                String("email", "email", method="jarowinkler", threshold=0.95, label="email"),
                String("birthdate", "birthdate", method="damerau_levenshtein", threshold=0.8, label="birthdate"),
                String("phone", "phone", method="damerau_levenshtein", threshold=0.9, label="phone"),
            ]
        )

        self.indexer = rl.Index()
        self.indexer.block(left_on="name", right_on="name")
        self.indexer.block(left_on="phone", right_on="phone")
        self.indexer.block(left_on="email", right_on="email")
        self.indexer.block(left_on="birthdate", right_on="birthdate")

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        candidates = self.indexer.index(df)
        features = self.comparer.compute(candidates, df)
        potential_duplicates = features[features.sum(axis=1) > 1]
        duplicate_pairs = pd.DataFrame(potential_duplicates.index.tolist(), columns=["index1", "index2"])
        duplicate_pairs["uid1"] = duplicate_pairs["index1"].mapply(lambda x: df.loc[x, "name"])
        duplicate_pairs["uid2"] = duplicate_pairs["index2"].mapply(lambda x: df.loc[x, "name"])
        return duplicate_pairs[["uid1", "uid2"]]

    def fast_call(self, df: pd.DataFrame) -> pd.DataFrame:
        df["phone"] = df["phone"].fillna("")
        df["email"] = df["email"].fillna("")

        # Разбиваем имя на составляющие (ФИО или ФИ)
        df["name_split"] = df["name"].str.split()
        df["first_last"] = df["name_split"].apply(lambda x: " ".join(x[:2]) if len(x) >= 2 else x[0])

        phone_pairs = self.find_pairs_by_column(df, "phone")
        email_pairs = self.find_pairs_by_column(df, "email")
        name_pairs = self.find_pairs_by_column(df, "first_last")

        all_pairs = pd.concat([phone_pairs, email_pairs, name_pairs]).drop_duplicates().reset_index(drop=True)

        return all_pairs

    @staticmethod
    def find_pairs_by_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Находит пары дубликатов по указанному столбцу с использованием merge для поиска совпадений"""
        df_non_empty = df[(df[column] != "") & (df[column].str.len() >= 3)]
        merged = df_non_empty.merge(df_non_empty, on=column, suffixes=("1", "2"))
        merged = merged[merged["uid1"] != merged["uid2"]]
        return merged[["name1", "name2", "uid1", "uid2"]]
