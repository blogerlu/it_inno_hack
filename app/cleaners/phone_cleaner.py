import re

from app.cleaners.base_cleaner import BaseCleaner


class PhoneCleaner(BaseCleaner):
    def clean(self, phone: str) -> str:
        phone = str(phone)
        phone = phone.replace("+7", "8")
        phone = re.sub(r"\D", "", phone)  # Убираем все кроме цифр
        return phone
