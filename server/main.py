import asyncio
import json
import sys

import aiohttp

from constants import BASE_URL
from utils import get_count_days, get_dates, get_currencies


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                return {'error_status': response.status, 'details': await response.text()}
        except aiohttp.ClientConnectorError as e:
            return {'errorStatus': e.errno, 'details': e}


def adapter_response(response, currencies=('EUR', 'USD')) -> dict:
    exchange_rate = response['exchangeRate']
    rates = {
        rate.get('currency'): {'sale': rate.get('saleRate', rate.get('saleRateNB')),
                               'purchase': rate.get('purchaseRate', rate.get('purchaseRateNB'))}
        for rate in exchange_rate if rate.get('currency', '') in currencies
    }
    return rates


async def get_rate(date: str, currencies: set) -> dict:
    url = f'{BASE_URL}/exchange_rates?json&date={date}'
    response = await request(url)
    if 'exchangeRate' in response:
        return {date: adapter_response(response, currencies)}
    return {date: response}


async def get_rates(dates, currencies) -> tuple:
    cors = [get_rate(date, currencies) for date in dates]
    return await asyncio.gather(*cors, return_exceptions=True)


def main():
    days = get_count_days(sys.argv)
    dates = get_dates(days)
    currencies = get_currencies(sys.argv)
    exchange_rate = asyncio.run(get_rates(dates, currencies))
    print(json.dumps(exchange_rate, indent=2))


if __name__ == '__main__':
    exit(main())
