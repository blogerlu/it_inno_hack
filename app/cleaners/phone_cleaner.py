import re

from app.cleaners.base_cleaner import BaseCleaner


class PhoneCleaner(BaseCleaner):
    def clean(self, phone):
        """Стандартизация телефонов к формату XXXXXXXXXX"""
        phone = re.sub(r"\D", "", phone)  # Убираем все кроме цифр
        if len(phone) == 11 and phone.startswith("8"):
            phone = phone[1:]
        if len(phone) != 11:
            return None  # Некорректный телефон
        return str(phone[1:])
