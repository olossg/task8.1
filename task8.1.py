# Добавьте в класс Rate параметр diff (со значениями True или False),
# который в случае значения True в методах eur и usd будет возвращать не курс валюты, а изменение по сравнению в прошлым значением.
# Считайте, self.diff будет принимать значение True только при возврате значения курса.
# При отображении всей информации о валюте он не используется.
import requests
class Rate:
    def __init__(self, format_='value'):
        self.format = format_

    def exchange_rates(self):
        """
        Возвращает ответ сервиса с информацией о валютах в виде:

        {
            'AMD': {
                'CharCode': 'AMD',
                'ID': 'R01060',
                'Name': 'Армянских драмов',
                'Nominal': 100,
                'NumCode': '051',
                'Previous': 14.103,
                'Value': 14.0879
                },
            ...
        }
        """
        r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        return r.json()['Valute']

    def make_format(self, currency, diff='False'):
        """
        Возвращает информацию о валюте currency в двух вариантах:
        - полная информация о валюте при self.format = 'full':
        Rate('full').make_format('EUR')
        {
            'CharCode': 'EUR',
            'ID': 'R01239',
            'Name': 'Евро',
            'Nominal': 1,
            'NumCode': '978',
            'Previous': 79.6765,
            'Value': 79.4966
        }

        Rate('value').make_format('EUR')
        79.4966
        """
        self.diff = diff
        response = self.exchange_rates()

        if currency in response:
            if self.format == 'full':
                return response[currency]

            if self.format == 'value':
                if self.diff == 'True' and (currency == 'USD' or currency == 'EUR'):
                    return format(response[currency]['Value'] - response[currency]['Previous'], '.3f')
                return response[currency]['Value']

        return 'Error'


    def eur(self):
        """Возвращает курс евро на сегодня в формате self.format"""
        return self.make_format('EUR')

    def usd(self):
        """Возвращает курс доллара на сегодня в формате self.format"""
        return self.make_format('USD')

    def brl(self):
        """Возвращает курс бразильского реала на сегодня в формате self.format"""
        return self.make_format('BRL')

print(Rate().make_format('USD','True'))
