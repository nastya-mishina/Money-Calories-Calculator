import datetime as dt


class Calculator:
    """
    Родительский класс для классов CashCalculator и CaloriesCalculator.
    """
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.date_to_spending = {}
    
    def add_record(self, record):
        """
        Данная функция сохраняет наши записи о расходах/приемах пищи.
        """
        self.records.append(record)
        
    def get_today_stats(self):
        """
        Считаем сколько денег/каллорий потрачено/съедено сегодня.
        """
        today = dt.date.today()
        today_stats = 0
        
        for record in self.records:
            if record.date == today:
                today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        """
        Считаем сколько денег/каллорий потрачено/съедено за последние 7 дней.
        """       
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        week_stats = 0

        for record in self.records:
            if week_ago < record.date <= today:
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    """
    Калькулятор калорий.
    """
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        """
        Определяем сколько каллорий можно еще использовать сегодня.
        """
        today_calories = self.get_today_stats()
        remaind = self.limit - today_calories

        if today_calories < self.limit:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remaind} кКал') 
        return 'Хватит есть!'    
    
        
class CashCalculator(Calculator):
    """
    Денежный калькулятор.
    """
    USD_RATE = 75.05
    EURO_RATE = 88.85

    def get_today_cash_remained(self, currency):
        """
        Определяем сколько еще денег можно потратить сегодня в рублях, долларах или евро.
        """    
        today_spend = self.get_today_stats()
        remaind = self.limit - today_spend
        debt = today_spend - self.limit
        
        if currency == 'rub':
            self.currency_out = 'руб'
        elif currency == 'usd':
            self.currency_out = 'USD'
            remaind = round(remaind/self.USD_RATE, 2)
            debt = round(debt/self.USD_RATE, 2)
        elif currency == 'eur':
            self.currency_out = 'Euro'
            remaind = round(remaind/self.EURO_RATE, 2)
            debt = round(debt/self.EURO_RATE, 2)

        if today_spend < self.limit:
            return(f'На сегодня осталось {remaind} {self.currency_out}')
        elif self.limit == today_spend:
            return('Денег нет, держись')
        else:
            return(f'Денег нет, держись: твой долг - {debt} {self.currency_out}')


DATE_FORMAT = '%d.%m.%Y'
class Record:
    """
    Класс для создания записей.
    """
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            moment = dt.datetime.strptime(date, DATE_FORMAT)
            self.date = moment.date()
        else:
            self.date = dt.date.today()
