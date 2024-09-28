class BaseCleaner:
    def clean(self, value):
        """Метод очистки, который будет переопределен в наследниках."""
        raise NotImplementedError("Метод clean() должен быть реализован")
