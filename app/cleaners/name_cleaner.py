import re

from app.cleaners.base_cleaner import BaseCleaner


class NameCleaner(BaseCleaner):
    def clean(self, name: str) -> str:
        name = re.sub(r"\d|\n|\\|/", "", name).strip().upper()
        name = re.sub(r"ОГЛЫ|ОГЛИ|КЫЗЫ", "", name)
        return name
