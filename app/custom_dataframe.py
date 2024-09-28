from typing import Dict
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, columns=self.COLUMNS)

    @staticmethod
    def generate_uid() -> str:
        return str(uuid4())

    def add_row(self, row: pd.Series) -> Dict[str, str]:
        new_uid = self.generate_uid()

        # TODO: adding by rules
        self.loc[new_uid] = row

        return {"uid": new_uid, "is_new": True}

    def is_in(self, row: pd.Series) -> bool:
        pass

    def add_dataframe(self, df: pd.DataFrame) -> None:
        pass
