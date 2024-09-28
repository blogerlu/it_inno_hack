import re

from app.cleaners.base_cleaner import BaseCleaner


class EmailCleaner(BaseCleaner):
    def clean(self, email):
        """Приведение email к нижнему регистру, исправление символов и проверка на корректность"""
        email = email.strip().lower()
        email = email.replace(";", "@")  # Исправление ошибок замены ; на @

        # Проверка на корректность email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return None  # Неверный формат email
        return email
