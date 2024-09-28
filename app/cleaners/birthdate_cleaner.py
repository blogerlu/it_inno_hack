from datetime import datetime

from app.cleaners.base_cleaner import BaseCleaner


class BirthdateCleaner(BaseCleaner):
    def clean(self, birthdate):
        """Приведение даты рождения к формату YYYY-MM-DD и проверка на допустимые значения"""
        try:
            birthdate = birthdate.strip("-")
            if len(birthdate) == 4:  # Если указан только год
                return f"{birthdate}-XX-XX"

            date_obj = datetime.strptime(birthdate, "%Y-%m-%d")
            if 1900 <= date_obj.year <= 2024:
                return date_obj.strftime("%Y-%m-%d")
            elif date_obj.year < 1900:
                year = "XXXX"
                return f"{year}-{date_obj.month:02d}-{date_obj.day:02d}"
            elif date_obj.year > 2024:
                year = str(date_obj.year)
                year = "1" + year[1:]
                return f"{year}-{date_obj.month:02d}-{date_obj.day:02d}"
        except ValueError:
            return "XXXX-XX-XX"
