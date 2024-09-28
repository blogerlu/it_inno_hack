from typing import Dict, Any, List, Tuple
from uuid import uuid4

import pandas as pd


class CustomDataFrame(pd.DataFrame):
    COLUMNS = [
        "uid",
        "first_name",
        "middle_name",
        "last_name",
        "birthdate",
        "sex",
        "phone1",  # старый и новый телефоны
        "phone2",
        "address",
        "email1",  # множественный email
        "email2",
        "email3",
    ]

    SIMILARITY_THRESHOLD = 0.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, columns=self.COLUMNS)

    @staticmethod
    def generate_uid() -> str:
        return str(uuid4())

    @staticmethod
    def get_similarity(row1: pd.Series, row2: pd.Series) -> float:  # TODO: create rules system
        if row1["email1"] == row2["email"]:
            return 1
        if row1["phone1"] == row2["phone"]:
            return 1
        return 0

    def add_row(self, row: pd.Series) -> str:
        intersection_columns = set(row.index) & set(self.columns)
        new_uid = self.generate_uid()

        for column in intersection_columns:
            self.at[new_uid, column] = row[column]

        return new_uid

    def delete_row(self, uid: str) -> None:
        self.drop(uid, inplace=True)

    def combine_rows(self, rows: List[pd.Series]) -> pd.Series:
        new_row = pd.Series([], index=self.columns)

        for row in rows:
            intersection_columns = set(row.index) & set(self.columns)

            for column in intersection_columns:
                if new_row[column].strip() == "":
                    new_row[column] = row[column]

        return new_row

    def register_row(self, row: pd.Series) -> Dict[str, Any]:
        duplicates = self.get_duplicates(row)

        if len(duplicates) == 0:
            new_uid = self.add_row(row)
            return {
                "uid": new_uid,
                "duplicates": [],
            }

        for duplicate in duplicates:
            self.delete_row(duplicate[0])

        combined_row = self.combine_rows([row, *duplicates])

        new_uid = self.add_row(combined_row)
        return {
            "uid": new_uid,
            "duplicates": duplicates,
        }

    def get_duplicates(self, row: pd.Series) -> List[Tuple[str, float]]:
        duplicates = []
        for index in self.index:
            row0 = self.loc[index]
            similarity = self.get_similarity(row0, row)
            if similarity > self.SIMILARITY_THRESHOLD:
                duplicates.append((row0["uid"], similarity))
        return duplicates
