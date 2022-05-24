from sqlite3 import Timestamp
import time
import requests
import pandas as pd
import os
import datetime

while(1):
    # call the orderbook from api
    response = requests.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = {}
    book = response.json()
    data = book['data']

    # pick the bid(type, timestampe) and make pd
    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors = 'ignore')
    bids.sort_values('price',ascending = False, inplace = True)
    bids = bids.reset_index(); del bids['index']
    bids[type] = 0
    bids[time] = datetime.datetime.now()

    # pick the ask(type, timestampe) and make pd
    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors = 'ignore')
    asks.sort_values('price',ascending = True, inplace = True)
    asks[type] = 1
    asks[time] = datetime.datetime.now()

    # combine the pd.bid and pd.aks
    df = bids.append(asks)

    # change the columns name
    df.columns = ['price', 'quantity', 'type', 'timestamp']

    # save the pd to csv
    if not os.path.exists('2022-05-22-Bithumb-btc-orderbook.csv'):
        df.to_csv("2022-05-22-Bithumb-btc-orderbook.csv", index = False, mode = 'w', sep = '|')
    else:
        df.to_csv("2022-05-22-Bithumb-btc-orderbook.csv", index = False, mode = 'a', header = False, sep = '|')



    time.sleep(1)