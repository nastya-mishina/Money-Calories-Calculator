import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.date_to_spending = {}
    
    '''
    Данная функция сохраняет наши записи о расходах/приемах пищи.
    '''
    def add_record(self, note):
        self.records.append(note)
        
        date_formate = note.date

        if note.date in self.date_to_spending:
            self.date_to_spending[date_formate] += note.amount
        else:
            self.date_to_spending[date_formate] = note.amount


    '''
    Считаем сколько денег/каллорий потрачено/съедено сегодня.
    '''
    def get_today_stats(self):
        today = dt.datetime.now().date()
        today_stats = 0
        
        if today in self.date_to_spending:
            today_stats = self.date_to_spending[today]
        return today_stats

    '''
    Считаем сколько денег/каллорий потрачено/съедено за последние 7 дней.
    '''
    def get_week_stats(self):
        dates = []
        today = dt.datetime.now().date()
        week_stats = 0
        dates.append(today)
        for i in range(1,7):
            period = dt.timedelta(days=i)
            seven_day = today - period
            dates.append(seven_day)
        
        for date in dates:
            if date in self.date_to_spending:
                week_stats += self.date_to_spending[date]
        return(week_stats)

class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    '''
    Определяем сколько каллорий можно еще использовать сегодня.
    '''
    def get_calories_remained(self):
        today_calories = self.get_today_stats()
        remaind = self.limit - today_calories

        if today_calories < self.limit:
            return(f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remaind} кКал')
        else:
            return('Хватит есть!')
    
    
        

class CashCalculator(Calculator):

    USD_RATE = 75.05
    EURO_RATE = 88.85

    '''
    Определяем сколько еще денег можно потратить сегодня в рублях, долларах или евро.
    '''
    def get_today_cash_remained(self, currency):    
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



class Record:
    def __init__(self, amount, comment, date=(dt.datetime.now()).date()):
        self.amount = amount
        self.comment = comment
        if type(date) is str:
            moment = dt.datetime.strptime(date, '%d.%m.%Y')
            self.date = moment.date()
        else:
            self.date = date

