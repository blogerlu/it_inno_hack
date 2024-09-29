import re

from transliterate import translit

from app.cleaners.base_cleaner import BaseCleaner


class NameCleaner(BaseCleaner):
    def clean(self, name: str) -> str:
        name = re.sub(r"\d|\n|\\|/", "", name).strip().upper()
        name = translit(name, "ru")
        name = re.sub(r"(.)\1+", r"\1", name)
        name = re.sub(r"[^А-ЯЁ ]", "", name)
        name = name.replace("ОГЛЫ", "")
        name = name.replace("ОГЛИ", "")
        name = name.replace("УГЛЫ", "")
        name = name.replace("УГЛИ", "")
        name = name.replace("НЕТ", "")
        name = " ".join(name.split())
        return name
