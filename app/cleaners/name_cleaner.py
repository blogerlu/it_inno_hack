import re

from app.cleaners.base_cleaner import BaseCleaner


class NameCleaner(BaseCleaner):
    def clean(self, full_name):
        """Разделяет и стандартизирует full_name на first_name, middle_name, last_name"""
        # Удаление лишних символов
        full_name = re.sub(r"\d|\n|\\|/", "", full_name).strip().upper()
        full_name = re.sub(r"ОГЛЫ|ОГЛИ|КЫЗЫ", "", full_name)
        parts = re.split(r"\s+", full_name)  # Разделение по пробелам

        # Возвращаем разделенные части ФИО
        return {
            "first_name": parts[1] if len(parts) > 1 else "",
            "middle_name": parts[2] if len(parts) > 2 else "",
            "last_name": parts[0] if len(parts) > 0 else "",
        }
