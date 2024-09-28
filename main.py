import pandas as pd

from app.cleaners.birthdate_cleaner import BirthdateCleaner
from app.cleaners.email_cleaner import EmailCleaner
from app.cleaners.name_cleaner import NameCleaner
from app.cleaners.phone_cleaner import PhoneCleaner
from app.duplicate_finder import DuplicateFinder


class DataProcessor:
    def __init__(self, df):
        self.df = df
        self.cleaners = {
            "name": NameCleaner(),
            "email": EmailCleaner(),
            "phone": PhoneCleaner(),
            "birthdate": BirthdateCleaner(),
        }

    def clean_data(self):
        """Применение всех очисток к данным"""
        # self.df["name"] = self.df["name"].apply(self.cleaners["name"].clean)
        self.df["email"] = self.df["email"].apply(self.cleaners["email"].clean)
        self.df["phone"] = self.df["phone"].apply(self.cleaners["phone"].clean)
        self.df["birthdate"] = self.df["birthdate"].apply(self.cleaners["birthdate"].clean)

    def find_duplicates(self):
        """Поиск дубликатов"""
        finder = DuplicateFinder(self.df)
        duplicates = finder.find_duplicates(["email", "birthdate", "phone"])
        return duplicates


def main():
    df = pd.read_csv("data/public/main1.csv", nrows=100000)
    processor = DataProcessor(df)
    processor.clean_data()
    duplicates = processor.find_duplicates()
    print(len(duplicates))


if __name__ == "__main__":
    main()
