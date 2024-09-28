import re

from app.cleaners.base_cleaner import BaseCleaner


class PhoneCleaner(BaseCleaner):
    def clean(self, phone):
        """Стандартизация телефонов к формату +7 (XXX) XXX-XX-XX"""
        phone = re.sub(r"\D", "", phone)  # Убираем все кроме цифр
        if len(phone) == 11 and phone.startswith("8"):
            phone = "+7" + phone[1:]
        if len(phone) != 11:
            return None  # Некорректный телефон
        return f"+7 ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:]}"
