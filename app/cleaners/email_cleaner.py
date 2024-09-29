import re

from app.cleaners.base_cleaner import BaseCleaner


class EmailCleaner(BaseCleaner):
    def clean(self, email: str) -> str:
        # remove all non-alphanumeric characters but not the @ and _ symbol
        email = str(email)
        email = email.lower()
        email = re.sub(r"[^a-z0-9@_]", "", email)
        for i in range(10):
            email = email.split(f"{i}")[0]
        return email
