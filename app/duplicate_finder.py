class DuplicateFinder:
    def __init__(self, df):
        self.df = df

    def find_duplicates(self, key_columns):
        """Поиск дубликатов на основе ключевых столбцов"""
        duplicates = self.df[self.df.duplicated(subset=key_columns, keep=False)]
        return duplicates
