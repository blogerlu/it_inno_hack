import re

from app.cleaners.base_cleaner import BaseCleaner


class BirthdateCleaner(BaseCleaner):
    def clean(self, birthdate: str) -> str:
        birthdate = re.sub(r"\D", "", birthdate)  # Убираем все кроме цифр
        return birthdate
