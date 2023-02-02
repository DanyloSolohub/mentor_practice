from datetime import datetime, timedelta

from constants import AVAILABLE_CURRENCIES


def get_count_days(argv) -> int:
    try:
        days = int(argv[1]) if len(argv) > 1 else 1
    except ValueError:
        days = 1
    if not 0 < days <= 10:
        days = 1
    return days


def get_dates(total_days=1) -> list[str]:
    today = datetime.now()
    return [
        datetime.strftime(today - timedelta(days=day), '%d.%m.%Y')
        for day in range(total_days)
    ]


def get_currencies(argv) -> set:
    currencies = list(argv[2:])
    for currency in currencies:
        if currency not in AVAILABLE_CURRENCIES:
            currencies.remove(currency)
    if not currencies:
        currencies = ['EUR', 'USD']
    return set(currencies)
