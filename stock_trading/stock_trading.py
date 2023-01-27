# I would like to see about trading stock options. I would like to build a little experiement to see how much money
# I would gain/lose if I were to just start today with $500.

# I will be using the Yahoo Finance API in order to track prices.
import yfinance as yf

import yfinance as yf

cash = 500.00
my_stocks = {}

def add_transaction(company, price, type, count):
    return company + str(price) + type + str(count)

def adjust_owned_stocks(company, count):
    global my_stocks
    if company in my_stocks.keys():
        if my_stocks[company] + count < 0:
            print('Cannot have negative stocks.')
            return False
        my_stocks[company] += count
        if my_stocks[company] == 0:
            del my_stocks[company]
    else:
        my_stocks[company] = count
    return True


def buy(company, count=1):
    global cash
    # Check on time
    ticker = yf.Ticker(company)

    price = ticker.fast_info.last_price

    if cash < price * count:
        print('Not enough cash.')
        return

    cash -= price * count
    adjust_owned_stocks(company, count)
    add_transaction(company, price, 'buy', count)
    print(f'You bought {count} shares of {company} at {price} for a total of {price * count}.')

def sell(company, count=1):
    global cash
    # Check on time
    ticker = yf.Ticker(company)

    price = ticker.fast_info.last_price

    if not adjust_owned_stocks(company, -1 * count):
        return

    cash += price * count
    add_transaction(company, price, 'sell', count)
    print(f'You sold {count} shares of {company} at {price} for a total of {price * count}.')

    return

def current_worth():
    total_stock = 0
    print('Cash: ' + str(cash))
    for company in my_stocks.keys():
        ticker = yf.Ticker(company)
        price = ticker.fast_info.last_price
        print(f'{company}: {my_stocks[company]} at {price}')
        total_stock += my_stocks[company] * price
    print('Total Stock: ' + str(total_stock))
    print('Total Worth: ' + str(cash + total_stock))
    return


selected = 1

while selected != 0:
    current_worth()
    print('0 - Exit')
    print('1 - Buy')
    print('2 - Sell')
    selected = int(input())

    if selected == 1:
        company = input('Company: ')
        count = int(input('Ammount: '))
        buy(company, count)

    if selected == 2:
        company = input('Company: ')
        count = int(input('Ammount: '))
        sell(company, count)
