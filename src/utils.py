from datetime import datetime, timedelta

class Date:
    def __init__(self, date: str):
        self.value = datetime.strptime(date, "%Y-%m-%d")

    def __add__(self, days: int):
        if isinstance(days, int):
            new_date = self.value + timedelta(days=days)
            return new_date.strftime("%Y-%m-%d")
        else:
            raise ValueError("Days must be an integer")
        
    def __str__(self):
        return self.value.strftime("%Y-%m-%d")