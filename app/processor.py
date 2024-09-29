import pandas as pd

from app.cleaners import BirthdateCleaner, EmailCleaner, NameCleaner, PhoneCleaner
from app.duplicate_finder import DuplicateFinder


class Processor:
    COLUMNS = [
        "uid",
        "name",
        "email",
        "phone",
        "birthdate",
        "address",
    ]

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.create_needed_columns()
        self.cleaners = {
            "name": NameCleaner(),
            "email": EmailCleaner(),
            "phone": PhoneCleaner(),
            "birthdate": BirthdateCleaner(),
        }
        self.duplicate_finder = DuplicateFinder()

    def create_needed_columns(self) -> None:
        for column in self.COLUMNS:
            if column not in self.df.columns:
                self.df[column] = ""

    def clean_data(self) -> pd.DataFrame:
        self.df["name"] = self.df["name"].apply(self.cleaners["name"].clean)
        self.df["email"] = self.df["email"].apply(self.cleaners["email"].clean)
        self.df["phone"] = self.df["phone"].apply(self.cleaners["phone"].clean)
        self.df["birthdate"] = self.df["birthdate"].apply(self.cleaners["birthdate"].clean)
        return self.df

    def find_duplicates(self) -> pd.DataFrame:
        return self.duplicate_finder(self.df)
